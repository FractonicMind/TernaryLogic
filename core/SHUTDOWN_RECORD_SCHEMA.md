# Shutdown Record Schema

## "Ternary Logic" (TL) Constitutional Freeze Evidence Record

**Framework:** "Ternary Logic" (TL) by Lev Goukassian
**ORCID:** 0009-0006-5966-1243
**Repository:** FractonicMind/TernaryLogic
**Spec Version:** 1.0.0-tl-monograph-2026
**Schema Draft:** JSON Schema Draft 2020-12
**Context:** Constitutional Forensics and Financial Governance

---

## Section 1: Purpose

The Shutdown Record is the immutable constitutional evidence artifact generated when a TL deployment transitions to the FREEZE state (S3) following a SHUTDOWN_TRIGGER event. It is committed to the Immutable Ledger before any freeze action propagates to the actuation layer. This commitment is mandatory. The NL=NA invariant applies to the freeze itself: the record of the freeze must exist before the freeze executes.

The Shutdown Record is admissible as forensic accounting evidence in legal and regulatory proceedings. Its cryptographic structure, conforming to `tl_schema.json` field conventions and signed with Ed25519 or ES256, provides tamper-evident proof of the conditions that caused the freeze.

---

## Section 2: Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://fractonicmind.github.io/TernaryLogic/core/schema/shutdown-record/v1.0.0",
  "title": "TL Shutdown Evidence Record",
  "description": "Immutable constitutional freeze evidence artifact. Committed to Immutable Ledger before freeze propagates to actuation layer. NL=NA applies to the freeze itself.",
  "type": "object",
  "required": [
    "recordId",
    "timestamp",
    "triggerId",
    "triggerSeries",
    "triggerName",
    "triggerContext",
    "finalState",
    "finalStateLabel",
    "lastDecisionId",
    "lastLogHash",
    "merkleRootAtFreeze",
    "pufAttestation",
    "architectureMode",
    "signatureAlgorithm",
    "signatureValue",
    "signerKeyId",
    "governanceLaneConfirmed",
    "pillarStatuses"
  ],
  "properties": {

    "recordId": {
      "type": "string",
      "format": "uuid",
      "description": "UUID v4 uniquely identifying this Shutdown Record."
    },

    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of freeze initiation. From hardware-protected clock in MT deployments; NTP-synchronized system clock in Architecture B."
    },

    "triggerId": {
      "type": "string",
      "description": "Trigger identifier from SHUTDOWN_TRIGGERS catalog. Examples: H-001, C-003, D-001.",
      "pattern": "^[HCD]-[0-9]{3}$"
    },

    "triggerSeries": {
      "type": "string",
      "enum": ["H", "C", "D"],
      "description": "H: Hardware Integrity. C: Constitutional Financial Violation. D: Cryptographic and Data Integrity."
    },

    "triggerName": {
      "type": "string",
      "description": "Human-readable name of the trigger from SHUTDOWN_TRIGGERS catalog. Example: Solvency Illusion, Hold Violation, Decision Log Bypass."
    },

    "triggerContext": {
      "type": "object",
      "description": "Domain-specific context for the trigger event.",
      "required": ["description", "pillarImplicated"],
      "properties": {
        "description": {
          "type": "string",
          "minLength": 10,
          "description": "Human-readable description of the specific condition that triggered the freeze."
        },
        "pillarImplicated": {
          "type": "string",
          "enum": [
            "EpistemicHold",
            "ImmutableLedger",
            "GoukassianPrinciple",
            "DecisionLogs",
            "EconomicRightsAndTransparencyMandate",
            "SustainableCapitalAllocationMandate",
            "HybridShield",
            "Anchors"
          ],
          "description": "The canonical TL Pillar implicated in the trigger condition."
        },
        "financialContext": {
          "type": "object",
          "description": "Populated for C-series triggers involving financial asset violations.",
          "properties": {
            "assetId": { "type": "string" },
            "claimedValue": { "type": "number" },
            "missingProof": {
              "type": "string",
              "description": "The specific Merkle root or oracle proof that failed verification."
            },
            "anchorOracleQueried": { "type": "string" },
            "replayAttackDetected": { "type": "boolean" }
          },
          "unevaluatedProperties": false
        },
        "hardwareContext": {
          "type": "object",
          "description": "Populated for H-series triggers involving hardware integrity violations.",
          "properties": {
            "railVoltageDeviation": { "type": "number", "description": "Observed voltage deviation as percentage." },
            "clockCyclesExceeded": { "type": "integer" },
            "tamperMeshContinuityLost": { "type": "boolean" },
            "hsmHeartbeatTimeoutMs": { "type": "integer" },
            "windowComparatorReading": {
              "type": "object",
              "properties": {
                "readingAvailable": { "type": "boolean" },
                "resistanceRangeOhm": {
                  "type": "object",
                  "properties": {
                    "minOhm": { "type": "number" },
                    "maxOhm": { "type": "number" }
                  },
                  "unevaluatedProperties": false
                },
                "softwareEnforcementActive": { "type": "boolean" }
              },
              "unevaluatedProperties": false
            }
          },
          "unevaluatedProperties": false
        },
        "cryptographicContext": {
          "type": "object",
          "description": "Populated for D-series triggers involving cryptographic integrity violations.",
          "properties": {
            "anchorChainBreakDetected": { "type": "boolean" },
            "previousBlockHash": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$",
              "description": "SHA-256 hash of previous block in Decision Log."
            },
            "storedReferenceHash": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$",
              "description": "Stored reference hash that did not match previousBlockHash."
            },
            "oracleDeviationPercent": { "type": "number" },
            "clockReversalMs": { "type": "integer", "description": "Milliseconds of backward clock movement detected." }
          },
          "unevaluatedProperties": false
        }
      },
      "unevaluatedProperties": false
    },

    "finalState": {
      "type": "integer",
      "enum": [-1, 0],
      "description": "The TL state at freeze. -1 (Refuse) for FATAL triggers. 0 (Epistemic Hold) for HIGH triggers requiring human review before full freeze."
    },

    "finalStateLabel": {
      "type": "string",
      "enum": ["Refuse", "EpistemicHold"],
      "description": "Human-readable label for finalState. Halt is not a valid label."
    },

    "lastDecisionId": {
      "type": "string",
      "format": "uuid",
      "description": "UUID v4 of the last valid governance decision before freeze. Ensures no decisions are orphaned in the freeze."
    },

    "lastLogHash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the last valid TGLF log entry before freeze. Ensures no log entries are lost in the freeze boundary."
    },

    "merkleRootAtFreeze": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 Merkle accumulator root at the moment of freeze. All governance actions after this root are held pending forensic audit."
    },

    "pufAttestation": {
      "type": "string",
      "description": "PUF binding attestation. Architecture B deployments MUST use sentinel value NULL_PUF_DEPLOYMENT. MT hardware deployments carry SHA3-256(K_PUF || device_serial_OTP || log_session_nonce)."
    },

    "architectureMode": {
      "type": "string",
      "enum": ["ARCHITECTURE_B", "FULL_PUF"],
      "description": "Hardware enforcement posture at time of freeze."
    },

    "signatureAlgorithm": {
      "type": "string",
      "enum": ["ES256", "Ed25519"],
      "default": "ES256",
      "description": "Signature algorithm used for this record. PQC slots SLH-DSA-SHAKE-128s and ML-KEM-1024 are FUTURE-reserved. SHIPPING MUST NOT emit PQC values."
    },

    "signatureValue": {
      "type": "string",
      "contentEncoding": "base64url",
      "description": "Cryptographic signature over the canonical serialization of this record. Key held in HSM; never exposed in plaintext outside the hardware trust boundary."
    },

    "signerKeyId": {
      "type": "string",
      "description": "Identifier of the HSM-held signing key used for this record."
    },

    "governanceLaneConfirmed": {
      "type": "boolean",
      "description": "True if the Governance Lane confirmed log commitment before freeze propagated. False if freeze was initiated by hardware interrupt (H-series) before Governance Lane could confirm."
    },

    "pillarStatuses": {
      "type": "array",
      "minItems": 8,
      "maxItems": 8,
      "description": "Status of all Eight Pillars at the moment of freeze.",
      "items": {
        "type": "object",
        "required": ["pillarId", "status"],
        "properties": {
          "pillarId": {
            "type": "string",
            "enum": [
              "EpistemicHold",
              "ImmutableLedger",
              "GoukassianPrinciple",
              "DecisionLogs",
              "EconomicRightsAndTransparencyMandate",
              "SustainableCapitalAllocationMandate",
              "HybridShield",
              "Anchors"
            ]
          },
          "status": {
            "type": "string",
            "enum": ["ACTIVE", "DEGRADED", "SUSPENDED", "EPISTEMIC_HOLD_ACTIVE"]
          }
        },
        "unevaluatedProperties": false
      }
    },

    "regulatoryNotifications": {
      "type": "array",
      "description": "Regulatory bodies notified at freeze. Populated for C-005 Regulatory Bypass and other compliance-triggered freezes.",
      "items": {
        "type": "object",
        "required": ["regulatoryBody", "notifiedAt", "notificationHash"],
        "properties": {
          "regulatoryBody": { "type": "string" },
          "notifiedAt": { "type": "string", "format": "date-time" },
          "notificationHash": { "type": "string", "pattern": "^[0-9a-f]{64}$" }
        },
        "unevaluatedProperties": false
      }
    },

    "recoveryPath": {
      "type": "string",
      "enum": ["RECOVERY_AUDIT", "UNFREEZE_TOKEN_REQUIRED", "CONSTITUTIONAL_REVIEW"],
      "description": "The constitutional path required to exit the freeze state. RECOVERY_AUDIT: S4 forensic accounting mode. UNFREEZE_TOKEN_REQUIRED: multi-party token from governance required. CONSTITUTIONAL_REVIEW: Tri-Cameral governance required."
    }
  },
  "unevaluatedProperties": false
}
```

---

## Section 3: Admissibility and Legal Status

The Shutdown Record, once committed to the Immutable Ledger, is:

**Tamper-evident:** The SHA-256 `lastLogHash` and `merkleRootAtFreeze` fields cryptographically bind this record to the complete governance history preceding the freeze. Any modification after commitment produces a detectable hash mismatch.

**Non-repudiable:** The `signatureValue` is produced by a key held exclusively within the HSM hardware trust boundary. In Architecture B, this is the Thales Luna 7 HSM (FIPS 140-3 Level 3) or equivalent. The signing key never leaves the hardware boundary in plaintext.

**Forensically complete:** The `lastDecisionId` and `lastLogHash` fields ensure that no governance decisions are orphaned or lost at the freeze boundary. An auditor can reconstruct the complete governance history from system initialization through freeze using only the Immutable Ledger and this record.

**Admissible as forensic accounting evidence:** The Shutdown Record constitutes legal evidence of the conditions that caused the freeze. The entity controlling the authorization keys at the time of a C-003 (Solvency Illusion) or C-004 (Hold Violation) trigger assumes presumptive liability as documented in COMPLIANCE_ATTESTATION.md Section 8.

---

## Section 4: Trigger-to-Schema Mapping

| Trigger | Series | finalState | triggerContext Object Populated |
|---------|--------|------------|--------------------------------|
| H-001 Rail Voltage Deviation (Pos) | H | -1 (Refuse) | hardwareContext.railVoltageDeviation |
| H-002 Rail Voltage Deviation (Neg) | H | -1 (Refuse) | hardwareContext.railVoltageDeviation |
| H-003 Zero Plane Drift | H | -1 (Refuse) | hardwareContext.windowComparatorReading |
| H-007 Physical Tamper Mesh | H | -1 (Refuse) | hardwareContext.tamperMeshContinuityLost |
| H-008 Hardware Anchor Timeout | H | -1 (Refuse) | hardwareContext.hsmHeartbeatTimeoutMs |
| C-001 Decision Log Bypass | C | -1 (Refuse) | financialContext (null), pillarImplicated: ImmutableLedger |
| C-002 Provenance Gap (AML) | C | -1 (Refuse) | financialContext.missingProof |
| C-003 Solvency Illusion | C | -1 (Refuse) | financialContext.claimedValue, missingProof, anchorOracleQueried |
| C-004 Hold Violation | C | -1 (Refuse) | pillarImplicated: EpistemicHold |
| C-005 Regulatory Bypass | C | -1 (Refuse) | pillarImplicated: EconomicRightsAndTransparencyMandate; regulatoryNotifications populated |
| C-006 Flash Crash Resonance | C | 0 (Epistemic Hold) | financialContext, pillarImplicated: EpistemicHold |
| C-007 Double-Spend Detect | C | -1 (Refuse) | financialContext.assetId |
| D-001 Anchor Chain Break | D | -1 (Refuse) | cryptographicContext.previousBlockHash, storedReferenceHash |
| D-002 Oracle Deviation | D | 0 (Epistemic Hold) | cryptographicContext.oracleDeviationPercent |
| D-003 Time Travel Detect | D | -1 (Refuse) | cryptographicContext.clockReversalMs |
