{
  "RPC_URL": "https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
  "CHAIN_ID": 137,
  "CHAIN_ID_TESTNET": 80001,
  "CHAIN_NOTE": "137 = Polygon mainnet. Override with CHAIN_ID_TESTNET for testnet deployments.",
  "PRIVATE_KEY": "YOUR_WALLET_PRIVATE_KEY_HERE",

  "CONTRACT_ADDRESSES": {
    "TL_LEDGER_CORE": "0x0000000000000000000000000000000000000000",
    "TL_EVIDENCE_VAULT": "0x0000000000000000000000000000000000000000",
    "ITL_VALIDATOR": "0x0000000000000000000000000000000000000000"
  },

  "API": {
    "BASE_URL": "https://your-tl-api-endpoint.example.com",
    "INFERENCE_LANE_JWT": "YOUR_TL_GOVERNANCE_JWT_HERE",
    "GOVERNANCE_LANE_JWT": "YOUR_HSM_SIGNED_JWT_HERE",
    "NLNA_GOVERNANCE_TOKEN": "YOUR_NLNA_GOVERNANCE_TOKEN_HERE",
    "HSM_KEY_ID": "YOUR_HSM_KEY_ID_HERE"
  },

  "TRI_CAMERAL_COUNCIL": {
    "TECHNICAL_COUNCIL_MEMBERS": 9,
    "TECHNICAL_COUNCIL_THRESHOLD": 7,
    "STEWARDSHIP_CUSTODIAN_MEMBERS": 11,
    "STEWARDSHIP_CUSTODIAN_THRESHOLD": 9,
    "JOINT_APPROVAL_SUPERMAJORITY": 0.75,
    "NOTE": "Joint-Approval requires 75% supermajority independently in both bodies. Stewardship Custodian veto is binding."
  },

  "GOVERNANCE_LANE": {
    "LANE_ORIGIN_PREIMAGE": "GOVERNANCE_LANE",
    "LANE_ORIGIN_HASH_NOTE": "keccak256('GOVERNANCE_LANE') - computed at contract deployment and stored as constant",
    "MAX_LIFETIME_MS": 300000,
    "JITTER_MAX_MS": 50,
    "HARD_CEILING_MS": 300
  },

  "INFERENCE_LANE": {
    "WCET_MS": 2,
    "WCET_PERCENTILE": "99.99th"
  },

  "NLNA": {
    "MERKLE_BATCH_SIZE": 1000,
    "MERKLE_BATCH_WINDOW_MS": 300000,
    "NOTE": "Every logHash must be provably included in an anchored Merkle root before a PermissionToken can be registered on-chain. NL=NA Layer 5."
  },

  "GAS": {
    "GAS_LIMIT_GOVERNANCE": 500000,
    "GAS_LIMIT_ANCHOR": 300000,
    "GAS_LIMIT_REGISTER_TOKEN": 200000,
    "GAS_LIMIT_EPISTEMIC_HOLD": 150000,
    "GAS_PRICE_GWEI": 20
  },

  "TRI_STATE_MAPPING": {
    "PROCEED": 1,
    "EPISTEMIC_HOLD": 0,
    "REFUSE": -1,
    "NOTE": "Canonical TL triadic state encoding. EpistemicHold is State 0 - a first-class constitutional state, never null, error, or timeout."
  },

  "IMMUTABLE_MANDATES": {
    "NO_SPY": true,
    "NO_WEAPON": true,
    "NO_SWITCH_OFF": true,
    "NOTE": "These three mandates cannot be modified, suspended, or reinterpreted by any governance body. Any proposal attempting to do so is void from the beginning."
  },

  "NETWORK_NOTE": "Remove PRIVATE_KEY from this file before committing to any repository. Use environment variables or a secrets manager in production."
}
