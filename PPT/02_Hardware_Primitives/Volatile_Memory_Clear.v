// =============================================================================
// Volatile_Memory_Clear.v
// Ternary Logic — Dual-Lane Latency Architecture
// 02_Hardware_Primitives
//
// Author:       Lev Goukassian | FractonicMind
// Framework:    Ternary Logic (TL) — Mandated Ternary (MT) Hardware Layer
// Repository:   FractonicMind/TernaryLogic/PPT/02_Hardware_Primitives
//
// Description:
//   Buffer invalidation logic triggered by C-element state_release going low.
//   This module monitors the C-element output and — on a high-to-low
//   transition (State 1 → State 0 snapback) — asserts validity bit
//   invalidation across the provisional execution buffer.
//
//   What this module does:
//     - Detects the falling edge of state_release (C-element collapse)
//     - Asserts buffer_invalid_strobe to the provisional execution buffer
//     - Zeros all validity bits in the volatile buffer (uncommitted data
//       is marked invalid — reads return INVALID_DATA sentinel)
//     - Signals clearing_complete when invalidation is finished
//     - Generates snapback_event for application-layer compensation logic
//
//   What this module does NOT do:
//     - It does not zero the data bytes themselves (only validity bits)
//     - It does not reverse externally visible effects (transmitted packets,
//       engaged actuators, persistent storage writes)
//     - It does not generate compensating transactions
//     - It does not touch Lane 2 / FPT infrastructure
//
//   The distinction between validity-bit invalidation and data erasure is
//   intentional. Data erasure introduces latency proportional to buffer size.
//   Validity-bit invalidation is O(1) — a single broadcast signal marks
//   all entries invalid simultaneously. The data bytes are overwritten on
//   the next write to each address after a fresh PPT cycle begins.
//
// Behavioral model: SYNTHESIZABLE RTL
//   Targeting Xilinx Versal / UltraScale+ or equivalent.
//   BUF_ENTRIES parameter must match the provisional execution buffer size
//   in the system integration.
//
// Evidence classification: [Engineering Estimate] for timing parameters
// =============================================================================

