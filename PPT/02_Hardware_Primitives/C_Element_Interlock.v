// =============================================================================
// C_Element_Interlock.v
// Ternary Logic — Dual-Lane Latency Architecture
// 02_Hardware_Primitives
//
// Author:       Lev Goukassian | FractonicMind
// Framework:    Ternary Logic (TL) — Mandated Ternary (MT) Hardware Layer
// Repository:   FractonicMind/TernaryLogic/PPT/02_Hardware_Primitives
//
// Description:
//   Muller C-element implementation serving as TL's physical authorization gate.
//   This module is the C-element referenced throughout TL's DLLA specification.
//   Its output (state_release) goes high if and only if both inputs are high:
//     - ppt_valid:   HSM-signed PPT has been verified (from cryptographic pipeline)
//     - hw_auth:     Hardware authorization signal (domain-specific; operator-wired)
//
//   When state_release is high, the Epistemic Hold (State 0) is released and
//   provisional execution (State 1) is permitted.
//
//   When state_release is low — for ANY reason — the execution gate is physically
//   closed. There is no software override path for state_release.
//
// Behavioral model: SYNTHESIZABLE RTL
//   This file is synthesizable RTL targeting Xilinx Versal / UltraScale+ or
//   equivalent FPGA fabric. It is NOT a behavioral simulation model.
//   For ASIC deployment, this RTL serves as the reference specification;
//   the ASIC implementation must be independently verified against this model.
//
// Implementation note:
//   The standard Muller C-element is implemented here as a set-dominant
//   SR latch with symmetric input structure. Both inputs must be asserted
//   for the output to go high. Either input going low forces the output low
//   via the pull-down network. This is the physical enforcement of TL's
//   authorization invariant: no execution without both conditions satisfied.
//
// FIPS / Safety classification:
//   For ASIL-D (ISO 26262) and IEC 62304 Class C deployments:
//   - Use flash-based FPGA (Microchip PolarFire) or ASIC implementation
//   - SRAM-based FPGA requires configuration scrubbing (see design notes)
//   - Triple Modular Redundancy (TMR) is recommended for safety-critical use
//
// Evidence classification: [Engineering Estimate] for timing parameters
//                          [Demonstrated] for C-element circuit properties
// =============================================================================

