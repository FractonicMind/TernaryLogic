// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ITL_Validator
 * @dev Interface for the Ternary Logic Economic Validator.
 * Enforces the Tri-State return protocol for financial verification.
 */
interface ITL_Validator {
    
    // The Tri-State Economic Logic
    // +1: VERIFIED   (Funds matched, signatures valid, proceed to settlement)
    //  0: AUDIT_HOLD (Discrepancy found, missing receipt, 'Epistemic Hold')
    // -1: REJECTED   (Fraud detected, invalid signature, hard stop)
    enum ValidationState { REJECTED, AUDIT_HOLD, VERIFIED }

    event LogSubmitted(bytes32 indexed transactionId, int8 decision, string reason);
    event EpistemicHoldTriggered(bytes32 indexed transactionId, string reason);

    /**
     * @dev Core validation function.
     * @param _transactionHash The hash of the off-chain financial transaction.
     * @param _evidenceURI IPFS/Arweave link to the supporting document (Invoice/Receipt).
     * @return int8 The Tri-State decision (+1, 0, -1).
     */
    function validateTransaction(bytes32 _transactionHash, string calldata _evidenceURI) external returns (int8);

    /**
     * @dev Check the current state of a specific transaction ID.
     */
    function getTransactionState(bytes32 _transactionHash) external view returns (int8);
}