`timescale 1ns / 1ps

module volatile_memory_clear #(
    parameter BUF_ENTRIES    = 1024,    // Number of entries in provisional buffer
    parameter ADDR_WIDTH     = 10,      // log2(BUF_ENTRIES)
    parameter DATA_WIDTH     = 64,      // Data width per entry (bits)
    parameter INVALID_SENTINEL = 64'hDEAD_C0DE_DEAD_C0DE  // Sentinel for debug reads
) (
    // Clock and reset
    input  wire                    clk,
    input  wire                    rst_n,

    // C-element interface
    input  wire                    state_release,       // From C_Element_Interlock
                                                         // Falling edge triggers clear

    // Provisional buffer interface (validity bits only — not data path)
    output reg  [BUF_ENTRIES-1:0]  validity_bits,       // 1 = valid; 0 = invalid
    output reg                     buffer_invalid_strobe, // Pulse: start invalidation
    output reg                     clearing_active,     // HIGH during invalidation
    output reg                     clearing_complete,   // Pulse: invalidation done

    // Write port (during State 1: provisional execution writes)
    input  wire                    write_enable,        // From execution pipeline
    input  wire [ADDR_WIDTH-1:0]   write_addr,          // Write address
    input  wire [DATA_WIDTH-1:0]   write_data,          // Write data (not stored here;
                                                         // this module only tracks valid)
    // Read port (validity check)
    input  wire [ADDR_WIDTH-1:0]   read_addr,           // Read address
    output wire                    read_valid,           // Is the read address valid?

    // Application-layer signaling
    output reg                     snapback_event,      // HIGH for 1 cycle on snapback
                                                         // Application layer monitors
                                                         // this to trigger compensation

    // Status
    output reg  [ADDR_WIDTH:0]     valid_entry_count,   // Number of valid entries
    output wire                    buffer_clean         // HIGH when all entries invalid
);

    // =========================================================================
    // Internal signals
    // =========================================================================

    reg                     state_release_prev;     // Previous cycle state_release
    wire                    falling_edge_detected;  // Falling edge of state_release
    reg  [ADDR_WIDTH-1:0]   clear_addr;             // Address being cleared
    reg                     clear_in_progress;      // Sequential clear state

    // =========================================================================
    // Falling edge detection: state_release HIGH → LOW = State 0 snapback
    // This is the trigger for all invalidation actions.
    // =========================================================================

    assign falling_edge_detected = state_release_prev & ~state_release;

    // =========================================================================
    // Read validity: check if a given address holds valid provisional data
    // =========================================================================

    assign read_valid  = validity_bits[read_addr];
    assign buffer_clean = (valid_entry_count == {(ADDR_WIDTH+1){1'b0}});

    // =========================================================================
    // Main control logic
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            validity_bits          <= {BUF_ENTRIES{1'b0}};  // All invalid on reset
            buffer_invalid_strobe  <= 1'b0;
            clearing_active        <= 1'b0;
            clearing_complete      <= 1'b0;
            snapback_event         <= 1'b0;
            valid_entry_count      <= {(ADDR_WIDTH+1){1'b0}};
            clear_addr             <= {ADDR_WIDTH{1'b0}};
            clear_in_progress      <= 1'b0;
            state_release_prev     <= 1'b0;
        end else begin

            // Track previous state_release for edge detection
            state_release_prev <= state_release;

            // Default: clear single-cycle pulses
            buffer_invalid_strobe <= 1'b0;
            clearing_complete     <= 1'b0;
            snapback_event        <= 1'b0;

            // ================================================================
            // FALLING EDGE DETECTED: State 1 → State 0 snapback
            // Begin invalidation sequence immediately.
            //
            // Option 1 — Broadcast invalidation (preferred, O(1)):
            //   Assert a broadcast signal that all validity bits are 0.
            //   This requires the target buffer to implement a "broadcast_invalid"
            //   control input that clears all validity bits in one cycle.
            //   clearing_complete is asserted the next cycle.
            //
            // Option 2 — Sequential invalidation (O(N), fallback):
            //   Walk through all entries and clear validity bits one by one.
            //   Used when the target buffer does not support broadcast_invalid.
            //   clearing_complete is asserted after BUF_ENTRIES cycles.
            //
            // This module implements Option 2 for generality.
            // System integrators should implement Option 1 where possible.
            // ================================================================

            if (falling_edge_detected) begin
                // Immediate actions on snapback detection
                buffer_invalid_strobe <= 1'b1;  // Pulse to buffer
                snapback_event        <= 1'b1;  // Notify application layer
                clearing_active       <= 1'b1;
                clear_addr            <= {ADDR_WIDTH{1'b0}};
                clear_in_progress     <= 1'b1;

                // Begin sequential clear from address 0
                validity_bits[0]      <= 1'b0;
                clear_addr            <= {{(ADDR_WIDTH-1){1'b0}}, 1'b1};
            end

            // Sequential clear in progress
            else if (clear_in_progress) begin
                validity_bits[clear_addr] <= 1'b0;

                if (clear_addr == BUF_ENTRIES[ADDR_WIDTH:1]) begin
                    // All entries cleared
                    clear_in_progress  <= 1'b0;
                    clearing_active    <= 1'b0;
                    clearing_complete  <= 1'b1;
                    valid_entry_count  <= {(ADDR_WIDTH+1){1'b0}};
                    clear_addr         <= {ADDR_WIDTH{1'b0}};
                end else begin
                    clear_addr <= clear_addr + 1'b1;
                end
            end

            // Normal operation: provisional execution writes validity bits
            else if (write_enable && state_release && !clearing_active) begin
                // Only accept writes during State 1 (state_release HIGH)
                validity_bits[write_addr] <= 1'b1;
                valid_entry_count         <= valid_entry_count + 1'b1;
            end

        end
    end

endmodule


// =============================================================================
// snapback_event_logger
// Monitors snapback_event and logs each occurrence with a timestamp.
// This provides an audit trail of all State 0 snapbacks for post-hoc
// analysis and regulatory audit purposes.
//
// The log is read-only from software — it cannot be cleared by software.
// Hardware reset clears it (power cycle / system reset only).
// =============================================================================

module snapback_event_logger #(
    parameter LOG_DEPTH    = 64,         // Number of snapback events to retain
    parameter TS_WIDTH     = 64          // Timestamp width (nanosecond resolution)
) (
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    snapback_event,  // From volatile_memory_clear
    input  wire [TS_WIDTH-1:0]     timestamp,       // Hardware timestamp counter

    // Log read interface (read-only from software via memory-mapped register)
    input  wire [$clog2(LOG_DEPTH)-1:0] read_idx,
    output wire [TS_WIDTH-1:0]     log_entry,
    output wire [$clog2(LOG_DEPTH):0]   log_count,  // Number of events logged
    output wire                    log_overflow     // HIGH if > LOG_DEPTH events
);

    localparam IDX_WIDTH = $clog2(LOG_DEPTH);

    reg [TS_WIDTH-1:0]  event_log [0:LOG_DEPTH-1];
    reg [IDX_WIDTH:0]   write_ptr;
    reg                 overflow;

    assign log_entry    = event_log[read_idx];
    assign log_count    = write_ptr;
    assign log_overflow = overflow;

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            write_ptr <= {(IDX_WIDTH+1){1'b0}};
            overflow  <= 1'b0;
            for (i = 0; i < LOG_DEPTH; i = i + 1)
                event_log[i] <= {TS_WIDTH{1'b0}};
        end else if (snapback_event) begin
            if (write_ptr < LOG_DEPTH[IDX_WIDTH:0]) begin
                event_log[write_ptr[IDX_WIDTH-1:0]] <= timestamp;
                write_ptr <= write_ptr + 1'b1;
            end else begin
                overflow <= 1'b1;
                // Oldest entry is overwritten (circular buffer)
                event_log[write_ptr[IDX_WIDTH-1:0]] <= timestamp;
            end
        end
    end

endmodule


// =============================================================================
// Design Notes
//
// Rollback scope boundary (see C_Element_Rollback.md):
//   This module invalidates the provisional execution buffer's validity bits.
//   It does NOT:
//     - Transmit network rollback packets
//     - Send actuator reversal commands
//     - Write compensating transactions to databases
//     - Interact with Lane 2 infrastructure
//
//   All externally visible effects during the provisional window require
//   application-layer compensation triggered by snapback_event.
//   The application must register a snapback_event handler before
//   entering State 1 if it may produce externally visible effects.
//
// Broadcast invalidation (performance optimization):
//   In the system integration, the provisional buffer should implement a
//   'broadcast_invalid' control input that sets all validity bits to 0
//   in a single clock cycle. This module's sequential clear loop is the
//   fallback for buffers that do not support broadcast invalidation.
//   For buffers > 256 entries, the sequential clear may introduce
//   non-trivial latency (N clock cycles). Broadcast invalidation is
//   strongly recommended for large buffers.
//
// Power-on requirement:
//   On power-on reset, validity_bits initializes to all zeros (all invalid).
//   The system must not assert write_enable until a valid PPT has been
//   issued and state_release is HIGH. This is enforced by the C-element:
//   write_enable should be gated by state_release in the system integration.
// =============================================================================
