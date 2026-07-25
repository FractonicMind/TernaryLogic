# HSM Signing Interface
### Ternary Logic — Dual-Lane Latency Architecture | 03_Cryptographic_Pipeline
**Author:** Lev Goukassian | FractonicMind  
**Parent directory:** `PPT/03_Cryptographic_Pipeline/`

---

## Overview

This document specifies the interface between TL's PPT hardware pipeline and the Hardware Security Module (HSM) that performs the Stage 3 cryptographic signing operation. The HSM is the element that produces the PPT's unforgeable authorization token — the ECDSA P-256 (or post-quantum) signature over the SHA-256 digest and Merkle root that the C-element gate validates.

The HSM is the most latency-significant stage in the pipeline (~5–10 ms warm path) and the single element whose compromise would defeat TL's entire authorization chain. Both facts govern this interface's design.

---

## HSM Role in the Pipeline

```
Stage 1 output: sha256_digest [255:0]       ─┐
Stage 2 output: merkle_root   [255:0]        ├─► HSM signing input
PPTHeader:      issued_at, expiry_bound       │   (canonical serialization)
PPTPayload:     operation_id, nonce, ...      │
PPTAudit:       merkle_root, leaf_set_hash  ─┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  FIPS 140-3 L3  │
                                    │      HSM        │
                                    │  ECDSA P-256    │
                                    │  (or Dilithium) │
                                    └────────┬────────┘
                                             │
                                             ▼
                              PPTSignature.signature_bytes
                              (64 bytes ECDSA / 2420 bytes Dilithium)
                                             │
                                             ▼
                              ───────────────────────────────
                              PPT is complete and signed.
                              Passed to C-element ppt_valid input.
```

---

## HSM Requirements

### Certification Baseline

**Mandatory:** FIPS 140-3 Level 3 certification (NIST CMVP validated).

FIPS 140-3 Level 3 provides:
- Physical tamper evidence and resistance
- Identity-based authentication before key use
- Demonstrated resistance to non-invasive attacks (timing side channels)
- Key zeroization on tamper detection

**Recommended for high-consequence domains** (financial market infrastructure, government, defense): FIPS 140-3 Level 4, which additionally requires:
- Environmental failure protection and testing
- Resistance to fault injection

**Validated HSM options** (as of TL specification date — verify current CMVP certificate status before procurement):
- Thales Luna Network HSM 7 (PCIe and Network variants)
- Entrust nShield 5 (Connect XC, Solo XC)
- Utimaco CryptoServer CP5 / Se-Series
- AWS CloudHSM (FIPS 140-2 Level 3 — evaluate against current FIPS 140-3 transition)
- Azure Dedicated HSM (Thales Luna 7 hosted)

**Disqualified for the signing critical path:**
- Discrete TPM 2.0: ECDSA signing latency in the tens of milliseconds exceeds TL's budget
- Software HSM (SoftHSM2): no hardware key protection; fails TL's hardware-constraint requirement
- Smart cards and USB tokens: insufficient throughput

---

## Signing Algorithm Specification

### Current Deployment: ECDSA P-256 + SHA-256

- **Curve:** NIST P-256 (secp256r1)
- **Hash:** SHA-256 (digest from Stage 1 already computed — HSM signs the digest directly)
- **Signature encoding:** DER-encoded ASN.1 or raw R||S (64 bytes) — operator-configured
- **FIPS reference:** NIST FIPS 186-5 (Digital Signature Standard)
- **Key size:** 256-bit private key, 65-byte uncompressed public key (04 || X || Y)
- **Classical security:** ~128-bit equivalent
- **Quantum security:** ~64-bit equivalent (insufficient for post-quantum adversary)

**Algorithm field in PPTSignature:** `0x01`

### Post-Quantum Migration: CRYSTALS-Dilithium (FIPS 204)

- **Algorithm:** ML-DSA-65 (CRYSTALS-Dilithium security level 3 — 128-bit quantum security)
- **Signature size:** 3,309 bytes (ML-DSA-65) — note: larger than initially estimated
- **Public key size:** 1,952 bytes
- **FIPS reference:** NIST FIPS 204 (finalized August 2024)
- **Signing latency:** Estimated 2–8 ms on hardware-accelerated HSM (vendor-dependent) [Engineering Estimate]
- **Algorithm field in PPTSignature:** `0x02`

Both algorithms must be supported by HSM firmware and by FPT verification infrastructure during the migration transition period. An HSM that supports only ECDSA P-256 is not post-quantum ready.

---

## Interface Specification

### Physical Connection

For latency-sensitive deployments (sub-50 ms PPT target):

