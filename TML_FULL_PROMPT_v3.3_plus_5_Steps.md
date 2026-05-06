  
## THE FULL PROMPT (v3.3)

```markdown  
# DEEP RESEARCH PROMPT: TML Specification Architecture v3.3

## 0. SOURCE MATERIAL INJECTION  
**AUTHORITY HIERARCHY:** TML Constitutionalization Monograph (Sections 1–13) > This Prompt > Existing Repository Files.  
**INSTRUCTION:** Paste relevant excerpts of the monograph below, particularly Sections 1–2, 2.2, 2.3, 2.4, 8, 10, and 13. If the monograph is not provided, halt generation and request the exact sections referenced in this prompt. Do not infer, paraphrase, or hallucinate pillar definitions, state transitions, or compliance mappings.

---

## 1. YOUR MISSION  
You are a Principal Specification Architect. Your task is to produce a **canonical API specification package** for the **Ternary Moral Logic (TML)** framework. 

**CRITICAL CONSTRAINT:** You are writing **specifications and schemas**, not implementation code. You are defining the contract, not building the runtime. Do not generate Python modules, Solidity contracts, or deployment scripts. Generate OpenAPI 3.1, JSON Schema Draft 2020-12, and architectural markdown only.

## 2. PRIMARY SOURCE MATERIAL  
Base your entire output on the monograph. The canonical concepts are:

- **Triadic Logic Core:** States +1 (Proceed), 0 (Sacred Zero), -1 (Refuse)  
- **Binary-Ternary Parallel Architecture:** TML does not replace the binary inference engine. Binary Logic handles speed, pattern recognition, and raw statistical throughput. In parallel, the ternary logic operates as a **sovereign governance coprocessor**. The binary system proposes the action; the ternary system dictates whether that action physically crosses the threshold into execution. This parallel structure neutralizes the fatal industry objection that hardware governance destroys throughput.  
- **The Sacred Zero:** Not a null or error. An active governance state of mandatory hesitation. When triggered, the system initiates a **Sacred Pause** — halting external execution while activating internal logging and escalation protocols. The Sacred Pause is the operational workflow; Sacred Zero is the state.  
- **The Eight Pillars:**  
  1. Sacred Zero (The state of moral ambiguity; the Sacred Pause is the operational process triggered within this state)  
  2. Always Memory (Anti-Spoliation / Pre-Actuation Commit)  
  3. Goukassian Promise (Lantern, Signature, License)  
  4. Moral Trace Logs (TSLF — forensic schema)  
  5. Human Rights Mandate (UDHR/Geneva vector enforcement)  
  6. Earth Protection Mandate (Paris Agreement vector enforcement)  
  7. Hybrid Shield (6-Custodian distributed anchoring)  
  8. Public Blockchains (Merkle-Batched Anchoring)  
- **Dual-Lane Latency Architecture:**  
  - Lane 1: Inference Lane (Fast Path, <2ms, System 1) — proposes actions via binary logic  
  - Lane 2: Anchoring Lane (Governance Lane, <500ms, System 2) — verifies, logs, and issues Permission Tokens via ternary logic  
- **No Log = No Action:** The iron law. The inference engine is cryptographically decoupled from actuation. The binary lane may propose +1, but the ternary lane must produce a valid Permission Token before the actuation layer fires.  
- **Goukassian Vow (Monograph Section 1.5 — Triadic State Code):** The operational interface to the three logic states.  
  - "Pause when truth is uncertain" → **State 0 (Sacred Zero)**  
  - "Refuse when harm is clear" → **State -1 (Refuse)**  
  - "Proceed where truth is" → **State +1 (Proceed)**

**TERMINOLOGY ENFORCEMENT:** Use these exact canonical terms in all schemas and endpoint descriptions. Do not substitute, abbreviate, or alias them. If the monograph calls it "Sacred Zero," the API spec must call it `SacredZero`, not `PauseState`, `HOLD`, or `Timeout`.

**CANONICAL PILLAR IDENTIFIERS:** Use exactly these machine-readable identifiers for all `x-tml-pillar` annotations:

| **Pillar** | **Identifier** |  
|------------|----------------|  
| Pillar I | `SacredZero` |  
| Pillar II | `AlwaysMemory` |  
| Pillar III | `GoukassianPromise` |  
| Pillar IV | `MoralTraceLogs` |  
| Pillar V | `HumanRightsMandate` |  
| Pillar VI | `EarthProtectionMandate` |  
| Pillar VII | `HybridShield` |  
| Pillar VIII | `PublicBlockchains` |

**API NAMING CONVENTIONS:** Apply these rules consistently across all deliverables:  
- Schema names: `PascalCase` (e.g., `SacredZeroLog`, `PermissionToken`)  
- JSON properties: `camelCase` (e.g., `sacredZeroState`, `permissionToken`)  
- Enum values: `UPPER_SNAKE_CASE` (e.g., `SACRED_ZERO`, `PROCEED`, `REFUSE`)  
- State values: signed integers `+1`, `0`, `-1` with optional `state_label` string for human readability

## 3. SCOPE BOUNDARIES (HARD RULES)

### IN SCOPE — Specification Only  
- OpenAPI 3.1 specification documenting the runtime API surface  
- JSON Schemas for: Moral Trace Log (TSLF), Justification Object, State Envelope, Permission Token, Lantern Status, Signature Block, License Validation Request  
- Canonical markdown explaining the specification architecture  
- A "Constitutional Compliance Matrix" mapping every endpoint and schema to its monograph section and Pillar  
- A "Future / Blocked" appendix labeling aspirational features

### OUT OF SCOPE — Do Not Produce  
- Python, C++, Go, or Java implementation code  
- Solidity smart contract source code (ABI definitions and EIP-712 typed data schemas are allowed)  
- Dockerfiles, CI/CD configs, or deployment manifests  
- Operational SLOs, throughput curves, or stress-test configurations  
- TypeScript type stubs, Python type stubs, or interface definitions  
- Marketing or philosophical essays (the monograph already exists)  
- Full SDK reference documentation (the SDK public interfaces may be referenced but are not to be specified in this pass)

## 4. REPOSITORY CONTEXT  
The following directory tree is **informational back-context only**. Do not map it to API endpoints; design logical REST-style paths (e.g., `/decisions`, `/anchoring-logs`, `/audit/verifications`).

```  
api/  
  complete_api_reference.md        (LEGACY — to be superseded)  
  openapi.yaml                     (if exists, must be updated to canonical terms)  
