// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ITL_Validator.sol";

/**
 * @title TL_Evidence_Vault
 * @dev Immutable on-chain storage for TL governance evidence.
 *
 * Framework: "Ternary Logic" (TL) by Lev Goukassian
 * ORCID: 0009-0006-5966-1243
 * DOI: 10.1007/s43681-025-00910-6
 * DOI: 10.1007/s43681-026-01124-0
 *
 * Constitutional role: provides the physical storage substrate for the
 * NL=NA invariant. G(execute implies P(escrow_recorded and auditable)).
 * Every governance action that reaches execution must have a prior,
 * immutable, tamper-evident evidence record in this vault.
 *
 * Architecture:
 *   - EvidenceLog entries are write-once. Overwrite attempts revert.
 *   - Merkle roots are anchored on-chain before PermissionTokens can be issued.
 *   - laneOrigin must equal keccak256("GOVERNANCE_LANE") on every write.
 *   - Only TL_Ledger_Core can write evidence (onlyCore modifier).
 *   - TL_Ledger_Core address is set once at initialization and immutable.
 *
 * Immutable Mandates (beyond any governance body's authority):
 *   No Spy | No Weapon | No Switch Off
 */
contract TL_Evidence_Vault {

    // -------------------------------------------------------------------------
    // CONSTANTS
    // -------------------------------------------------------------------------

    /**
     * @dev Canonical Governance Lane identifier.
     * NL=NA Layer 2: all evidence writes must originate from the Governance Lane.
     * Any write with a different laneOrigin reverts NLNAViolation.
     */
    bytes32 public constant GOVERNANCE_LANE_HASH = keccak256("GOVERNANCE_LANE");

    /**
     * @dev Canonical Goukassian Principle artifact name hashes.
     */
    bytes32 public constant LANTERN_HASH    = keccak256("lantern");
    bytes32 public constant SIGNATURE_HASH  = keccak256("signature");
    bytes32 public constant LICENSE_HASH    = keccak256("license");

    /**
     * @dev Immutable Mandate hashes.
     * Used in mandate violation records.
     */
    bytes32 public constant NO_SPY_HASH        = keccak256("No Spy");
    bytes32 public constant NO_WEAPON_HASH     = keccak256("No Weapon");
    bytes32 public constant NO_SWITCH_OFF_HASH = keccak256("No Switch Off");

    // -------------------------------------------------------------------------
    // STORAGE
    // -------------------------------------------------------------------------

    /**
     * @dev Full evidence record for a governance action.
     * Write-once. Overwrite attempts revert ImmutabilityViolation.
     *
     * Fields:
     *   timestamp       - block.timestamp at archival
     *   uri             - IPFS or Arweave link to off-chain document
     *   submitter       - Governance Lane operator address
     *   finalState      - TL triadic state: +1, 0, -1
     *   merkleRoot      - Batch Merkle root this record belongs to
     *   laneOrigin      - Must equal GOVERNANCE_LANE_HASH
     *   permissionTokenId - Associated PermissionToken (zero bytes32 for State 0/-1)
     *   traceId         - X-TL-Trace-Id UUID v4 from originating API request
     *   escrowRecordId  - EscrowRecord identifier for State 0 entries
     */
    struct EvidenceLog {
        uint256 timestamp;
        string  uri;
        address submitter;
        int8    finalState;
        bytes32 merkleRoot;
        bytes32 laneOrigin;
        bytes32 permissionTokenId;
        bytes32 traceId;
        bytes32 escrowRecordId;
    }

    /**
     * @dev Anchored Merkle root record.
     * Once anchored, immutable. Enables NL=NA Layer 5 enforcement.
     */
    struct AnchoredRoot {
        uint256 anchoredAt;
        bytes32 batchId;
        address anchoredBy;
        bool    exists;
    }

    /// @dev Maps transaction hash to its immutable evidence log.
    mapping(bytes32 => EvidenceLog) private _vault;

    /// @dev Maps Merkle root to its on-chain anchor record.
    mapping(bytes32 => AnchoredRoot) private _anchoredRoots;

    /// @dev Maps mandate violation ID to immutability flag.
    mapping(bytes32 => bool) private _mandateViolations;

    /// @dev The one and only address authorized to write evidence.
    address public ledgerCore;

    /// @dev System-wide Epistemic Hold state.
    bool public epistemicHoldActive;
    bytes32 public activeEscrowRecordId;
    uint256 public epistemicHoldResolutionDeadline;

    // -------------------------------------------------------------------------
    // EVENTS
    // -------------------------------------------------------------------------

    event EvidenceArchived(
        bytes32 indexed txHash,
        int8    indexed finalState,
        bytes32         merkleRoot,
        bytes32         traceId,
        uint256         timestamp
    );

    event MerkleRootAnchored(
        bytes32 indexed merkleRoot,
        bytes32 indexed batchId,
        address         anchoredBy,
        uint256         anchoredAt
    );

    event EpistemicHoldActivated(
        bytes32 indexed escrowRecordId,
        uint256         resolutionDeadline,
        uint256         activatedAt
    );

    event EpistemicHoldResolved(
        bytes32 indexed escrowRecordId,
        uint8           resolvedState,
        uint256         resolvedAt
    );

    // -------------------------------------------------------------------------
    // ERRORS
    // -------------------------------------------------------------------------

    /// @dev Reverted when an evidence write is attempted for an existing entry.
    error ImmutabilityViolation(bytes32 txHash);

    /// @dev Reverted when a caller other than TL_Ledger_Core attempts a write.
    error UnauthorizedWriter(address caller);

    /// @dev Reverted when laneOrigin does not equal GOVERNANCE_LANE_HASH.
    error InvalidLaneOrigin(bytes32 provided, bytes32 required);

    /// @dev Reverted when a Merkle root is not found in anchored roots.
    error MerkleRootNotAnchored(bytes32 merkleRoot);

    /// @dev Reverted when a Merkle root is already anchored (immutability).
    error MerkleRootAlreadyAnchored(bytes32 merkleRoot);

    /// @dev Reverted when a mandate violation ID already exists.
    error MandateViolationAlreadyRecorded(bytes32 violationId);

    /// @dev Reverted when ledgerCore is already set.
    error LedgerCoreAlreadySet();

    /// @dev Reverted when system-wide Epistemic Hold is active.
    error SystemEpistemicHoldActive(bytes32 escrowRecordId);

    // -------------------------------------------------------------------------
    // MODIFIERS
    // -------------------------------------------------------------------------

    modifier onlyCore() {
        if (msg.sender != ledgerCore) revert UnauthorizedWriter(msg.sender);
        _;
    }

    modifier notUnderEpistemicHold() {
        if (epistemicHoldActive) revert SystemEpistemicHoldActive(activeEscrowRecordId);
        _;
    }

    // -------------------------------------------------------------------------
    // INITIALIZATION
    // -------------------------------------------------------------------------

    constructor() {}

    /**
     * @dev Set the TL_Ledger_Core address. Called once during deployment.
     * Immutable after first call. Cannot be changed - no admin key.
     */
    function setLedgerCore(address _core) external {
        if (ledgerCore != address(0)) revert LedgerCoreAlreadySet();
        require(_core != address(0), "TL_Vault: Zero address not permitted");
        ledgerCore = _core;
    }

    // -------------------------------------------------------------------------
    // MERKLE ROOT ANCHORING
    // -------------------------------------------------------------------------

    /**
     * @dev Anchor a Merkle root on-chain. Called by TL_Ledger_Core after
     * Tri-Cameral quorum verification. Once anchored, the root enables
     * NL=NA Layer 5 enforcement: only logHashes provably included in this
     * root can be used to register PermissionTokens.
     *
     * Reverts MerkleRootAlreadyAnchored if root is already anchored.
     * Emits MerkleRootAnchored on success.
     */
    function anchorMerkleRoot(
        bytes32 merkleRoot,
        bytes32 batchId,
        address anchoredBy
    ) external onlyCore {
        if (_anchoredRoots[merkleRoot].exists) {
            revert MerkleRootAlreadyAnchored(merkleRoot);
        }

        _anchoredRoots[merkleRoot] = AnchoredRoot({
            anchoredAt: block.timestamp,
            batchId:    batchId,
            anchoredBy: anchoredBy,
            exists:     true
        });

        emit MerkleRootAnchored(merkleRoot, batchId, anchoredBy, block.timestamp);
    }

    /**
     * @dev Check whether a Merkle root has been anchored on-chain.
     */
    function isMerkleRootAnchored(bytes32 merkleRoot) external view returns (bool) {
        return _anchoredRoots[merkleRoot].exists;
    }

    /**
     * @dev Retrieve the full anchor record for a Merkle root.
     */
    function getAnchoredRoot(bytes32 merkleRoot)
        external
        view
        returns (uint256 anchoredAt, bytes32 batchId, address anchoredBy)
    {
        AnchoredRoot memory root = _anchoredRoots[merkleRoot];
        if (!root.exists) revert MerkleRootNotAnchored(merkleRoot);
        return (root.anchoredAt, root.batchId, root.anchoredBy);
    }

    // -------------------------------------------------------------------------
    // MERKLE INCLUSION VERIFICATION
    // -------------------------------------------------------------------------

    /**
     * @dev Pure function. Verify that a leaf hash is included in a Merkle root
     * given an ordered sibling hash proof path.
     * Used by TL_Ledger_Core for NL=NA Layer 5 enforcement before
     * PermissionToken registration.
     */
    function verifyMerkleInclusion(
        bytes32 leaf,
        bytes32 merkleRoot,
        bytes32[] calldata proof
    ) external pure returns (bool included) {
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (computedHash <= proofElement) {
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        return computedHash == merkleRoot;
    }

    // -------------------------------------------------------------------------
    // EVIDENCE ARCHIVAL
    // -------------------------------------------------------------------------

    /**
     * @dev Archive governance evidence permanently. Called only by TL_Ledger_Core.
     *
     * Constitutional requirements enforced here:
     *   1. Write-once: reverts ImmutabilityViolation if entry already exists.
     *   2. Lane origin: reverts InvalidLaneOrigin if laneOrigin != GOVERNANCE_LANE_HASH.
     *   3. Merkle root: reverts MerkleRootNotAnchored if merkleRoot not anchored.
     *   4. Epistemic Hold: State +1 writes blocked if system hold is active.
     *
     * NL=NA: the evidence record is created BEFORE execution gate releases.
     * The record cannot be absent if the action occurred.
     */
    function archiveEvidence(
        bytes32 _txHash,
        string  calldata _uri,
        address _submitter,
        int8    _state,
        bytes32 _merkleRoot,
        bytes32 _laneOrigin,
        bytes32 _permissionTokenId,
        bytes32 _traceId,
        bytes32 _escrowRecordId
    ) external onlyCore {
        // 1. Immutability check
        if (_vault[_txHash].timestamp != 0) {
            revert ImmutabilityViolation(_txHash);
        }

        // 2. Lane origin check - NL=NA Layer 2
        if (_laneOrigin != GOVERNANCE_LANE_HASH) {
            revert InvalidLaneOrigin(_laneOrigin, GOVERNANCE_LANE_HASH);
        }

        // 3. Merkle root must be anchored - NL=NA Layer 5
        if (!_anchoredRoots[_merkleRoot].exists) {
            revert MerkleRootNotAnchored(_merkleRoot);
        }

        // 4. If State +1 (Proceed), system must not be under Epistemic Hold
        if (_state == 1 && epistemicHoldActive) {
            revert SystemEpistemicHoldActive(activeEscrowRecordId);
        }

        // 5. Archive
        _vault[_txHash] = EvidenceLog({
            timestamp:         block.timestamp,
            uri:               _uri,
            submitter:         _submitter,
            finalState:        _state,
            merkleRoot:        _merkleRoot,
            laneOrigin:        _laneOrigin,
            permissionTokenId: _permissionTokenId,
            traceId:           _traceId,
            escrowRecordId:    _escrowRecordId
        });

        emit EvidenceArchived(_txHash, _state, _merkleRoot, _traceId, block.timestamp);
    }

    // -------------------------------------------------------------------------
    // EPISTEMIC HOLD MANAGEMENT
    // -------------------------------------------------------------------------

    /**
     * @dev Activate system-wide Epistemic Hold. Called by TL_Ledger_Core
     * after Tri-Cameral quorum verification.
     * Blocks all subsequent State +1 evidence writes until resolved.
     */
    function activateEpistemicHold(
        bytes32 _escrowRecordId,
        uint256 _resolutionDeadline
    ) external onlyCore {
        epistemicHoldActive = true;
        activeEscrowRecordId = _escrowRecordId;
        epistemicHoldResolutionDeadline = _resolutionDeadline;

        emit EpistemicHoldActivated(_escrowRecordId, _resolutionDeadline, block.timestamp);
    }

    /**
     * @dev Resolve system-wide Epistemic Hold. Called by TL_Ledger_Core
     * after Tri-Cameral quorum verification.
     * resolvedState uint8 encoding (function-local):
     *   1 = PROCEED (+1 integer)
     *   0 = REFUSE  (-1 integer)
     * Epistemic Hold (State 0) is not a valid resolution.
     */
    function resolveEpistemicHold(
        bytes32 _escrowRecordId,
        uint8   _resolvedState
    ) external onlyCore {
        require(epistemicHoldActive, "TL_Vault: No active Epistemic Hold");
        require(
            _resolvedState == 0 || _resolvedState == 1,
            "TL_Vault: Invalid resolution state"
        );

        epistemicHoldActive = false;
        activeEscrowRecordId = bytes32(0);
        epistemicHoldResolutionDeadline = 0;

        emit EpistemicHoldResolved(_escrowRecordId, _resolvedState, block.timestamp);
    }

    // -------------------------------------------------------------------------
    // MANDATE VIOLATION RECORDING
    // -------------------------------------------------------------------------

    /**
     * @dev Record an immutable mandate violation.
     * Write-once: reverts MandateViolationAlreadyRecorded if violationId exists.
     * mandateViolated must be one of:
     *   NO_SPY_HASH, NO_WEAPON_HASH, or NO_SWITCH_OFF_HASH
     */
    function recordMandateViolation(
        bytes32 _violationId,
        bytes32 _mandateViolated,
        bytes32 _violationDetailsHash,
        bytes32 _decisionId
    ) external onlyCore {
        if (_mandateViolations[_violationId]) {
            revert MandateViolationAlreadyRecorded(_violationId);
        }

        require(
            _mandateViolated == NO_SPY_HASH ||
            _mandateViolated == NO_WEAPON_HASH ||
            _mandateViolated == NO_SWITCH_OFF_HASH,
            "TL_Vault: Unknown mandate"
        );

        _mandateViolations[_violationId] = true;

        // Mandate violations anchor to the zero Merkle root (pre-anchoring context)
        // and are always written with GOVERNANCE_LANE origin.
        _vault[_violationId] = EvidenceLog({
            timestamp:         block.timestamp,
            uri:               "",
            submitter:         msg.sender,
            finalState:        -1,
            merkleRoot:        _violationDetailsHash,
            laneOrigin:        GOVERNANCE_LANE_HASH,
            permissionTokenId: bytes32(0),
            traceId:           _decisionId,
            escrowRecordId:    bytes32(0)
        });
    }

    // -------------------------------------------------------------------------
    // READ FUNCTIONS
    // -------------------------------------------------------------------------

    /**
     * @dev Retrieve the full evidence log for a transaction hash.
     */
    function getEvidence(bytes32 _txHash)
        external
        view
        returns (
            uint256 timestamp,
            string memory uri,
            address submitter,
            int8 finalState,
            bytes32 merkleRoot,
            bytes32 laneOrigin,
            bytes32 permissionTokenId,
            bytes32 traceId,
            bytes32 escrowRecordId
        )
    {
        EvidenceLog memory log = _vault[_txHash];
        return (
            log.timestamp,
            log.uri,
            log.submitter,
            log.finalState,
            log.merkleRoot,
            log.laneOrigin,
            log.permissionTokenId,
            log.traceId,
            log.escrowRecordId
        );
    }

    /**
     * @dev Check whether an evidence entry exists for a transaction hash.
     */
    function evidenceExists(bytes32 _txHash) external view returns (bool) {
        return _vault[_txHash].timestamp != 0;
    }

    /**
     * @dev Retrieve the TL triadic state for a transaction hash.
     * Returns 0 (EpistemicHold) if no evidence exists yet - fail-closed default.
     */
    function getTransactionState(bytes32 _txHash) external view returns (int8) {
        EvidenceLog memory log = _vault[_txHash];
        if (log.timestamp == 0) return 0; // Fail-closed: unknown = EpistemicHold
        return log.finalState;
    }

    /**
     * @dev Check whether a mandate violation has been recorded.
     */
    function mandateViolationExists(bytes32 _violationId) external view returns (bool) {
        return _mandateViolations[_violationId];
    }
}