**PCIe-attached HSM (preferred):**
- Eliminates network round-trip latency
- Signing latency governed by HSM hardware speed alone (~1–5 ms for ECDSA P-256)
- Examples: Thales Luna PCIe HSM 7, Entrust nShield Solo XC

**Network-attached HSM (acceptable with constraints):**
- Adds network RTT (typically 1–5 ms on local LAN)
- Total signing contribution: ~5–10 ms (hardware ~1–5 ms + network ~1–5 ms)
- Acceptable for warm-path 50 ms budget with margin
- Unacceptable if network path has >10 ms RTT at p99

**Cloud HSM (acceptable — weaker instantiation tier):**
- AWS CloudHSM: ~1–3 ms additional network latency over co-located compute
- Azure Dedicated HSM: similar characteristics
- Cloud HSM deployments are classified as Tier 2 (software-policy-on-hardware) because the HSM's physical security is delegated to the cloud provider

### Software Interface

TL uses PKCS#11 (Cryptoki) as the standard HSM interface. All major FIPS-certified HSMs support PKCS#11 v2.40 or later.

**Key PKCS#11 operations used:**

```c
// Session management (warm path: session pre-established at startup)
CK_RV rv = C_OpenSession(slot_id, CKF_SERIAL_SESSION, NULL, NULL, &session);

// Signing (per-PPT operation — this is the latency-critical path)
CK_MECHANISM mechanism = { CKM_ECDSA, NULL, 0 };  // ECDSA, hash pre-computed
rv = C_SignInit(session, &mechanism, private_key_handle);
rv = C_Sign(session, digest, 32, signature_buf, &sig_len);

// Post-quantum (Dilithium, when HSM firmware supports CKM_DILITHIUM)
CK_MECHANISM pq_mechanism = { CKM_DILITHIUM, NULL, 0 };
rv = C_SignInit(session, &pq_mechanism, dilithium_key_handle);
rv = C_Sign(session, digest, 32, signature_buf, &sig_len);
```

**Session pre-warming (mandatory startup procedure):**

Cold HSM sessions add session establishment overhead (~10–50 ms) to the first signing operation. This creates a cold-path p99 that can exceed TL's 50 ms specification.

Mandatory startup procedure:
1. At system initialization, establish HSM session and authenticate
2. Load signing key handle into session (do not re-load per PPT)
3. Issue one warm-up signing operation (discarded) to prime HSM key cache
4. Declare system ready for Lane 1 operations

The warm-up operation must complete before the system accepts any authorization requests. The warm-up is a startup transient and is excluded from the SLA.

### Signing Input Preparation

The HSM signs the canonical serialization of PPTHeader + PPTPayload + PPTAudit. The serialization format is defined in `01_Architecture_Specs/PPT_Token_Schema.md`.

The Stage 1 SHA-256 digest covers the PPTPayload only (the operation-specific content). The HSM signs the full canonical serialization — including the Merkle root and audit metadata — ensuring that the signature binds the PPT to its complete audit context, not just to the operation parameters.

```
HSM signing input (bytes):
  [PPTHeader — 29 bytes]
  [PPTPayload — ~115 bytes]
  [PPTAudit — 77 bytes]
  ─────────────────────────
  Total: ~221 bytes (fits within one PKCS#11 C_Sign call)
```

---

## Latency Characterization

### Warm-Path Latency (Operational Steady State)

| Component | Min | Mean | p99 | Classification |
|---|---|---|---|---|
| PCIe HSM hardware signing (ECDSA P-256) | ~0.5 ms | ~1–2 ms | ~3 ms | [Engineering Estimate] |
| Network-attached HSM (LAN RTT + signing) | ~1 ms | ~5 ms | ~10 ms | [Engineering Estimate] |
| PKCS#11 library overhead | ~0.1 ms | ~0.2 ms | ~0.5 ms | [Engineering Estimate] |
| **Total Stage 3 (PCIe, warm path)** | **~0.6 ms** | **~1–2 ms** | **~3.5 ms** | **[Engineering Estimate]** |
| **Total Stage 3 (network, warm path)** | **~1.1 ms** | **~5 ms** | **~10 ms** | **[Engineering Estimate]** |

**Verification note:** These figures are derived from published HSM throughput specifications and standard network latency estimates. Direct measurement under operational load is required before elevating to [Demonstrated]. This is identified as Future Work FW1 in the publication package.

### Cold-Path Latency (First Issuance / Session Startup)