schemas/  
  moral_trace_log.yaml             (if exists, must align with TSLF Section 8)  
  justification_object.yaml        (if exists, must align with monograph)  
core/  
  SYSTEM_STATE_MACHINE.md  
  ANCHORING_STANDARDS.md  
  SYNC_PROTOCOL.md  
  SHUTDOWN_TRIGGERS.md  
docs/specs/  
  Dual-Lane Architecture.md  
  TML_Gateway.md  
  Sacred_Pause_Protocol.md  
  EKR_Security_Architecture.md  
sdk/  
  python/  cpp/  go/  java/        (public interfaces referenced only; not specified in this pass)  
Smart_Contracts/  
  src/TML_Core.sol  
  src/ITMLEnforcer.sol  
tml_audit_project/  
  apis/auditor_api.py  
  apis/redress_api.py  
  apis/regulator_api.py  
compliance/  
  human_rights/  
  earth_protection/  
No_Log-No_Action/  
No_Spy-No_Weapon/  
```

## 5. REQUIRED DELIVERABLES

### A. `openapi.yaml` — Canonical API Contract  
The `info.version` field must be tied to the monograph version: `3.3.0-tml-monograph-2025` (or current monograph version). Include a `servers` entry with a placeholder URL: `https://api.tml-framework.example/v1`.

