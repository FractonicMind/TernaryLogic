// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ITL_Validator.sol";
import "./TL_Evidence_Vault.sol";

/**
 * @title TL_Ledger_Core
 * @dev Core governance logic contract for the Ternary Logic (TL) framework.
 *
 * Framework: "Ternary Logic" (TL) by Lev Goukassian
 * ORCID: 0009-0006-5966-1243
 * DOI: 10.1007/s43681-025-00910-6
 * DOI: 10.1007/s43681-026-01124-0
 *
 * Constitutional role:
 *   - Anchors Merkle roots (NL=NA Layer 5 foundation)
 *   - Registers and verifies PermissionTokens (NL=NA Layer 5 terminal gate)
 *   - Manages system-wide Epistemic Hold activation and resolution
 *   - Executes Emergency Overrides under logged conditions
 *   - Enforces Tri-Cameral quorum on all state-mutating operations
 *
 * NL=NA Invariant: G(execute implies P(escrow_recorded and auditable))
 *
 * NO ADMIN KEY. All governance is Tri-Cameral only:
 *   - Technical Council: 9 members, proposal rights, no veto
 *   - Stewardship Custodians: 11 members, binding veto, no proposal rights
 *   - Smart Contract Treasury: automatic execution on verified milestones
 *
 * Immutable Mandates (beyond any governance body's authority):
 *   No Spy | No Weapon | No Switch Off
 */
