// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ITL_Validator.sol";

/**
 * @title TL_Evidence_Vault
 * @dev Immutable storage for financial proofs. 
 * Implements "No Log = No Action" by requiring storage before logic execution.
 */
contract TL_Evidence_Vault {

    struct EvidenceLog {
        uint256 timestamp;
        string uri;        // Link to off-chain document (PDF/JSON)
        address submitter; // The auditor or bridge that submitted it
        int8 finalState;   // The locked TML state (+1, 0, -1)
    }

    // Maps Transaction Hash -> Evidence Log
    mapping(bytes32 => EvidenceLog) private vault;
    
    address public ledgerCore;

    modifier onlyCore() {
        require(msg.sender == ledgerCore, "TL_Vault: Only Ledger Core can write evidence");
        _;
    }

    constructor() {}

    function setLedgerCore(address _core) external {
        require(ledgerCore == address(0), "TL_Vault: Core already set");
        ledgerCore = _core;
    }

    /**
     * @dev Stores the evidence permanently. 
     * Cannot be overwritten.
     */
    function archiveEvidence(bytes32 _txHash, string calldata _uri, address _submitter, int8 _state) external onlyCore {
        require(vault[_txHash].timestamp == 0, "TL_Vault: Log already exists (Immutability Violation)");
        
        vault[_txHash] = EvidenceLog({
            timestamp: block.timestamp,
            uri: _uri,
            submitter: _submitter,
            finalState: _state
        });
    }

    function getEvidence(bytes32 _txHash) external view returns (uint256, string memory, address, int8) {
        EvidenceLog memory log = vault[_txHash];
        return (log.timestamp, log.uri, log.submitter, log.finalState);
    }
}
