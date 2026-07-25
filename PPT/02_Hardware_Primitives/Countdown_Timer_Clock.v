// =============================================================================
// Countdown_Timer_Clock.v
// Ternary Logic — Dual-Lane Latency Architecture
// 02_Hardware_Primitives
//
// Author:       Lev Goukassian | FractonicMind
// Framework:    Ternary Logic (TL) — Mandated Ternary (MT) Hardware Layer
// Repository:   FractonicMind/TernaryLogic/PPT/02_Hardware_Primitives
//
// Description:
//   Hardware watchdog counter implementing TL's provisionalExpiry mechanism.
//   This module begins counting on PPT issuance (ppt_issued strobe) and
//   fires expiry_signal when the configured bound is reached — triggering
//   State 0 snapback in the C-element interlock.
//
//   The timer operates independently of software. It cannot be paused,
//   reset, or extended by any software path after ppt_issued is asserted.
//   This is the hardware enforcement of TL's provisional window guarantee:
//   the window has a deterministic upper bound regardless of software behavior.
//
// Critical safety requirement:
//   The timer's operational status is monitored by a secondary watchdog
//   (heartbeat). If the timer's heartbeat signal is absent for more than
//   2× the configured tick period, the secondary watchdog asserts
//   timer_fault and forces expiry_signal high — fail-closed behavior.
//   A failed timer defaults to expired. The system never remains in State 1
//   due to timer failure.
//
// Behavioral model: SYNTHESIZABLE RTL
//   Targeting Xilinx Versal / UltraScale+ or equivalent.
//   Clock frequency parameter (CLK_FREQ_MHZ) must be set at synthesis time
//   to match the system clock frequency.
//
// Evidence classification: [Engineering Estimate] for timing parameters
// =============================================================================