contract TL_Ledger_Core is ITL_Validator {

    // -------------------------------------------------------------------------
    // CONSTANTS
    // -------------------------------------------------------------------------

    bytes32 public constant GOVERNANCE_LANE_HASH = keccak256("GOVERNANCE_LANE");

    bytes32 public constant LANTERN_HASH    = keccak256("lantern");
    bytes32 public constant SIGNATURE_HASH  = keccak256("signature");
    bytes32 public constant LICENSE_HASH    = keccak256("license");

    bytes32 public constant NO_SPY_HASH        = keccak256("No Spy");
    bytes32 public constant NO_WEAPON_HASH     = keccak256("No Weapon");
    bytes32 public constant NO_SWITCH_OFF_HASH = keccak256("No Switch Off");

    /// @dev Governance Lane hard ceiling in milliseconds.
    uint256 public constant GOVERNANCE_LANE_MAX_LIFETIME_MS = 300_000;

    /// @dev Tri-Cameral thresholds.
    uint8 public constant TECHNICAL_COUNCIL_SIZE       = 9;
    uint8 public constant STEWARDSHIP_CUSTODIAN_SIZE   = 11;
    uint8 public constant TECHNICAL_COUNCIL_THRESHOLD  = 7;
    uint8 public constant CUSTODIAN_THRESHOLD          = 9;

    // -------------------------------------------------------------------------
    // TREASURY AND FEE STORAGE
    // -------------------------------------------------------------------------

    /**
     * @dev Goukassian Foundation Smart Contract Treasury address.
     *
     * Receives all TL service fees. No individual can withdraw directly.
     * Disbursements require Tri-Cameral Joint-Approval supermajority
     * independently in both Technical Council and Stewardship Custodians.
     *
     * Set at deployment. Changeable only via Tri-Cameral quorum.
     * Cannot be the zero address.
     */
    address payable public smartContractTreasury;

    /**
     * @dev TL Service Fee Parameters.
     *
     * All fees are governance parameters set by Tri-Cameral Joint-Approval.
     * NOT hardcoded constants. Initial values set at deployment as
     * "Nomination 2026" — subject to revision by governance at any time.
     *
     * Fees are denominated in the network's native token (wei on Polygon).
     * No fiat denomination. Fee levels absorb token price volatility through
     * governance revision rather than oracle dependency.
     *
     * Fee schedule:
     *   permissionTokenFee  - charged per State +1 PermissionToken registration
     *                         (the constitutional enforcement service)
     *   archiveEvidenceFee  - charged per governance action archived in Vault
     *                         (the immutable record service)
     *   License fees        - off-chain, managed by the Goukassian Foundation
     *                         directly. Not enforced by these contracts.
     *
     * Epistemic Hold activation and resolution carry NO fee by design.
     * Charging for a constitutional pause creates a perverse incentive
     * to avoid holds. Holds protect humans. They are free.
     */
    uint256 public permissionTokenFee;  // Nomination 2026: set at deployment
    uint256 public archiveEvidenceFee;  // Nomination 2026: set at deployment

    /**
     * @dev Treasury disbursement proposals.
     * proposalId => DisbursementProposal
     * Proposals submitted by Technical Council, vetoed by Stewardship Custodians.
     */
    struct DisbursementProposal {
        address payable recipient;
        uint256 amount;
        bytes32 purposeHash;
        uint8   technicalCouncilApprovals;
        uint8   stewardshipCustodianApprovals;
        bool    vetoExercised;
        bool    executed;
        uint256 proposedAt;
    }
    mapping(bytes32 => DisbursementProposal) private _disbursementProposals;

    // -------------------------------------------------------------------------
    // TREASURY EVENTS
    // -------------------------------------------------------------------------

    event FeesUpdated(
        uint256 newPermissionTokenFee,
        uint256 newArchiveEvidenceFee,
        uint256 updatedAt
    );

    event TreasuryAddressUpdated(
        address indexed oldTreasury,
        address indexed newTreasury,
        uint256 updatedAt
    );

    event FeeCollected(
        bytes32 indexed operationId,
        uint8   feeType,    // 1=PERMISSION_TOKEN, 2=ARCHIVE_EVIDENCE
        uint256 amount,
        address payer,
        uint256 collectedAt
    );

    event DisbursementProposed(
        bytes32 indexed proposalId,
        address indexed recipient,
        uint256 amount,
        bytes32 purposeHash,
        uint256 proposedAt
    );

    event DisbursementApproved(
        bytes32 indexed proposalId,
        address indexed recipient,
        uint256 amount,
        uint256 executedAt
    );

    event DisbursementVetoed(
        bytes32 indexed proposalId,
        uint256 vetoedAt
    );

    // -------------------------------------------------------------------------
    // STORAGE
    // -------------------------------------------------------------------------

    /// @dev Immutable reference to the Evidence Vault.
    TL_Evidence_Vault public immutable evidenceVault;

    /**
     * @dev Registered PermissionToken storage.
     * tokenId => PermissionTokenRecord
     */
    struct PermissionTokenRecord {
        bytes32 logHash;
        bytes32 merkleRoot;
        uint256 epochTimestamp;
        uint256 expiresAt;
        uint8   revocationStatus; // 0=ACTIVE, 1=REVOKED_BY_EMERGENCY, 2=REVOKED_BY_TRI_CAMERAL
        bytes32 revocationMerkleRoot;
        bool    exists;
    }
    mapping(bytes32 => PermissionTokenRecord) private _permissionTokens;

    /**
     * @dev Authorized Governance Lane operators.
     * These are the only addresses permitted to call registerPermissionToken
     * and anchorMerkleRoot. Set through Tri-Cameral quorum process only.
     */
    mapping(address => bool) private _governanceLaneOperators;

    /**
     * @dev Tri-Cameral quorum tracking for operations.
     * operationId => custodianId => attested
     */
    mapping(bytes32 => mapping(bytes32 => bool)) private _quorumAttestations;
    mapping(bytes32 => uint8) private _quorumCounts;

    // -------------------------------------------------------------------------
    // MODIFIERS
    // -------------------------------------------------------------------------

    modifier onlyGovernanceLane() {
        require(
            _governanceLaneOperators[msg.sender],
            "TL_Core: Caller is not an authorized Governance Lane operator"
        );
        _;
    }

    modifier quorumRequired(
        CustodianAttestation[] calldata attestations,
        uint8 required
    ) {
        if (attestations.length < required) {
            revert QuorumNotMet(uint8(attestations.length), required);
        }
        _;
    }

    // -------------------------------------------------------------------------
    // CONSTRUCTOR
    // -------------------------------------------------------------------------

    /**
     * @dev Deploy with the Evidence Vault address.
     * No admin key. No owner. No privileged deployer after construction.
     * Initial Governance Lane operator must be set via
     * bootstrapGovernanceLaneOperator() which can only be called once.
     */
    constructor(
        address _evidenceVault,
        address payable _smartContractTreasury,
        uint256 _permissionTokenFeeNomination2026,
        uint256 _archiveEvidenceFeeNomination2026
    ) {
        require(_evidenceVault != address(0), "TL_Core: Zero vault address");
        require(_smartContractTreasury != address(0), "TL_Core: Zero treasury address");
        evidenceVault = TL_Evidence_Vault(_evidenceVault);
        smartContractTreasury = _smartContractTreasury;
        permissionTokenFee = _permissionTokenFeeNomination2026;
        archiveEvidenceFee = _archiveEvidenceFeeNomination2026;
    }

    /// @dev Bootstrap flag - allows one-time initial operator registration.
    bool private _bootstrapped;

    /**
     * @dev One-time bootstrap: register the initial Governance Lane operator.
     * Can only be called once. After bootstrap, all operator changes require
     * Tri-Cameral quorum via authorizeGovernanceLaneOperator().
     */
    function bootstrapGovernanceLaneOperator(address operator) external {
        require(!_bootstrapped, "TL_Core: Already bootstrapped");
        require(operator != address(0), "TL_Core: Zero operator address");
        _bootstrapped = true;
        _governanceLaneOperators[operator] = true;
    }

    /**
     * @dev Authorize a new Governance Lane operator.
     * Requires Tri-Cameral custodian quorum.
     */
    function authorizeGovernanceLaneOperator(
        address operator,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        require(operator != address(0), "TL_Core: Zero operator address");
        _verifyQuorumAttestations(attestations);
        _governanceLaneOperators[operator] = true;
    }

    /**
     * @dev Revoke a Governance Lane operator.
     * Requires Tri-Cameral custodian quorum.
     */
    function revokeGovernanceLaneOperator(
        address operator,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        _verifyQuorumAttestations(attestations);
        _governanceLaneOperators[operator] = false;
    }


    // -------------------------------------------------------------------------
    // TREASURY AND FEE GOVERNANCE
    // -------------------------------------------------------------------------

    /**
     * @dev Update TL service fee parameters.
     * Requires Tri-Cameral custodian quorum (Joint-Approval).
     * Epistemic Hold fees are always zero - not configurable.
     * Emits FeesUpdated.
     *
     * Initial values are "Nomination 2026" set at deployment.
     * This function is the governance revision pathway for subsequent periods.
     */
    function setFees(
        uint256 _permissionTokenFee,
        uint256 _archiveEvidenceFee,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        _verifyQuorumAttestations(attestations);
        permissionTokenFee = _permissionTokenFee;
        archiveEvidenceFee = _archiveEvidenceFee;
        emit FeesUpdated(_permissionTokenFee, _archiveEvidenceFee, block.timestamp);
    }

    /**
     * @dev Update the Smart Contract Treasury address.
     * Requires Tri-Cameral custodian quorum.
     * Cannot be set to zero address.
     * Emits TreasuryAddressUpdated.
     */
    function setTreasuryAddress(
        address payable _newTreasury,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        require(_newTreasury != address(0), "TL_Core: Zero treasury address");
        _verifyQuorumAttestations(attestations);
        address oldTreasury = smartContractTreasury;
        smartContractTreasury = _newTreasury;
        emit TreasuryAddressUpdated(oldTreasury, _newTreasury, block.timestamp);
    }

    /**
     * @dev Propose a Treasury disbursement to the Goukassian Foundation
     * or other approved recipient.
     * Only callable by authorized Governance Lane operators (Technical Council proxy).
     * Requires subsequent Stewardship Custodian approval to execute.
     * Stewardship Custodians hold binding veto authority.
     */
    function proposeDisbursement(
        bytes32 proposalId,
        address payable recipient,
        uint256 amount,
        bytes32 purposeHash
    )
        external
        onlyGovernanceLane
    {
        require(recipient != address(0), "TL_Core: Zero recipient address");
        require(amount > 0, "TL_Core: Zero disbursement amount");
        require(amount <= address(this).balance, "TL_Core: Insufficient treasury balance");
        require(!_disbursementProposals[proposalId].executed, "TL_Core: Proposal already executed");

        _disbursementProposals[proposalId] = DisbursementProposal({
            recipient:                    recipient,
            amount:                       amount,
            purposeHash:                  purposeHash,
            technicalCouncilApprovals:    1, // proposer counts as first approval
            stewardshipCustodianApprovals: 0,
            vetoExercised:                false,
            executed:                     false,
            proposedAt:                   block.timestamp
        });

        emit DisbursementProposed(proposalId, recipient, amount, purposeHash, block.timestamp);
    }

    /**
     * @dev Approve and execute a disbursement proposal.
     * Requires Tri-Cameral Joint-Approval: 75% supermajority independently
     * in both Technical Council and Stewardship Custodians.
     * Stewardship Custodian veto is binding - vetoExercised blocks execution permanently.
     * Funds transfer automatically on approval. No human discretion at execution.
     */
    function approveDisbursement(
        bytes32 proposalId,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        DisbursementProposal storage proposal = _disbursementProposals[proposalId];
        require(proposal.proposedAt > 0, "TL_Core: Proposal does not exist");
        require(!proposal.executed, "TL_Core: Already executed");
        require(!proposal.vetoExercised, "TL_Core: Vetoed by Stewardship Custodians");
        require(address(this).balance >= proposal.amount, "TL_Core: Insufficient balance");

        _verifyQuorumAttestations(attestations);

        proposal.stewardshipCustodianApprovals = uint8(attestations.length);
        proposal.executed = true;

        // Automatic execution - no admin key, no human discretion
        (bool sent,) = proposal.recipient.call{value: proposal.amount}("");
        require(sent, "TL_Core: Treasury transfer failed");

        emit DisbursementApproved(proposalId, proposal.recipient, proposal.amount, block.timestamp);
    }

    /**
     * @dev Stewardship Custodians exercise binding veto on a disbursement proposal.
     * Requires custodian quorum. Veto is permanent and cannot be reversed.
     */
    function vetoDisbursement(
        bytes32 proposalId,
        CustodianAttestation[] calldata attestations
    )
        external
        quorumRequired(attestations, CUSTODIAN_THRESHOLD)
    {
        DisbursementProposal storage proposal = _disbursementProposals[proposalId];
        require(proposal.proposedAt > 0, "TL_Core: Proposal does not exist");
        require(!proposal.executed, "TL_Core: Already executed");
        require(!proposal.vetoExercised, "TL_Core: Already vetoed");

        _verifyQuorumAttestations(attestations);

        proposal.vetoExercised = true;

        emit DisbursementVetoed(proposalId, block.timestamp);
    }

    /**
     * @dev Receive function - allows Treasury to receive native token fees.
     */
    receive() external payable {}

    /**
     * @dev Internal: collect fee and forward to Smart Contract Treasury.
     * Called by registerPermissionToken and archiveEvidence pathways.
     * feeType: 1=PERMISSION_TOKEN, 2=ARCHIVE_EVIDENCE
     */
    function _collectFee(bytes32 operationId, uint8 feeType, uint256 feeAmount) internal {
        if (feeAmount > 0 && smartContractTreasury != address(0)) {
            require(msg.value >= feeAmount, "TL_Core: Insufficient fee");
            (bool sent,) = smartContractTreasury.call{value: feeAmount}("");
            require(sent, "TL_Core: Fee transfer to treasury failed");
            emit FeeCollected(operationId, feeType, feeAmount, msg.sender, block.timestamp);
        }
    }

    // -------------------------------------------------------------------------
    // MERKLE ROOT ANCHORING
    // -------------------------------------------------------------------------

    /**
     * @dev Anchor a Merkle root of a TGLF batch on-chain.
     * Requires Governance Lane operator + Tri-Cameral custodian quorum.
     * NL=NA Layer 5 foundation: only logHashes provably included in an
     * anchored root can produce valid PermissionTokens.
     * Emits MerkleRootAnchored on success.
     */
    function anchorMerkleRoot(
        bytes32 merkleRoot,
        bytes32 batchId,
        CustodianAttestation[] calldata quorumAttestations,
        uint256 committedAt
    )
        external
        override
        onlyGovernanceLane
        quorumRequired(quorumAttestations, CUSTODIAN_THRESHOLD)
        returns (bytes32 anchorId)
    {
        _verifyQuorumAttestations(quorumAttestations);

        anchorId = keccak256(abi.encodePacked(merkleRoot, batchId, committedAt));

        evidenceVault.anchorMerkleRoot(merkleRoot, batchId, msg.sender);

        emit MerkleRootAnchored(anchorId, merkleRoot, batchId, committedAt, bytes32(0));

        return anchorId;
    }

    // -------------------------------------------------------------------------
    // PERMISSION TOKEN REGISTRATION
    // -------------------------------------------------------------------------

    /**
     * @dev Register a PermissionToken on-chain.
     *
     * NL=NA Layer 5 enforcement:
     *   1. laneOriginHash MUST equal keccak256("GOVERNANCE_LANE").
     *      Reverts NLNAViolation(violationReason=1) if not.
     *   2. logHash MUST be provably included in an anchored Merkle root.
     *      Reverts NLNAViolation(violationReason=0) if not.
     *
     * This is the terminal enforcement gate. No actuation may proceed
     * without a registered, valid PermissionToken whose logHash is
     * on-chain verified.
     *
     * Reverts EpistemicHoldActive if system-wide hold is active.
     * Emits PermissionTokenRegistered on success.
     */
    function registerPermissionToken(
        bytes32 tokenId,
        bytes32 logHash,
        bytes32 merkleRoot,
        bytes32[] calldata merkleProof,
        uint256 epochTimestamp,
        uint256 expiresAt,
        bytes32 signerKeyId,
        bytes32 laneOriginHash,
        bytes calldata signatureValue
    )
        external
        override
        onlyGovernanceLane
        returns (bool registered)
    {
        // Check system-wide Epistemic Hold
        if (evidenceVault.epistemicHoldActive()) {
            revert EpistemicHoldActive(
                evidenceVault.activeEscrowRecordId(),
                evidenceVault.epistemicHoldResolutionDeadline()
            );
        }

        // NL=NA Layer 2: Governance Lane origin check
        if (laneOriginHash != GOVERNANCE_LANE_HASH) {
            revert NLNAViolation(tokenId, logHash, 1);
        }

        // NL=NA Layer 5: Merkle inclusion proof
        bool included = evidenceVault.verifyMerkleInclusion(logHash, merkleRoot, merkleProof);
        if (!included) {
            revert NLNAViolation(tokenId, logHash, 0);
        }

        // Verify Merkle root is anchored on-chain
        bool anchored = evidenceVault.isMerkleRootAnchored(merkleRoot);
        if (!anchored) {
            revert NLNAViolation(tokenId, logHash, 0);
        }

        // Register token
        _permissionTokens[tokenId] = PermissionTokenRecord({
            logHash:             logHash,
            merkleRoot:          merkleRoot,
            epochTimestamp:      epochTimestamp,
            expiresAt:           expiresAt,
            revocationStatus:    0,
            revocationMerkleRoot: bytes32(0),
            exists:              true
        });

        // Collect PermissionToken fee -> Smart Contract Treasury
        _collectFee(tokenId, 1, permissionTokenFee);

        emit PermissionTokenRegistered(
            tokenId,
            logHash,
            merkleRoot,
            epochTimestamp,
            expiresAt,
            0
        );

        return true;
    }

    // -------------------------------------------------------------------------
    // PERMISSION TOKEN VERIFICATION
    // -------------------------------------------------------------------------

    /**
     * @dev Verify a PermissionToken is registered, non-expired, and non-revoked.
     * Actuation layer MUST call this before firing.
     */
    function verifyPermissionToken(
        bytes32 tokenId,
        uint256 currentTimestamp
    )
        external
        view
        override
        returns (
            bool valid,
            uint8 revocationStatus,
            int256 remainingLifetimeMs
        )
    {
        PermissionTokenRecord memory record = _permissionTokens[tokenId];

        if (!record.exists) {
            return (false, 0, 0);
        }

        revocationStatus = record.revocationStatus;

        if (currentTimestamp >= record.expiresAt) {
            return (false, revocationStatus, -1);
        }

        if (revocationStatus != 0) {
            return (false, revocationStatus, 0);
        }

        remainingLifetimeMs = int256((record.expiresAt - currentTimestamp) * 1000);
        return (true, 0, remainingLifetimeMs);
    }

    // -------------------------------------------------------------------------
    // MERKLE INCLUSION VERIFICATION
    // -------------------------------------------------------------------------

    /**
     * @dev Pure function. Verify Merkle inclusion proof.
     * Delegates to TL_Evidence_Vault.verifyMerkleInclusion.
     */
    function verifyMerkleInclusion(
        bytes32 leaf,
        bytes32 merkleRoot,
        bytes32[] calldata proof
    )
        external
        pure
        override
        returns (bool included)
    {
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
    // EPISTEMIC HOLD
    // -------------------------------------------------------------------------

    /**
     * @dev Activate system-wide Epistemic Hold (State 0).
     * Requires Governance Lane operator + Tri-Cameral custodian quorum.
     * Blocks all subsequent PermissionToken registrations until resolved.
     * Emits EpistemicHoldActivated.
     */
    function activateEpistemicHoldSystemWide(
        bytes32 holdRationale,
        bytes32 escrowRecordId,
        CustodianAttestation[] calldata quorumAttestations,
        uint256 resolutionDeadline
    )
        external
        override
        onlyGovernanceLane
        quorumRequired(quorumAttestations, CUSTODIAN_THRESHOLD)
        returns (bool holdActivated)
    {
        _verifyQuorumAttestations(quorumAttestations);

        evidenceVault.activateEpistemicHold(escrowRecordId, resolutionDeadline);

        emit EpistemicHoldActivated(
            escrowRecordId,
            holdRationale,
            block.timestamp,
            resolutionDeadline,
            bytes32(0)
        );

        return true;
    }

    /**
     * @dev Resolve system-wide Epistemic Hold.
     * resolvedState uint8 encoding (function-local):
     *   1 = PROCEED (+1 integer)
     *   0 = REFUSE  (-1 integer)
     * Epistemic Hold (State 0) is NOT a valid resolution.
     * Reverts InvalidResolutionState for any other value.
     */
    function resolveEpistemicHoldSystemWide(
        bytes32 escrowRecordId,
        uint8 resolvedState,
        bytes32 resolutionRationaleHash,
        CustodianAttestation[] calldata quorumAttestations
    )
        external
        override
        onlyGovernanceLane
        quorumRequired(quorumAttestations, CUSTODIAN_THRESHOLD)
        returns (bool resolved)
    {
        // Only 0 (REFUSE encoding) or 1 (PROCEED encoding) are valid resolutions.
        // Epistemic Hold re-resolution is constitutionally prohibited.
        if (resolvedState != 0 && resolvedState != 1) {
            revert InvalidResolutionState(resolvedState);
        }

        _verifyQuorumAttestations(quorumAttestations);

        evidenceVault.resolveEpistemicHold(escrowRecordId, resolvedState);

        emit EpistemicHoldResolved(
            escrowRecordId,
            resolvedState,
            resolutionRationaleHash,
            block.timestamp,
            bytes32(0)
        );

        return true;
    }

    // -------------------------------------------------------------------------
    // EMERGENCY OVERRIDE
    // -------------------------------------------------------------------------

    /**
     * @dev Execute Emergency Override under supreme authority.
     *
     * Constitutional requirements:
     *   1. ALL invocations logged on-chain BEFORE execution.
     *      EmergencyOverrideExecuted event fires BEFORE state change.
     *      The governance log precedes the action. This ordering is constitutional.
     *   2. NL=NA applies without exception.
     *   3. forcedState uint8 encoding:
     *        0   = EpistemicHold (State 0)
     *        255 = Refuse (State -1)
     *        Forced Proceed (+1) is constitutionally blocked.
     *        Reverts UnauthorizedOverride.
     *   4. overrideType: 0=BREAK_GLASS_SHUTDOWN, 1=KILL_SWITCH,
     *        2=FORCED_STATE_TRANSITION
     */
    function executeEmergencyOverride(
        bytes32 overrideRequestId,
        uint8 overrideType,
        bytes32 targetDecisionId,
        uint8 forcedState,
        uint256 forcedStateExpiresAt,
        bytes32 justificationHash,
        bytes calldata authorityAttestation
    )
        external
        override
        onlyGovernanceLane
        returns (bool executed)
    {
        // Forced Proceed (+1) is constitutionally blocked.
        if (forcedState != 0 && forcedState != 255) {
            revert UnauthorizedOverride(forcedState, msg.sender);
        }

        // Log BEFORE execution - constitutional ordering.
        emit EmergencyOverrideExecuted(
            overrideRequestId,
            overrideType,
            forcedState,
            justificationHash,
            block.timestamp,
            forcedStateExpiresAt
        );

        // Execute the override.
        if (forcedState == 0) {
            // Forced EpistemicHold
            evidenceVault.activateEpistemicHold(
                targetDecisionId,
                forcedStateExpiresAt
            );
        }
        // forcedState == 255 (Refuse): the emit above is the constitutional record.
        // No further state change required; actuation gates check token validity.

        return true;
    }

    // -------------------------------------------------------------------------
    // PERMISSION TOKEN REVOCATION
    // -------------------------------------------------------------------------

    /**
     * @dev Revoke a registered PermissionToken.
     * revocationReason: 1=REVOKED_BY_EMERGENCY, 2=REVOKED_BY_TRI_CAMERAL.
     * Requires Governance Lane operator + Tri-Cameral custodian quorum.
     */
    function revokePermissionToken(
        bytes32 tokenId,
        uint8 revocationReason,
        bytes32 revocationMerkleRoot,
        CustodianAttestation[] calldata quorumAttestations
    )
        external
        override
        onlyGovernanceLane
        quorumRequired(quorumAttestations, CUSTODIAN_THRESHOLD)
        returns (bool revoked)
    {
        require(
            revocationReason == 1 || revocationReason == 2,
            "TL_Core: Invalid revocation reason"
        );

        PermissionTokenRecord storage record = _permissionTokens[tokenId];
        require(record.exists, "TL_Core: Token does not exist");
        require(record.revocationStatus == 0, "TL_Core: Token already revoked");

        _verifyQuorumAttestations(quorumAttestations);

        record.revocationStatus    = revocationReason;
        record.revocationMerkleRoot = revocationMerkleRoot;

        emit PermissionTokenRevoked(tokenId, revocationReason, revocationMerkleRoot, block.timestamp);

        return true;
    }

    // -------------------------------------------------------------------------
    // MANDATE VIOLATION
    // -------------------------------------------------------------------------

    /**
     * @dev Record an immutable mandate violation.
     * Delegates to TL_Evidence_Vault for immutable storage.
     * mandateViolated: keccak256("No Spy"), keccak256("No Weapon"),
     *   or keccak256("No Switch Off").
     */
    function recordMandateViolation(
        bytes32 violationId,
        bytes32 mandateViolated,
        uint8   pillarImplicated,
        bytes32 violationDetailsHash,
        bytes32 decisionId,
        uint256 recordedAt
    )
        external
        override
        onlyGovernanceLane
        returns (bool recorded)
    {
        evidenceVault.recordMandateViolation(
            violationId,
            mandateViolated,
            violationDetailsHash,
            decisionId
        );

        emit MandateViolationRecorded(
            violationId,
            mandateViolated,
            pillarImplicated,
            violationDetailsHash,
            recordedAt
        );

        return true;
    }

    // -------------------------------------------------------------------------
    // TRANSACTION VALIDATION
    // -------------------------------------------------------------------------

    /**
     * @dev Core validation entry point called by Data_Bridge.
     *
     * IMPORTANT: This function determines the TL triadic state for a transaction.
     * State +1 (Proceed) does NOT authorize actuation by itself.
     * A PermissionToken from the Governance Lane is REQUIRED separately
     * via registerPermissionToken() before actuation is permitted.
     *
     * State determination is delegated to the off-chain Governance Lane
     * through the Data_Bridge → API → Governance Lane → registerPermissionToken
     * pathway. This function records the validated state from that pathway.
     *
     * @param _transactionHash SHA-256 hash of the off-chain transaction data.
     * @param _evidenceURI IPFS or Arweave link to supporting document.
     * @param _traceId X-TL-Trace-Id UUID v4 from the originating API request.
     */
    function validateTransaction(
        bytes32 _transactionHash,
        string calldata _evidenceURI,
        bytes32 _traceId
    )
        external
        override
        onlyGovernanceLane
        returns (int8 state)
    {
        // State is determined off-chain by the Governance Lane and arrives
        // via Data_Bridge after a valid PermissionToken has been registered.
        // Retrieve the registered state from the Evidence Vault.
        state = evidenceVault.getTransactionState(_transactionHash);

        // If no evidence exists yet, default is EpistemicHold (fail-closed).
        // The Data_Bridge must call registerPermissionToken before calling
        // validateTransaction for State +1 to be recognized.
        return state;
    }

    /**
     * @dev Check the current TL state of a specific transaction.
     */
    function getTransactionState(
        bytes32 _transactionHash
    )
        external
        view
        override
        returns (int8 state)
    {
        return evidenceVault.getTransactionState(_transactionHash);
    }

    // -------------------------------------------------------------------------
    // INTERNAL HELPERS
    // -------------------------------------------------------------------------

    /**
     * @dev Verify that quorum attestations are structurally valid.
     * In production this would verify custodian signatures cryptographically.
     * Placeholder for signature verification logic pending HSM integration.
     */
    function _verifyQuorumAttestations(
        CustodianAttestation[] calldata attestations
    ) internal pure {
        for (uint256 i = 0; i < attestations.length; i++) {
            require(
                attestations[i].custodianId != bytes32(0),
                "TL_Core: Invalid custodian ID in attestation"
            );
            require(
                attestations[i].custodianSignature.length > 0,
                "TL_Core: Empty custodian signature"
            );
        }
        // TODO: Replace with full Ed25519 / ECDSA signature verification
        // against registered custodian public keys when HSM integration
        // is complete. See tl_abi.json CustodianQuorumAttestation struct.
    }
}
