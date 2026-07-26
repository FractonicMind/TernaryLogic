// =============================================================================
// Shadow_Buffer_Gate.v
// Ternary Logic — Dual-Lane Latency Architecture
// 02_Hardware_Primitives
//
// Author:       Lev Goukassian | FractonicMind
// Framework:    Ternary Logic (TL) — Mandated Ternary (MT) Hardware Layer
// Repository:   FractonicMind/TernaryLogic/PPT/02_Hardware_Primitives
//
// Description:
//   Per-PPT shadow buffer instance implementing the Reversibility Boundary.
//   One instance of this module is instantiated per concurrent PPT cycle.
//   Each instance owns its staging area exclusively — no routing tables,
//   no CAM, no cross-PPT contamination.
//
//   At 100 concurrent PPTs × 8 slots × ~64 bytes = ~51 KB total system
//   footprint. Less than a rounding error in modern manufacturing.
//
// Reversibility Boundary — constitutional definition:
//
//   Class R — Reversible (Provisional Computation):
//     ALU operations, volatile registers, internal state changes.
//     Authorized by PPT. Destroyed by C-element on provisionalExpiry.
//     Does NOT pass through this module.
//
//   Class I — Irreversible (External Actuation):
//     NIC transmissions, financial bus transfers, actuator commands,
//     outbound API calls, external database commits.
//     MUST pass through this module. Physical port stays CLOSED
//     until the State 2 rail goes high.
//
// The Two-Signal Chain (constitutional requirement):
//   FPT arrives → cryptographic validation → C-element achieves State 2
//   → state_2_active HIGH → port_enable HIGH → port opens → world
//
//   The FPT NEVER directly controls port_enable.
//   The Shadow Buffer Gate obeys State 2. Only State 2.
//
// Rollback — single-cycle wipe:
//   When provisionalExpiry fires, the C-element cuts voltage to this
//   module's enable rail. The entire buffer is grounded in one clock
//   cycle. No routing table search. No partial clear. No race condition.
//   Physics, not logic.
//
// Per-PPT instantiation — why it is the only correct architecture:
//   A shared buffer requires Content Addressable Memory (CAM) to map
//   staged actions back to their originating PPT. CAM is expensive,
//   power-hungry, and puts matching logic in the critical path.
//   Per-PPT instances require none of this. Rollback is a voltage cut.
//   Isolation is total. Silicon cost is negligible.
//
// Adversarial guarantee:
//   FPT suppression → mass provisionalExpiry → per-PPT buffers wiped
//   → physical ports never opened → world untouched → electricity wasted.
//
// Behavioral model: SYNTHESIZABLE RTL
//   Instantiate one module per concurrent PPT slot.
//   BUFFER_DEPTH = 8 covers the upper bound of Class I actions per
//   transaction across all TL deployment domains. [Engineering Estimate]
//
// Evidence classification: [Demonstrated] for circuit topology
//                          [Engineering Estimate] for BUFFER_DEPTH sizing
// =============================================================================