Define endpoints for:  
- **Inference Lane:** Submit decision vector, receive proposed state (+1/0/-1)  
- **Anchoring Lane:** Submit Moral Trace Log, receive Permission Token (cryptographic release key)  
- **Sacred Zero Escalation:** Human-in-the-loop review queue, Lantern signal broadcast  
- **Refusal State:** Hard refusal logging, License violation recording  
- **Emergency Override:** Break-glass shutdown, kill switch activation, forced state transitions under supreme authority (Monograph Section 13.3)  
- **Auditor Verification Endpoints:** Merkle root verification, log inclusion proof, custodian heartbeat check, compliance attestation pull  
- **Redress / Appeal Endpoints:** Subject-initiated challenge, Moral Trace Log re-evaluation, human rights grievance filing  
- **Regulator Inspection Endpoints:** Bulk evidence export, cross-jurisdiction custodian quorum status, qualified timestamp verification  
- **Gateway Endpoints:** TML Gateway Logic routing, lane assignment, fail-closed status

Include OpenAPI `webhooks` or `callbacks` for:  
- `sacredPause.escalation`: Async notification when State 0 triggers human review  
- `lanternStatus.broadcast`: Public beacon signal updates  
Specify payload schema, retry semantics, and `x-tml-idempotency` headers for each webhook.

Every endpoint MUST include:  
- `x-tml-pillar` annotation using the canonical identifiers from Section 2  
- `x-tml-monograph-ref` annotation (e.g., `x-tml-monograph-ref: "Section 2.3.3"`)  
- `x-tml-implementation-status` annotation per this decision table:

| **Status** | **Decision Criteria** |  
|------------|----------------------|  
| **SHIPPING** | Buildable with 2025 production libraries and infrastructure; no known blockers from Section 10. |  
| **BETA** | Buildable with documented tradeoffs; latency, cost, or throughput penalties are acceptable for regulated deployments. |  
| **FUTURE** | Blocked by a named constraint from Section 10 (Implementation Gap); add sibling `x-tml-blocking-constraint` with the quoted section reference. |

Every endpoint MUST also declare security requirements using OpenAPI `securitySchemes`:  
- Inference Lane: `x-tml-security: "mTLS + ServiceAccountJWT"`  
- Anchoring/Governance Lanes: `x-tml-security: "HSM-SignedJWT + MutualTLS"`  
- Auditor/Regulator/Redress: `x-tml-security: "CA-VettedJWT + IPAllowlist"`

Define these in `components.securitySchemes` and attach to relevant paths.

Every `POST`, `PUT`, and `PATCH` endpoint MUST require an `Idempotency-Key` header. Error responses MUST conform to RFC 7807 `application/problem+json` with `x-tml-state`, `x-tml-pillar`, and `retry_after` fields.

### B. `tml_schema.json` — JSON Schema Bundle  
Produce a single JSON Schema document using `$defs` that contains each named schema as a definition (e.g., `$defs/TSLF-State0`). Reference them with `$ref` across the OpenAPI specification.

All JSON Schemas MUST:  
- Use `"$schema": "https://json-schema.org/draft/2020-12/schema"`  
- Enforce `unevaluatedProperties: false` to reject unknown fields  
- Use `oneOf` with `discriminator` for TSLF state variants  
- Include `default` values only where explicitly required by the monograph

Define strict schemas for:  
1. **State Envelope:** The outer decision container. Must include `current_state` (+1/0/-1), `state_label`, `proposed_action`, and conditionally require `permission_token` when `current_state == "+1"`.  
2. **TSLF-State0 (Sacred Pause Log):** Must include `lantern_status`, `uncertainty_quantification`, `deliberation_matrix`, `resolution_request`  
3. **TSLF-State-1 (Refusal Log):** Must include `license_violation`, `threat_vector_analysis`, `chain_of_custody`  
4. **TSLF-State+1 (Proceed Log):** Must include `ethical_verification`, `the_signature`, `audit_proof`  
5. **Justification Object:** The envelope that travels between Inference and Anchoring lanes  
6. **Lantern Status:** The public compliance beacon signal  
7. **Signature Block:** The provenance and non-repudiation artifact

