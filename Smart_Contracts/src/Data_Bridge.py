"""
Data_Bridge.py
The Synapse for Ternary Logic.
Ingests financial data, hashes it, and submits to the TL Ledger.
"""

import json
import time
from web3 import Web3
from hashlib import sha256

# --- Configuration ---
CONFIG_PATH = "TL_Config.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config["RPC_URL"]))
account = w3.eth.account.from_key(config["PRIVATE_KEY"])
contract_address = config["TL_CORE_ADDRESS"]

# Load ABI (Simplified for brevity)
CONTRACT_ABI = '[{"inputs":[{"internalType":"bytes32","name":"_transactionHash","type":"bytes32"},{"internalType":"string","name":"_evidenceURI","type":"string"}],"name":"validateTransaction","outputs":[{"internalType":"int8","name":"","type":"int8"}],"stateMutability":"nonpayable","type":"function"}]'

contract = w3.eth.contract(address=contract_address, abi=json.loads(CONTRACT_ABI))

def ingest_financial_record(record_id, amount, sender, doc_link):
    """
    Takes a raw financial record, creates a cryptographic hash,
    and submits it for Ternary Validation.
    """
    print(f"[*] Processing Record: {record_id} | Amount: {amount}")

    # 1. Create Deterministic Hash (The "Fingerprint")
    raw_data = f"{record_id}{amount}{sender}".encode('utf-8')
    tx_hash = "0x" + sha256(raw_data).hexdigest()
    
    print(f"    -> Generated Hash: {tx_hash}")

    # 2. Build Transaction
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.validateTransaction(
        tx_hash,
        doc_link
    ).build_transaction({
        'chainId': config["CHAIN_ID"],
        'gas': 200000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce,
    })

    # 3. Sign & Send
    signed_tx = w3.eth.account.sign_transaction(tx, config["PRIVATE_KEY"])
    tx_receipt = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"    -> Sent to Ledger. TxID: {w3.to_hex(tx_receipt)}")
    print("    -> Waiting for confirmation...")
    
    # 4. Wait for Receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_receipt)
    print(f"[*] Confirmed in Block {receipt.blockNumber}\n")

if __name__ == "__main__":
    # Example Usage: Ingesting a mock invoice
    ingest_financial_record("INV-2026-001", 5000.00, "Acme Corp", "ipfs://QmHash...")