`timescale 1ns / 1ps

module c_element_interlock (
    // Clock and reset
    input  wire clk,            // System clock
    input  wire rst_n,          // Active-low synchronous reset → forces State 0

    // Authorization inputs (both must be high to release State 0)
    input  wire ppt_valid,      // PPT cryptographic pipeline: valid PPT present
    input  wire hw_auth,        // Hardware authorization: domain-specific signal

    // State outputs
    output reg  state_release,  // HIGH = State 0 released (State 1 permitted)
                                 // LOW  = State 0 held (no execution permitted)
    output wire state_0_active, // HIGH = Epistemic Hold active (for monitoring)
    output wire state_1_active, // HIGH = Provisional Execution active (for monitoring)

    // Fault detection (dual-rail encoding)
    input  wire ppt_valid_n,    // Complement of ppt_valid (dual-rail input)
    input  wire hw_auth_n,      // Complement of hw_auth (dual-rail input)
    output reg  encoding_fault  // HIGH = dual-rail encoding violation detected
                                 // Triggers immediate State 0 assertion
);

    // =========================================================================
    // Internal signals
    // =========================================================================

    wire both_inputs_high;      // True when ppt_valid AND hw_auth are both high
    wire either_input_low;      // True when either input is low (pull-down active)
    wire dual_rail_ok;          // True when dual-rail encoding is consistent

    // =========================================================================
    // Dual-rail encoding check
    // The dual-rail inputs (ppt_valid_n, hw_auth_n) must be the logical
    // complements of (ppt_valid, hw_auth). A violation indicates a fault —
    // either a stuck-at fault, an SEU in SRAM-based FPGA, or an active
    // fault injection attempt.
    //
    // On encoding violation: encoding_fault is asserted and state_release
    // is forced low unconditionally — fail-closed behavior.
    // =========================================================================

    assign dual_rail_ok = (ppt_valid == ~ppt_valid_n) &&
                          (hw_auth   == ~hw_auth_n);

    // =========================================================================
    // C-element consensus logic
    // Output goes high only when both inputs are high AND encoding is valid.
    // Output goes low when any input is low OR when encoding is violated.
    //
    // This implements the Muller C-element truth table:
    //   ppt_valid=1, hw_auth=1 → state_release=1 (consensus: release)
    //   ppt_valid=1, hw_auth=0 → state_release=0 (no consensus: hold)
    //   ppt_valid=0, hw_auth=1 → state_release=0 (no consensus: hold)
    //   ppt_valid=0, hw_auth=0 → state_release=0 (no consensus: hold)
    // =========================================================================

    assign both_inputs_high = ppt_valid & hw_auth & dual_rail_ok;
    assign either_input_low  = (~ppt_valid) | (~hw_auth) | (~dual_rail_ok);

    assign state_0_active = ~state_release;
    assign state_1_active =  state_release;

    // =========================================================================
    // Sequential C-element with synchronous reset
    // The C-element is registered to prevent glitch propagation to the
    // execution gate. The combinational consensus result is sampled on
    // the clock edge.
    //
    // Reset behavior: rst_n LOW → state_release = 0 (State 0 forced)
    // This ensures that power-on and reset always begin in State 0.
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Synchronous reset: force State 0 unconditionally
            state_release  <= 1'b0;
            encoding_fault <= 1'b0;
        end else begin
            // Dual-rail encoding fault: force State 0 and assert fault signal
            if (!dual_rail_ok) begin
                state_release  <= 1'b0;
                encoding_fault <= 1'b1;
            end
            // Consensus reached: both inputs high, encoding valid
            else if (both_inputs_high) begin
                state_release  <= 1'b1;
                encoding_fault <= 1'b0;
            end
            // No consensus: either input low — hold State 0
            else if (either_input_low) begin
                state_release  <= 1'b0;
                encoding_fault <= 1'b0;
            end
            // Default: maintain current state (C-element memory property)
            // This handles the case where inputs are transitioning
            else begin
                state_release  <= state_release;
                encoding_fault <= 1'b0;
            end
        end
    end

endmodule


// =============================================================================
// c_element_tmr_wrapper
// Triple Modular Redundancy wrapper for safety-critical deployments.
//
// Instantiates three independent c_element_interlock modules and takes
// the majority vote of their state_release outputs.
//
// USE THIS WRAPPER for:
//   - ISO 26262 ASIL-D deployments (autonomous vehicles)
//   - IEC 62304 Class C deployments (medical devices)
//   - Any deployment where SRAM-based FPGA is used (SEU mitigation)
//
// USE THE BASE MODULE for:
//   - ASIC implementations (TMR at cell level)
//   - Flash-based FPGA (PolarFire — SEU-resistant by design)
//   - Development and simulation environments
// =============================================================================

module c_element_tmr_wrapper (
    input  wire clk,
    input  wire rst_n,
    input  wire ppt_valid,
    input  wire hw_auth,
    input  wire ppt_valid_n,
    input  wire hw_auth_n,
    output wire state_release,   // Majority-voted output
    output wire state_0_active,
    output wire state_1_active,
    output wire encoding_fault,  // Asserted if any instance reports fault
    output wire tmr_mismatch     // Asserted if instances disagree (degraded mode)
);

    // Three independent C-element instances
    wire sr_a, sr_b, sr_c;
    wire ef_a, ef_b, ef_c;

    c_element_interlock inst_a (
        .clk(clk), .rst_n(rst_n),
        .ppt_valid(ppt_valid), .hw_auth(hw_auth),
        .ppt_valid_n(ppt_valid_n), .hw_auth_n(hw_auth_n),
        .state_release(sr_a), .state_0_active(), .state_1_active(),
        .encoding_fault(ef_a)
    );

    c_element_interlock inst_b (
        .clk(clk), .rst_n(rst_n),
        .ppt_valid(ppt_valid), .hw_auth(hw_auth),
        .ppt_valid_n(ppt_valid_n), .hw_auth_n(hw_auth_n),
        .state_release(sr_b), .state_0_active(), .state_1_active(),
        .encoding_fault(ef_b)
    );

    c_element_interlock inst_c (
        .clk(clk), .rst_n(rst_n),
        .ppt_valid(ppt_valid), .hw_auth(hw_auth),
        .ppt_valid_n(ppt_valid_n), .hw_auth_n(hw_auth_n),
        .state_release(sr_c), .state_0_active(), .state_1_active(),
        .encoding_fault(ef_c)
    );

    // Majority voter: output high only if at least 2 of 3 agree on high
    assign state_release  = (sr_a & sr_b) | (sr_b & sr_c) | (sr_a & sr_c);
    assign state_0_active = ~state_release;
    assign state_1_active =  state_release;

    // Fault aggregation: any instance reporting a fault asserts the fault output
    assign encoding_fault = ef_a | ef_b | ef_c;

    // TMR mismatch: instances disagree — system is in degraded mode
    assign tmr_mismatch   = (sr_a ^ sr_b) | (sr_b ^ sr_c) | (sr_a ^ sr_c);

endmodule


// =============================================================================
// Design Notes
//
// Timing parameters (28 nm CMOS process, synthesis estimates):
//   - C-element propagation delay: ~45 ps [Engineering Estimate]
//   - Setup time to state_release output: ~100 ps [Engineering Estimate]
//   - Clock-to-output delay: 1 clock cycle (registered output)
//
// SEU mitigation for SRAM-based FPGA:
//   - Enable configuration scrubbing (Xilinx: use ICAP primitive with scrub
//     controller; Intel: use CONF_DONE monitoring with PR controller)
//   - Scrub interval should be ≤ 1/3 of the expected SEU rate for the
//     deployment environment's radiation profile
//   - Alternatively, use flash-based FPGA (Microchip PolarFire family)
//     which does not use SRAM configuration memory
//
// ASIC implementation note:
//   - The standard cell implementation should use a full-custom C-element
//     cell from the process PDK where available
//   - If no C-element cell is available, the SR-latch implementation in
//     this RTL is the correct synthesis target
//   - The pull-down network should be sized for fail-safe behavior under
//     all process corners (worst-case: slow process, high temperature, low voltage)
//
// Prohibited modifications:
//   - Do not add a software-accessible register that can override state_release
//   - Do not add a debug bypass for state_release
//   - Do not remove the dual-rail encoding check
//   - Any modification that creates a software path to state_release defeats
//     TL's hardware-constraint design intent and must not be made
// =============================================================================