| Component | Additional latency | Notes |
|---|---|---|
| Session establishment | ~10–50 ms | C_OpenSession + authentication |
| Key loading | ~5–20 ms | C_FindObjects + key handle resolution |
| First signing (cache cold) | ~2–5× warm signing | Key cache miss |
| **Total cold path overhead** | **~20–80 ms** | **Startup transient only** |

Cold-path p99 is the primary reason TL's 50 ms SLA applies to warm-path steady-state only. Mandatory session pre-warming eliminates the cold-path overhead from the operational SLA.

---

## Throughput and Scalability

### Per-Module Throughput Ceiling

| HSM Model | Signing algorithm | Throughput | PPT capacity | Classification |
|---|---|---|---|---|
| Thales Luna Network HSM 7 | ECDSA P-256 / RSA-2048 | ~10,000 RSA ops/s; ~20,000 ECC ops/s | ~10,000–20,000 PPT/s | [Demonstrated — vendor spec] |
| Utimaco Se-Series | RSA-2048 | ~40,000 ops/s | ~40,000 PPT/s | [Demonstrated — vendor spec] |
| Utimaco CSe-Series | RSA-2048 | ~5,000 ops/s | ~5,000 PPT/s | [Demonstrated — vendor spec] |
| Entrust nShield Connect XC | ECDSA P-256 | ~8,600 sig/s | ~8,600 PPT/s | [Engineering Estimate] |
| AWS CloudHSM | RSA-2048 | **~262 sig/s (measured)** | ~262 PPT/s | [Demonstrated — measured under load] |
| Azure Dedicated HSM (Thales Luna 7) | RSA-2048 | ~10,000 ops/s | ~10,000 PPT/s | [Engineering Estimate] |

**Critical observation:** The gap between vendor-specified throughput and measured cloud HSM throughput is significant. AWS CloudHSM achieves ~262 signatures/second under real-world conditions — approximately 38× slower than Thales Luna 7's vendor-specified maximum. Factors include network virtualization overhead, API layer latency, and HSM resource contention in multi-tenant environments. Cloud HSM deployments must be capacity-planned against measured figures, not vendor maximums.

**Recommended operational ceiling:** 80% of measured throughput to maintain p99 latency within the 50 ms specification. For on-premises Utimaco Se-Series: ~32,000 PPTs/s. For cloud HSM: ~210 PPTs/s.

**Note:** Published throughput figures are maximum values under ideal conditions. Actual throughput under mixed-operation load (key management, audit logging, session management) will be lower. Operational derating of 20–40% from published maximums is prudent for on-premises capacity planning. [Engineering Estimate]

### Horizontal Scaling

TL's architecture supports horizontal HSM scaling:
- Multiple HSMs in an active-active pool, load-balanced by the PKCS#11 layer
- Each HSM holds a copy of the signing key (requires multi-party key ceremony for key distribution)
- Linear throughput scaling with HSM count: N HSMs provide ~N× throughput
- Failover: if one HSM fails, remaining pool continues. System enters degraded mode if pool capacity drops below minimum threshold

### Queue Saturation Behavior

When HSM signing capacity is saturated:

1. **Stall mode** (Fast Lane FIFO > 80% capacity): Lane 1 deasserts RequestReady, stops accepting new authorization requests. In-flight PPT computations continue to completion.

2. **Reject mode** (stall persists > 100 ms): New authorization requests receive immediate NAK. In-flight operations continue.

TL's saturation response is queue-then-reject. It never silently drops requests or returns a false positive authorization.

---

## Security Requirements

### Key Management

**Key generation:** HSM signing keys must be generated inside the HSM using the HSM's certified RNG. No key material ever exists in plaintext outside the HSM boundary.

**Key ceremony:** For high-consequence deployments, the signing key should be generated under multi-party control (M-of-N operators required for key ceremony). This prevents any single operator from unilaterally controlling the signing key.

**Key backup:** HSM key backup must use encrypted key export under a wrapping key held by a second HSM or a split-knowledge key custodian process. Plaintext backup is prohibited.

**Key rotation:** Signing keys should be rotated periodically (recommended: annually for ECDSA P-256; quarterly during PQC migration). Key rotation requires updating the public_key_id registry and supporting validation of PPTs signed under prior keys for the retention period.

### HSM Compromise Detection

If the HSM is compromised, it can produce valid-looking PPTs for unauthorized operations, defeating TL's authorization chain. The C-element provides no residual protection — it enforces that a valid PPT exists, not that the PPT was generated by an uncompromised HSM. This is TL's most severe single-point security failure.

**The critical architectural implication:** TL's physical gate guarantee is conditioned on HSM software and firmware integrity. A Byzantine-faulty HSM converts TL's physical gate into an authorized-execution pathway for any attacker who controls HSM behavior. This is not a minor operational risk — it is an architectural dependency that must be addressed at the specification level.