`timescale 1ns / 1ps

module shadow_buffer_gate #(
    parameter PORT_WIDTH    = 64,   // Width of physical port (bits)
    parameter BUFFER_DEPTH  = 8,    // Class I staging slots per PPT instance
                                     // 8 slots covers upper bound of any domain
                                     // 100 PPTs × 8 × 64b = ~51KB system total
    parameter ADDR_WIDTH    = 3     // log2(BUFFER_DEPTH) — 3 bits for 8 slots
) (
    // Clock and reset
    input  wire                     clk,
    input  wire                     rst_n,

    // =========================================================================
    // PPT identity — ties this instance to its owning PPT cycle
    // =========================================================================
    input  wire [63:0]              ppt_nonce,      // Nonce of the owning PPT
                                                     // For audit logging only
                                                     // Not used for routing

    // =========================================================================
    // State machine interface — from C_Element_Interlock.v
    // This module obeys state. It does not know what an FPT is.
    // =========================================================================
    input  wire                     state_1_active, // Provisional Execution
    input  wire                     state_2_active, // Final Confirmed Execution
                                                     // THIS opens the port

    // =========================================================================
    // Class I payload staging — from ALU pipeline during State 1
    // =========================================================================
    input  wire                     stage_valid,    // New Class I payload ready
    input  wire [PORT_WIDTH-1:0]    stage_payload,  // Payload from ALU
    output reg                      stage_ready,    // Buffer has space (backpressure)
    output wire                     buffer_full,    // All 8 slots occupied

    // =========================================================================
    // Physical port — Class I output
    // CLOSED during State 0 and State 1. OPENS on State 2 assertion.
    // This wire connects to the NIC enable pin, actuator enable, or
    // outbound bus enable. It is a physical wire, not a register.
    // =========================================================================
    output reg  [PORT_WIDTH-1:0]    port_data,      // Released Class I payload
    output reg                      port_valid,     // Data on port is valid
    output reg                      port_enable,    // Physical port enable
                                                     // Hardwired to device enable pin

    // =========================================================================
    // Single-cycle wipe interface
    // When C-element cuts voltage on provisionalExpiry, wipe_enable goes
    // high for exactly one cycle. The entire buffer is zeroed. Done.
    // =========================================================================
    input  wire                     wipe_enable,    // From C-element collapse
                                                     // One cycle = full buffer clear

    // =========================================================================
    // Audit outputs — for Tri-Cameral oversight and Immutable Ledger
    // =========================================================================
    output reg  [ADDR_WIDTH:0]      staged_count,   // Current staged payload count
    output reg                      release_event,  // Pulse: payload released (State 2)
    output reg                      wipe_event,     // Pulse: buffer wiped (expiry)
    output reg  [31:0]              lifetime_staged,   // Total staged since reset
    output reg  [31:0]              lifetime_released, // Total released to world
    output reg  [31:0]              lifetime_wiped     // Total wiped (never released)
);

    // =========================================================================
    // Shadow buffer — BUFFER_DEPTH slots of PORT_WIDTH bits
    // Allocated statically. No dynamic sizing. No routing table.
    // This is the holding pen.
    // =========================================================================

    reg [PORT_WIDTH-1:0]    shadow_buffer [0:BUFFER_DEPTH-1];
    reg [ADDR_WIDTH-1:0]    write_ptr;
    reg [ADDR_WIDTH-1:0]    read_ptr;
    reg                     state_2_prev;

    assign buffer_full = (staged_count == BUFFER_DEPTH[ADDR_WIDTH:0]);

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            port_data        <= {PORT_WIDTH{1'b0}};
            port_valid       <= 1'b0;
            port_enable      <= 1'b0;       // Port CLOSED on reset
            stage_ready      <= 1'b1;
            staged_count     <= {(ADDR_WIDTH+1){1'b0}};
            write_ptr        <= {ADDR_WIDTH{1'b0}};
            read_ptr         <= {ADDR_WIDTH{1'b0}};
            release_event    <= 1'b0;
            wipe_event       <= 1'b0;
            lifetime_staged  <= 32'd0;
            lifetime_released<= 32'd0;
            lifetime_wiped   <= 32'd0;
            state_2_prev     <= 1'b0;
            for (i = 0; i < BUFFER_DEPTH; i = i + 1)
                shadow_buffer[i] <= {PORT_WIDTH{1'b0}};
        end else begin
            state_2_prev  <= state_2_active;
            release_event <= 1'b0;
            wipe_event    <= 1'b0;

            // =================================================================
            // SINGLE-CYCLE WIPE
            // provisionalExpiry fired. C-element cut the enable rail.
            // wipe_enable is high for exactly one clock cycle.
            // Zero every slot. Reset pointers. Port stays CLOSED.
            // This is a voltage cut expressed in RTL.
            // =================================================================
            if (wipe_enable) begin
                for (i = 0; i < BUFFER_DEPTH; i = i + 1)
                    shadow_buffer[i] <= {PORT_WIDTH{1'b0}};
                lifetime_wiped   <= lifetime_wiped + staged_count;
                staged_count     <= {(ADDR_WIDTH+1){1'b0}};
                write_ptr        <= {ADDR_WIDTH{1'b0}};
                read_ptr         <= {ADDR_WIDTH{1'b0}};
                port_enable      <= 1'b0;   // Port stays CLOSED
                port_valid       <= 1'b0;
                stage_ready      <= 1'b1;
                wipe_event       <= 1'b1;   // Audit: buffer wiped without release
            end

            // =================================================================
            // STATE 1 — Provisional Execution
            // Workers are packing boxes. Loading dock doors stay LOCKED.
            // Accept Class I payloads from ALU. Stage them. Wait for State 2.
            // =================================================================
            else if (state_1_active && !state_2_active) begin
                port_enable <= 1'b0;    // Port CLOSED during State 1
                port_valid  <= 1'b0;

                if (stage_valid && !buffer_full) begin
                    shadow_buffer[write_ptr] <= stage_payload;
                    write_ptr        <= write_ptr + 1'b1;
                    staged_count     <= staged_count + 1'b1;
                    lifetime_staged  <= lifetime_staged + 1'b1;
                end

                // Backpressure: buffer full — signal Lane 1 to stop minting PPTs
                stage_ready <= ~buffer_full;
            end

            // =================================================================
            // STATE 2 — Final Confirmed Execution
            // Manager arrived with the final receipt. Physical key turned.
            // THE STATE 2 RAIL OPENS THE PORT. Not the FPT. State 2.
            // Release staged Class I payloads sequentially.
            // =================================================================
            else if (state_2_active) begin

                // Rising edge of State 2: open the physical port
                if (!state_2_prev) begin
                    port_enable <= 1'b1;    // Physical port OPENS
                end

                // Release payloads from shadow buffer
                if (!buffer_empty_internal && port_enable) begin
                    port_data        <= shadow_buffer[read_ptr];
                    port_valid       <= 1'b1;
                    read_ptr         <= read_ptr + 1'b1;
                    staged_count     <= staged_count - 1'b1;
                    release_event    <= 1'b1;
                    lifetime_released<= lifetime_released + 1'b1;
                end else begin
                    port_valid <= 1'b0;
                end
            end

            // =================================================================
            // STATE 0 — Epistemic Hold
            // Default state. Port CLOSED. Buffer empty.
            // =================================================================
            else begin
                port_enable <= 1'b0;
                port_valid  <= 1'b0;
                stage_ready <= 1'b1;
            end
        end
    end

    // Buffer empty when read_ptr has caught up to write_ptr
    wire buffer_empty_internal = (staged_count == {(ADDR_WIDTH+1){1'b0}});

endmodule


// =============================================================================
// shadow_buffer_array
// Top-level instantiation of N per-PPT shadow buffer instances.
// One instance per concurrent PPT slot. No shared state between instances.
// No routing table. No CAM. Rollback of instance K does not affect K+1.
//
// Parameter N_PPT_SLOTS matches the system's configured concurrent PPT cap
// (default: 100, matching Governor Independence throughput model).
// =============================================================================

module shadow_buffer_array #(
    parameter N_PPT_SLOTS   = 100,  // Concurrent PPT capacity
    parameter PORT_WIDTH    = 64,
    parameter BUFFER_DEPTH  = 8,
    parameter ADDR_WIDTH    = 3
) (
    input  wire                             clk,
    input  wire                             rst_n,

    // Per-slot control signals (indexed by PPT slot)
    input  wire [N_PPT_SLOTS-1:0]           state_1,        // Per-slot State 1
    input  wire [N_PPT_SLOTS-1:0]           state_2,        // Per-slot State 2
    input  wire [N_PPT_SLOTS-1:0]           wipe,           // Per-slot wipe
    input  wire [N_PPT_SLOTS-1:0]           stage_valid_in, // Per-slot stage request
    input  wire [PORT_WIDTH*N_PPT_SLOTS-1:0] stage_payloads, // Per-slot payloads

    // Per-slot outputs
    output wire [N_PPT_SLOTS-1:0]           stage_ready_out,
    output wire [N_PPT_SLOTS-1:0]           port_enable_out,
    output wire [PORT_WIDTH*N_PPT_SLOTS-1:0] port_data_out,
    output wire [N_PPT_SLOTS-1:0]           port_valid_out,
    output wire [N_PPT_SLOTS-1:0]           wipe_event_out,
    output wire [N_PPT_SLOTS-1:0]           release_event_out,

    // Backpressure: any slot full halts new PPT minting
    output wire                             any_slot_full
);

    wire [N_PPT_SLOTS-1:0] slot_full;
    assign any_slot_full = |slot_full;

    genvar k;
    generate
        for (k = 0; k < N_PPT_SLOTS; k = k + 1) begin : slot_gen
            shadow_buffer_gate #(
                .PORT_WIDTH   (PORT_WIDTH),
                .BUFFER_DEPTH (BUFFER_DEPTH),
                .ADDR_WIDTH   (ADDR_WIDTH)
            ) u_slot (
                .clk            (clk),
                .rst_n          (rst_n),
                .ppt_nonce      (64'd0),    // Connected per-slot in full integration
                .state_1_active (state_1[k]),
                .state_2_active (state_2[k]),
                .stage_valid    (stage_valid_in[k]),
                .stage_payload  (stage_payloads[PORT_WIDTH*(k+1)-1 : PORT_WIDTH*k]),
                .stage_ready    (stage_ready_out[k]),
                .buffer_full    (slot_full[k]),
                .port_data      (port_data_out[PORT_WIDTH*(k+1)-1 : PORT_WIDTH*k]),
                .port_valid     (port_valid_out[k]),
                .port_enable    (port_enable_out[k]),
                .wipe_enable    (wipe[k]),
                .staged_count   (),         // Connected to oversight in full integration
                .release_event  (release_event_out[k]),
                .wipe_event     (wipe_event_out[k]),
                .lifetime_staged   (),
                .lifetime_released (),
                .lifetime_wiped    ()
            );
        end
    endgenerate

endmodule

// =============================================================================
// Design Notes
//
// Why BUFFER_DEPTH = 8:
//   Financial execution: typically 2–4 Class I actions per transaction
//     (payment message, settlement instruction, confirmation dispatch,
//      regulatory report). 8 provides 2× headroom.
//   AI governance: typically 1–2 Class I actions per authorized decision
//     (response dispatch, downstream agent instruction). 8 is generous.
//   Autonomous systems: typically 1 Class I action per authorization
//     (single actuator command per PPT). 8 is very generous.
//   Industrial control: typically 1–3 Class I actions per command
//     (valve open, conveyor start, interlock release). 8 provides margin.
//   The 8-slot figure covers the extreme upper bound across all domains.
//   [Engineering Estimate — subject to domain-specific validation]
//
// Single-cycle wipe implementation:
//   In physical silicon, wipe_enable is the output of the C-element's
//   provisionalExpiry detection circuit. When the watchdog fires:
//     1. C-element output collapses (45ps propagation)
//     2. wipe_enable asserted for exactly one clock cycle
//     3. All 8 buffer slots zeroed simultaneously
//     4. Pointers reset
//     5. port_enable remains low
//   Total wipe time: 1 clock cycle at system frequency.
//   At 200 MHz: 5 nanoseconds. This is physics, not software.
//
// Backpressure chain:
//   shadow_buffer_array.any_slot_full → Lane 1 PPT pipeline stall
//   When any slot is full, no new PPTs are minted until:
//     (a) An FPT arrives and State 2 releases a slot, or
//     (b) A provisionalExpiry fires and wipes a slot
//   The warehouse stops accepting orders when the holding pen is full.
//   This is the correct behavior. It is not a failure mode.
//
// Physical port wiring:
//   port_enable[k] connects to the enable pin of the k-th PPT slot's
//   designated physical output device (NIC port, actuator controller,
//   financial bus interface). The wire is physically distinct from any
//   software-accessible register. No software path can assert port_enable.
//   Only state_2_active from the C-element can do so.
//
// Protocol agnosticism:
//   If the FPT mechanism changes (PQC migration, human-in-the-loop,
//   new consensus ledger), this module requires zero modification.
//   It responds to state_2_active. How State 2 is achieved is not
//   this module's concern.
// =============================================================================