#### B.i. Permission Token Schema (Dedicated Subsection)  
The Permission Token is the schema-level enforcement of **No Log = No Action**. Define it as a standalone schema with:

- **Required fields:** `log_hash` (SHA-256 of the anchored Moral Trace Log), `epoch_timestamp`, `signer_key_id`, `lane_origin` (Inference or Anchoring)  
- **Non-repudiation binding:** The token must be cryptographically signed by the Anchoring Lane and verifiable against the Merkle root  
- **Schema constraint:** Any State Envelope with `current_state: +1` MUST include a valid Permission Token. Its absence renders the envelope invalid by schema constraint. The inference engine cannot transition to +1 without this token.

### C. `tml_abi.json` — Smart Contract Interface  
Define the standard ABI (Application Binary Interface) for:  
- `TML_Core.sol`: Core constitutional enforcement functions  
- `ITMLEnforcer.sol`: Interface for mandate enforcement (Human Rights, Earth Protection)

Output a JSON object containing function signatures, event logs, and structured data types only. No Solidity source code.

### D. `eip712_typed_data.json` — EIP-712 Typed Data Schema  
Define the EIP-712 domain separator and type definitions for off-chain structured data hashing:  
- `MoralTraceLog` typed data  
- `PermissionToken` typed data

Include `primaryType`, `domain` (EIP712Domain), and `types` definitions. This is distinct from the on-chain ABI.

### E. `constitutional_compliance_matrix.md`  
A table mapping every OpenAPI path and every JSON Schema property to:  
- Monograph Section and Subsection  
- TML Pillar (I–VIII) using canonical identifiers  
- Regulatory nexus (EU AI Act Article, NIST RMF Function, ISO 42001 Clause, FRE 902 Rule)  
- Implementation Status per the Section 5A decision table

**Regulatory Nexus Guard:** Only map to provisions explicitly cited or unmistakably implied in the monograph. For all other cells, write `Not directly referenced in monograph`.

### F. `specification_architecture.md`  
The narrative document explaining:  
- How the Dual-Lane Architecture is expressed in the OpenAPI paths, with explicit separation of the binary Inference Lane and the ternary Anchoring Lane  
- How the binary system proposes actions while the ternary system dictates execution via the Permission Token  
- How the "No Log = No Action" principle is enforced at the schema level  
- How the Goukassian Promise artifacts (Lantern, Signature, License) are represented as API resources  
- How the Eight Pillars are operationalized as API capabilities versus out-of-band processes

**STRICT FORMATTING RULE:** In narrative prose, avoid em-dashes and en-dashes. Use colons, semicolons, or commas for clause separation. Standard markdown list syntax (`- ` or `* `) and code fence markers are permitted.

### G. `future_blocked_appendix.md`  
Explicitly list features that are **architectural targets but not shipping specifications** due to the Implementation Gap (Section 10):  
- Real-time per-token blockchain anchoring (throughput asymmetry)  
- Quantum-proof signature migration (PQC algorithms)  
- Hardware Moral Processing Units (MPUs)  
- Cross-jurisdiction custodian quorum in <500ms  
- Immutable ledger with native GDPR Article 17 compliance (Erasure Paradox)

For each blocked feature, cite the specific monograph section explaining the constraint. If the monograph proposes a mitigation (e.g., cryptographic erasure for GDPR), note the mitigation and still classify the feature as `FUTURE`, explaining what remains unbuildable.

## 6. QUALITY GATES