Required mitigations:

**Threshold cryptography — architectural requirement for high-consequence deployments:** A valid PPT must require signatures from M-of-N independent HSMs (threshold ECDSA or equivalent). No single compromised HSM can forge a valid PPT. This is not a best practice — it is an architectural requirement for any deployment where HSM compromise is a credible threat model. Single-HSM deployments must be explicitly labeled as operating with elevated single-point-of-failure risk. [Engineering Estimate — threshold ECDSA protocols are established; TL integration is Theoretical]

**Anomaly detection:** Monitor HSM signing rate, operation type distribution, and session patterns. Alert on anomalous patterns (e.g., signing rate spike, unexpected operation types, after-hours sessions). Establish baseline behavioral profiles per HSM instance.

**Hardware attestation chaining:** Each HSM should produce a periodic attestation report (signed by an HSM-internal attestation key) confirming firmware version, configuration hash, and operational status. Attestation reports are audited for anomalies.

### HSM High-Availability Failover Under Governor Independence

Under Governor Independence, multiple PPTs may be in-flight simultaneously when an HSM failure occurs. TL's HA protocol must specify behavior for this scenario.

**Thales Luna HA failover behavior** [Demonstrated — Thales documentation]:
- Detects HSM failure and automatically establishes a new session on a functioning HA group member
- Pending signing operations are transparently rescheduled on remaining member partitions
- Protocol timeout: approximately 10 seconds before failover completes
- If signing keys are replicated across all HA members, in-flight PPT validity is maintained during failover

**TL-specific failover requirements:**

For in-flight PPTs at the moment of HSM failure:
- PPTs whose signing operations were completed before failure: valid, proceed normally through `provisionalExpiry` and FPT
- PPTs whose signing operations were in-progress at failure: must be resubmitted to the HA secondary; `provisionalExpiry` timer has not yet started for these
- The HA switchover latency (~10 seconds) must be accounted for in `provisionalExpiry` configuration — if the window is shorter than the failover time, all in-flight operations will expire during failover

**Recommendation:** For deployments using Governor Independence pipelining, `provisionalExpiry` should be set to at least 3× the HSM HA failover timeout to ensure that a primary HSM failure does not cascade into mass concurrent expiry of all in-flight PPTs.

**Current specification status:** [Gap] — TL spec does not currently define HSM failover behavior for concurrent provisional windows. This is identified as a required specification addition before production deployment.

---

## Integration Checklist

Before declaring the HSM signing interface operational:

- [ ] HSM is FIPS 140-3 Level 3 certified (verify NIST CMVP certificate number)
- [ ] Signing key generated inside HSM under multi-party ceremony
- [ ] PKCS#11 session pre-warming implemented and tested
- [ ] Cold-path first-signing latency measured and documented
- [ ] Warm-path p99 measured at 50%, 80%, and 95% HSM utilization
- [ ] FIPS 180-4 KAT validation completed for SHA-256 (Stage 1)
- [ ] Anomaly detection configured and tested
- [ ] Key backup and recovery procedure tested
- [ ] Post-quantum algorithm field (Dilithium) tested in staging environment
- [ ] HSM failover to pool secondary tested under load — including behavior with N concurrent in-flight PPTs
- [ ] Threshold cryptography (M-of-N) evaluated for deployment threat model; single-HSM deployments documented with explicit PoF risk acknowledgment
- [ ] `provisionalExpiry` bound confirmed to be ≥ 3× HSM HA failover timeout for Governor Independence deployments

---

## Related Files

| File | Relationship |
|---|---|
| `PPT_Token_Schema.md` | PPTSignature section — what the HSM signs and how it is encoded |
| `SHA256_Hardware_Accel.v` | Produces the digest that the HSM signs |
| `Merkle_Precomputation.v` | Produces the Merkle root included in the signed payload |
| `02_Hardware_Primitives/C_Element_Interlock.v` | Receives HSM signature validity as ppt_valid input |
| `01_Architecture_Specs/Dual_Lane_Governance.md` | FPT routing table — HSM session continuity during failover |
| `05_Research/Session-2_Deep_Research.md` | Q6 security analysis — HSM compromise treatment |
| `PPT_Governor_Independence_Research.md` | Governor Independence research — measured throughput figures, Thales HA failover behavior |
| `06_Publication/PPT_Paper_Draft.md` | Section 7.3 — HSM compromise architectural dependency |

---

*Ternary Logic — FractonicMind/TernaryLogic/PPT/03_Cryptographic_Pipeline*