`timescale 1ns / 1ps

module countdown_timer_clock #(
    parameter CLK_FREQ_MHZ    = 200,        // System clock frequency in MHz
    parameter EXPIRY_MS_MAX   = 50,         // Maximum configurable expiry in ms
    parameter COUNTER_WIDTH   = 32          // Counter width — must accommodate
                                            // CLK_FREQ_MHZ * EXPIRY_MS_MAX * 1000
                                            // = 200 * 50 * 1000 = 10,000,000
                                            // 32 bits sufficient (max ~4.3 billion)
) (
    // Clock and reset
    input  wire                    clk,
    input  wire                    rst_n,           // Active-low synchronous reset

    // Timer configuration (set before ppt_issued, held constant during window)
    input  wire [31:0]             expiry_ms,       // Provisional window in ms
                                                     // Must be ≤ EXPIRY_MS_MAX
                                                     // Typically 50 for Lane 1

    // Control signals
    input  wire                    ppt_issued,      // Strobe: PPT has been minted
                                                     // Rising edge starts timer
    input  wire                    fpt_arrived,     // Strobe: valid FPT received
                                                     // Clears timer (State 2 reached)

    // Timer outputs
    output reg                     expiry_signal,   // HIGH = provisionalExpiry fired
                                                     // Wired to C-element ppt_valid_n
    output reg                     timer_active,    // HIGH = timer is running
    output wire [COUNTER_WIDTH-1:0] ticks_remaining, // Remaining ticks (monitoring)
    output wire [31:0]             ms_remaining,    // Remaining ms (monitoring, approx)

    // Heartbeat (for secondary watchdog monitoring)
    output reg                     heartbeat,       // Toggles every 1ms when timer active

    // Fault signals
    input  wire                    secondary_wd_fault, // Secondary watchdog asserts fault
    output reg                     timer_fault,     // Timer failure detected
    output reg                     config_fault     // expiry_ms > EXPIRY_MS_MAX
);

    // =========================================================================
    // Internal signals and registers
    // =========================================================================

    localparam TICKS_PER_MS = CLK_FREQ_MHZ * 1000; // Ticks per millisecond

    reg  [COUNTER_WIDTH-1:0] counter;           // Main countdown counter
    reg  [COUNTER_WIDTH-1:0] expiry_ticks;      // Configured expiry in ticks
    reg  [COUNTER_WIDTH-1:0] heartbeat_counter; // 1ms heartbeat sub-counter
    reg                      timer_started;     // Edge detector state for ppt_issued
    reg                      fpt_edge;          // Edge detector state for fpt_arrived

    wire                     ppt_rising_edge;   // Rising edge of ppt_issued
    wire                     fpt_rising_edge;   // Rising edge of fpt_arrived
    wire                     counter_expired;   // True when counter reaches zero

    // =========================================================================
    // Edge detection for ppt_issued and fpt_arrived strobes
    // =========================================================================

    assign ppt_rising_edge = ppt_issued & ~timer_started;
    assign fpt_rising_edge = fpt_arrived & ~fpt_edge;
    assign counter_expired = (counter == {COUNTER_WIDTH{1'b0}}) & timer_active;

    // =========================================================================
    // Configuration fault detection
    // Reject configurations where expiry_ms exceeds the hardware maximum
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            config_fault <= 1'b0;
        end else begin
            config_fault <= (expiry_ms > EXPIRY_MS_MAX[31:0]);
        end
    end

    // =========================================================================
    // Main timer logic
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter        <= {COUNTER_WIDTH{1'b0}};
            expiry_ticks   <= {COUNTER_WIDTH{1'b0}};
            timer_active   <= 1'b0;
            expiry_signal  <= 1'b0;
            timer_started  <= 1'b0;
            fpt_edge       <= 1'b0;
            timer_fault    <= 1'b0;
        end else begin

            // Update edge detector states
            timer_started <= ppt_issued;
            fpt_edge      <= fpt_arrived;

            // Timer fault: propagate secondary watchdog fault → fail closed
            if (secondary_wd_fault) begin
                timer_fault   <= 1'b1;
                expiry_signal <= 1'b1;   // Force expiry — fail-closed
                timer_active  <= 1'b0;
                counter       <= {COUNTER_WIDTH{1'b0}};
            end

            // Configuration fault: do not start timer with invalid configuration
            else if (config_fault) begin
                expiry_signal <= 1'b1;   // Reject invalid config — fail-closed
                timer_active  <= 1'b0;
            end

            // PPT issued: start the countdown
            else if (ppt_rising_edge && !timer_active && !config_fault) begin
                expiry_ticks  <= expiry_ms * TICKS_PER_MS[COUNTER_WIDTH-1:0];
                counter       <= expiry_ms * TICKS_PER_MS[COUNTER_WIDTH-1:0];
                timer_active  <= 1'b1;
                expiry_signal <= 1'b0;
                timer_fault   <= 1'b0;
            end

            // FPT arrived: valid FPT before expiry — clear timer, State 2 reached
            else if (fpt_rising_edge && timer_active) begin
                counter       <= {COUNTER_WIDTH{1'b0}};
                timer_active  <= 1'b0;
                expiry_signal <= 1'b0;
            end

            // Timer running: decrement counter
            else if (timer_active && !counter_expired) begin
                counter <= counter - 1'b1;
            end

            // Counter expired: fire provisionalExpiry — State 0 snapback
            else if (counter_expired) begin
                expiry_signal <= 1'b1;   // Triggers C-element ppt_valid pull-down
                timer_active  <= 1'b0;
                counter       <= {COUNTER_WIDTH{1'b0}};
            end

        end
    end

    // =========================================================================
    // Monitoring outputs
    // =========================================================================

    assign ticks_remaining = timer_active ? counter : {COUNTER_WIDTH{1'b0}};
    assign ms_remaining    = timer_active ?
                             (counter / TICKS_PER_MS[COUNTER_WIDTH-1:0]) : 32'd0;

    // =========================================================================
    // Heartbeat generator — toggles every 1ms when timer is active
    // Monitored by secondary watchdog. Absence of heartbeat for > 2ms
    // causes secondary_wd_fault to be asserted externally.
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            heartbeat         <= 1'b0;
            heartbeat_counter <= {COUNTER_WIDTH{1'b0}};
        end else if (timer_active) begin
            if (heartbeat_counter >= TICKS_PER_MS[COUNTER_WIDTH-1:0] - 1) begin
                heartbeat         <= ~heartbeat;
                heartbeat_counter <= {COUNTER_WIDTH{1'b0}};
            end else begin
                heartbeat_counter <= heartbeat_counter + 1'b1;
            end
        end else begin
            heartbeat_counter <= {COUNTER_WIDTH{1'b0}};
        end
    end

endmodule


// =============================================================================
// secondary_watchdog
// Monitors the primary countdown_timer_clock heartbeat.
// If heartbeat is absent for > 2× tick period, asserts wd_fault_out.
// This ensures that a crashed primary timer results in fail-closed behavior
// (expiry_signal forced high, State 0 asserted) rather than indefinite
// State 1 persistence.
// =============================================================================

module secondary_watchdog #(
    parameter CLK_FREQ_MHZ = 200,
    parameter TIMEOUT_MS   = 2           // Heartbeat timeout: 2ms
) (
    input  wire clk,
    input  wire rst_n,
    input  wire timer_active,            // From countdown_timer_clock
    input  wire heartbeat,               // From countdown_timer_clock
    output reg  wd_fault_out             // Asserted when heartbeat absent > TIMEOUT_MS
);

    localparam TIMEOUT_TICKS = CLK_FREQ_MHZ * 1000 * TIMEOUT_MS;
    localparam WD_WIDTH = 32;

    reg [WD_WIDTH-1:0] wd_counter;
    reg                hb_prev;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wd_counter  <= {WD_WIDTH{1'b0}};
            wd_fault_out <= 1'b0;
            hb_prev     <= 1'b0;
        end else begin
            hb_prev <= heartbeat;

            // If timer is not active, reset watchdog — no fault
            if (!timer_active) begin
                wd_counter   <= {WD_WIDTH{1'b0}};
                wd_fault_out <= 1'b0;
            end
            // Heartbeat toggled — reset watchdog counter
            else if (heartbeat != hb_prev) begin
                wd_counter   <= {WD_WIDTH{1'b0}};
                wd_fault_out <= 1'b0;
            end
            // No heartbeat toggle — increment counter
            else if (wd_counter < TIMEOUT_TICKS[WD_WIDTH-1:0]) begin
                wd_counter <= wd_counter + 1'b1;
            end
            // Timeout exceeded — assert fault (fail-closed)
            else begin
                wd_fault_out <= 1'b1;
            end
        end
    end

endmodule


// =============================================================================
// Design Notes
//
// provisionalExpiry configuration:
//   - Standard Lane 1 mode: expiry_ms = 50 (50 ms)
//   - Strict mode (medical/AV actuation): expiry_ms set to 0 or timer
//     bypassed entirely — FPT required before any execution proceeds
//   - The expiry_ms value is operator-configured at deployment.
//     It must not be configurable at runtime after system initialization.
//
// Post-expiry FPT rejection:
//   When expiry_signal is HIGH, any arriving FPT must be rejected.
//   The fpt_arrived input should not be wired directly from the FPT
//   intake — an interlock must check that expiry_signal is LOW before
//   treating fpt_arrived as valid. See PPT_Lifecycle.md Phase 4.
//
// Software isolation:
//   No software-accessible register may write to expiry_ms after the
//   system has been initialized. expiry_ms should be loaded from a
//   hardware-protected configuration store (OTP or HSM-signed config)
//   at boot and held in a read-only register thereafter.
//
// TMR recommendation for safety-critical deployments:
//   Instantiate three countdown_timer_clock modules with independent
//   clocks (if available) and majority-vote their expiry_signal outputs.
//   A single SEU that flips the expiry_signal register in one instance
//   will be overridden by the other two.
// =============================================================================