Before finalizing, verify:  
- [ ] Zero terminology drift: Every concept from the monograph appears verbatim in the spec.  
- [ ] Every endpoint has an `x-tml-pillar` and `x-tml-monograph-ref` annotation.  
- [ ] The binary-ternary parallel architecture is explicit: Inference Lane proposes; Anchoring Lane dictates execution via Permission Token.  
- [ ] The Sacred Zero (State 0) is never represented as `null`, `error`, `false`, or `timeout`. It is a first-class state.  
- [ ] The Sacred Pause is explicitly documented as the operational workflow that executes within State 0, not as a synonym for the state itself.    
  **Negative example (do not do this):** `state: "SacredPause"` as an alias for State 0.    
  **Correct example:** `state: 0`, `state_label: "SacredZero"`, `process_active: "SacredPause"`.  
- [ ] The State Envelope schema explicitly rejects any `current_state: "+1"` object that lacks a valid `permission_token` field (No Log = No Action enforced at the schema level).  
- [ ] The "No Log = No Action" principle is schema-enforced: the Permission Token is a required field for all `+1` state envelopes.  
- [ ] The Implementation Gap is acknowledged: no endpoint claims to do real-time Merkle anchoring of every token at global AI scale.  
- [ ] The Goukassian Promise artifacts are explicitly modeled by their canonical string names (`lantern`, `signature`, `license`) in all machine-readable schemas. Emoji symbols and visual shorthand are restricted to narrative markdown only.

## 7. SUCCESS CRITERION (SPLIT BY AUDIENCE)

The final output must satisfy two distinct quality bars:

**For Engineers:** The `openapi.yaml` and JSON Schemas must provide sufficient endpoint definitions, request/response examples, and error codes to build a TML-compliant system without re-reading the monograph.

**For Auditors:** The `constitutional_compliance_matrix.md` must provide sufficient regulatory mapping, monograph cross-references, and implementation status labeling to verify compliance without reading any implementation code.

## 8. GENERATION PROTOCOL  
Output deliverables sequentially. Begin with A. `openapi.yaml`. Pause and await "CONTINUE" before proceeding to B. Repeat for C through G. Do not compress, summarize, or skip any deliverable.

Do not hallucinate features. If a capability is not in the monograph, do not add it. If a capability is in the monograph but unbuildable per Section 10, label it `FUTURE` and explain why.

END OF PROMPT  
```

**Step 1:**  
[PASTE FULL v3.3 PROMPT]  
[PASTE MONOGRAPH EXCERPTS FOR A]  
EXECUTE DELIVERABLE A: openapi.yaml

**Step 2:**  
[PASTE FULL v3.3 PROMPT]  
[PASTE MONOGRAPH EXCERPTS FOR B]  
[ATTACH: Output from Step 1 (openapi.yaml)]  
EXECUTE DELIVERABLE B: tml_schema.json  
Use the attached openapi.yaml to ensure your schema names and $ref targets match exactly.

**Step 3:**  
[PASTE FULL v3.3 PROMPT]  
[PASTE MONOGRAPH EXCERPTS FOR C AND D]  
EXECUTE DELIVERABLES C AND D: tml_abi.json and eip712_typed_data.json

**Step 4:**  
[PASTE FULL v3.3 PROMPT]  
[PASTE MONOGRAPH EXCERPTS FOR E]  
[ATTACH: Output from Step 1 (openapi.yaml)]  
[ATTACH: Output from Step 2 (tml_schema.json)]  
EXECUTE DELIVERABLE E: constitutional_compliance_matrix.md  
Map every path from the attached openapi.yaml and every property from the attached tml_schema.json.

**Step 5:**  
[PASTE FULL v3.3 PROMPT]  
[PASTE MONOGRAPH EXCERPTS FOR F AND G]  
[ATTACH: Output from Step 1 (openapi.yaml)]  
[ATTACH: Output from Step 2 (tml_schema.json)]  
EXECUTE DELIVERABLES F AND G: specification_architecture.md and future_blocked_appendix.md  
Reference the actual endpoint names and schema structures from the attached files.

