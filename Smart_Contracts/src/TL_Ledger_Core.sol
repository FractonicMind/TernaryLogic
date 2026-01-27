// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ITL_Validator.sol";
import "./TL_Evidence_Vault.sol";

/**
 * @title TL_Ledger_Core
 * @dev The execution engine for Ternary Economic Logic.
 */
contract TL_Ledger_Core is ITL_Validator {

    TL_Evidence_Vault public vault;
    address public governance;
    mapping(address => bool) public authorizedAuditors;

    constructor(address _vaultAddress) {
        vault = TL_Evidence_Vault(_vaultAddress);
        governance = msg.sender;
    }

    modifier onlyAuditor() {
        require(authorizedAuditors[msg.sender], "TL_Core: Unauthorized Auditor");
        _;
    }

    function authorizeAuditor(address _auditor, bool _status) external {
        require(msg.sender == governance, "TL_Core: Only Governance");
        authorizedAuditors[_auditor] = _status;
    }

    /**
     * @dev The Heart of the System.
     * Takes a transaction and an evidence link.
     * Returns +1 (Verified), 0 (Audit Hold), or -1 (Rejected).
     */
    function validateTransaction(bytes32 _transactionHash, string calldata _evidenceURI) external override onlyAuditor returns (int8) {
        
        // 1. Simulating Logic Check (In production, this might call an Oracle)
        // For demo: We check if the hash starts with specific bytes to simulate states
        int8 decision;

        if (uint256(_transactionHash) % 3 == 0) {
            decision = 0; // Simulate AUDIT HOLD (Ambiguity)
        } else if (uint256(_transactionHash) % 3 == 1) {
            decision = 1; // Simulate VERIFIED
        } else {
            decision = -1; // Simulate REJECTED
        }

        // 2. ENFORCEMENT: No Log = No Action
        vault.archiveEvidence(_transactionHash, _evidenceURI, msg.sender, decision);

        // 3. Emit Events based on Ternary State
        if (decision == 0) {
            emit EpistemicHoldTriggered(_transactionHash, "Ambiguous Data: Manual Audit Required");
        } else {
            emit LogSubmitted(_transactionHash, decision, decision == 1 ? "Verified" : "Rejected");
        }

        return decision;
    }

    function getTransactionState(bytes32 _transactionHash) external view override returns (int8) {
        (,,, int8 state) = vault.getEvidence(_transactionHash);
        return state;
    }
}
