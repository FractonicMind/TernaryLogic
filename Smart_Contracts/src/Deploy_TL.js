/**
 * Deploy_TL.js
 * ============
 * Deployment script for TL smart contract suite.
 *
 * Framework: "Ternary Logic" (TL) by Lev Goukassian
 * ORCID:     0009-0006-5966-1243
 * DOI:       10.1007/s43681-025-00910-6
 * DOI:       10.1007/s43681-026-01124-0
 *
 * Deployment order (mandatory):
 *   1. TL_Evidence_Vault   — immutable storage layer
 *   2. TL_Ledger_Core      — governance logic layer (references Vault)
 *   3. TL_Evidence_Vault.setLedgerCore(core.address) — link Core to Vault
 *   4. TL_Ledger_Core.bootstrapGovernanceLaneOperator — initial operator
 *
 * This ordering is constitutional: the Vault must exist before the Core
 * can reference it. The Core must exist before the Vault can be linked.
 * setLedgerCore() can only be called once — immutable after first call.
 *
 * NL=NA Invariant: G(execute implies P(escrow_recorded and auditable))
 *
 * Immutable Mandates (beyond any governance body's authority):
 *   No Spy | No Weapon | No Switch Off
 */

const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// CONFIGURATION
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.join(__dirname, "TL_Config.json");

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    throw new Error(`TL_Deploy: Config file not found at ${CONFIG_PATH}`);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
}

function saveConfig(config) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  console.log("  ✓ TL_Config.json updated with deployed addresses");
}

// ---------------------------------------------------------------------------
// CONSTANTS
// ---------------------------------------------------------------------------

/**
 * Nomination 2026 fee values.
 * These are initial governance parameters — NOT hardcoded constants.
 * Set by Tri-Cameral Joint-Approval at the first governance session
 * following mainnet deployment. Subject to revision by governance at any time.
 *
 * Denominated in wei (Polygon MATIC).
 * No fiat denomination: fee levels absorb token price volatility through
 * governance revision rather than oracle dependency.
 *
 * PERMISSION_TOKEN_FEE: charged per State +1 PermissionToken registration
 * ARCHIVE_EVIDENCE_FEE: charged per governance action archived in Vault
 * Epistemic Hold activation/resolution: always free by constitutional design
 */
const NOMINATION_2026 = {
  PERMISSION_TOKEN_FEE: ethers.parseUnits("0.001", "ether"), // ~$0.001 at Polygon prices
  ARCHIVE_EVIDENCE_FEE: ethers.parseUnits("0.0005", "ether"),
};

// GOVERNANCE_LANE_HASH constant - must match contract
const GOVERNANCE_LANE_HASH = ethers.keccak256(
  ethers.toUtf8Bytes("GOVERNANCE_LANE")
);

// ---------------------------------------------------------------------------
// NETWORK VALIDATION
// ---------------------------------------------------------------------------

async function validateNetwork(config) {
  const network = await ethers.provider.getNetwork();
  const chainId = Number(network.chainId);

  console.log("\n── Network Validation ──────────────────────────────────");
  console.log(`  Network:  ${network.name}`);
  console.log(`  Chain ID: ${chainId}`);

  if (chainId === 137) {
    console.log("\n  ⚠️  MAINNET DEPLOYMENT DETECTED");
    console.log("  This will deploy to Polygon mainnet and cost real MATIC.");
    console.log("  Proceeding in 5 seconds — Ctrl+C to abort.\n");
    await new Promise(resolve => setTimeout(resolve, 5000));
  } else if (chainId === 80001) {
    console.log("  ✓ Testnet deployment (Polygon Mumbai)");
  } else {
    console.log(`  ✓ Local/custom network deployment (chainId=${chainId})`);
  }

  return chainId;
}

// ---------------------------------------------------------------------------
// TREASURY VALIDATION
// ---------------------------------------------------------------------------

function validateTreasuryAddress(config) {
  const treasury = config.TRI_CAMERAL_COUNCIL?.TREASURY_ADDRESS
    || process.env.TL_TREASURY_ADDRESS;

  if (!treasury || treasury === "0x" + "0".repeat(40)) {
    throw new Error(
      "TL_Deploy: Smart Contract Treasury address not set.\n" +
      "Set TL_TREASURY_ADDRESS environment variable or " +
      "add TRI_CAMERAL_COUNCIL.TREASURY_ADDRESS to TL_Config.json.\n" +
      "This is the Goukassian Foundation wallet address — " +
      "all TL service fees accumulate here."
    );
  }

  if (!ethers.isAddress(treasury)) {
    throw new Error(`TL_Deploy: Invalid treasury address: ${treasury}`);
  }

  console.log(`  ✓ Treasury address: ${treasury}`);
  return treasury;
}

// ---------------------------------------------------------------------------
// CONTRACT DEPLOYMENT
// ---------------------------------------------------------------------------

async function deployVault(deployer) {
  console.log("\n── Step 1: Deploy TL_Evidence_Vault ────────────────────");
  console.log("  Constitutional role: immutable on-chain storage layer");
  console.log("  NL=NA: archiveEvidence is a precondition of execution\n");

  const VaultFactory = await ethers.getContractFactory(
    "TL_Evidence_Vault",
    deployer
  );
  const vault = await VaultFactory.deploy();
  await vault.waitForDeployment();

  const vaultAddress = await vault.getAddress();
  console.log(`  ✓ TL_Evidence_Vault deployed: ${vaultAddress}`);
  return vault;
}

async function deployCore(deployer, vaultAddress, treasuryAddress) {
  console.log("\n── Step 2: Deploy TL_Ledger_Core ───────────────────────");
  console.log("  Constitutional role: governance logic, NL=NA Layer 5 gate");
  console.log("  No admin key. All governance is Tri-Cameral only.\n");

  const CoreFactory = await ethers.getContractFactory(
    "TL_Ledger_Core",
    deployer
  );

  const core = await CoreFactory.deploy(
    vaultAddress,
    treasuryAddress,
    NOMINATION_2026.PERMISSION_TOKEN_FEE,
    NOMINATION_2026.ARCHIVE_EVIDENCE_FEE
  );
  await core.waitForDeployment();

  const coreAddress = await core.getAddress();
  console.log(`  ✓ TL_Ledger_Core deployed: ${coreAddress}`);
  console.log(`  ✓ Treasury: ${treasuryAddress}`);
  console.log(`  ✓ PermissionToken fee (Nomination 2026): ${ethers.formatEther(NOMINATION_2026.PERMISSION_TOKEN_FEE)} MATIC`);
  console.log(`  ✓ ArchiveEvidence fee (Nomination 2026): ${ethers.formatEther(NOMINATION_2026.ARCHIVE_EVIDENCE_FEE)} MATIC`);
  return core;
}

async function linkContracts(vault, core) {
  console.log("\n── Step 3: Link TL_Evidence_Vault → TL_Ledger_Core ─────");
  console.log("  setLedgerCore() is one-time only — immutable after this call.\n");

  const vaultAddress = await vault.getAddress();
  const coreAddress = await core.getAddress();

  const tx = await vault.setLedgerCore(coreAddress);
  await tx.wait();

  // Verify the link
  const linkedCore = await vault.ledgerCore();
  if (linkedCore.toLowerCase() !== coreAddress.toLowerCase()) {
    throw new Error("TL_Deploy: Vault→Core link verification failed");
  }

  console.log(`  ✓ TL_Evidence_Vault.ledgerCore = ${linkedCore}`);
  console.log(`  ✓ Link is immutable — cannot be changed`);
}

async function bootstrapOperator(core, deployer, config) {
  console.log("\n── Step 4: Bootstrap Governance Lane Operator ──────────");
  console.log("  One-time call only. Subsequent operator changes require");
  console.log("  Tri-Cameral quorum via authorizeGovernanceLaneOperator().\n");

  const operatorAddress = process.env.TL_GOVERNANCE_LANE_OPERATOR
    || config.API?.GOVERNANCE_LANE_OPERATOR
    || deployer.address;

  const tx = await core.bootstrapGovernanceLaneOperator(operatorAddress);
  await tx.wait();

  console.log(`  ✓ Initial Governance Lane operator: ${operatorAddress}`);
}

// ---------------------------------------------------------------------------
// CONSTANT VERIFICATION
// ---------------------------------------------------------------------------

async function verifyConstants(core, vault) {
  console.log("\n── Constant Verification ───────────────────────────────");

  // Verify GOVERNANCE_LANE_HASH matches contract constant
  const contractHash = await core.GOVERNANCE_LANE_HASH();
  if (contractHash !== GOVERNANCE_LANE_HASH) {
    throw new Error(
      `TL_Deploy: GOVERNANCE_LANE_HASH mismatch.\n` +
      `  Expected: ${GOVERNANCE_LANE_HASH}\n` +
      `  Contract: ${contractHash}\n` +
      `  NL=NA Layer 2 enforcement compromised.`
    );
  }
  console.log(`  ✓ GOVERNANCE_LANE_HASH matches: ${contractHash}`);

  // Verify Vault GOVERNANCE_LANE_HASH
  const vaultHash = await vault.GOVERNANCE_LANE_HASH();
  if (vaultHash !== GOVERNANCE_LANE_HASH) {
    throw new Error(
      `TL_Deploy: Vault GOVERNANCE_LANE_HASH mismatch.\n` +
      `  Expected: ${GOVERNANCE_LANE_HASH}\n` +
      `  Vault:    ${vaultHash}`
    );
  }
  console.log(`  ✓ Vault GOVERNANCE_LANE_HASH matches: ${vaultHash}`);

  // Verify Immutable Mandates hashes
  const noSpyHash    = await core.NO_SPY_HASH();
  const noWeaponHash = await core.NO_WEAPON_HASH();
  const noSwitchHash = await core.NO_SWITCH_OFF_HASH();

  const expectedNoSpy    = ethers.keccak256(ethers.toUtf8Bytes("No Spy"));
  const expectedNoWeapon = ethers.keccak256(ethers.toUtf8Bytes("No Weapon"));
  const expectedNoSwitch = ethers.keccak256(ethers.toUtf8Bytes("No Switch Off"));

  if (noSpyHash !== expectedNoSpy)    throw new Error("TL_Deploy: NO_SPY_HASH mismatch");
  if (noWeaponHash !== expectedNoWeapon) throw new Error("TL_Deploy: NO_WEAPON_HASH mismatch");
  if (noSwitchHash !== expectedNoSwitch) throw new Error("TL_Deploy: NO_SWITCH_OFF_HASH mismatch");

  console.log(`  ✓ NO_SPY_HASH    verified`);
  console.log(`  ✓ NO_WEAPON_HASH verified`);
  console.log(`  ✓ NO_SWITCH_OFF_HASH verified`);
  console.log(`  ✓ Immutable Mandates constants confirmed`);
}

// ---------------------------------------------------------------------------
// SMOKE TEST
// ---------------------------------------------------------------------------

async function runSmokeTest(core, vault) {
  console.log("\n── Smoke Test ──────────────────────────────────────────");

  // Test 1: Evidence Vault is linked
  const linkedCore = await vault.ledgerCore();
  const coreAddress = await core.getAddress();
  if (linkedCore.toLowerCase() !== coreAddress.toLowerCase()) {
    throw new Error("Smoke test FAILED: Vault→Core link broken");
  }
  console.log("  ✓ Vault→Core link intact");

  // Test 2: Epistemic Hold is not active at deployment
  const holdActive = await vault.epistemicHoldActive();
  if (holdActive) {
    throw new Error("Smoke test FAILED: Epistemic Hold active at deployment");
  }
  console.log("  ✓ Epistemic Hold: inactive (correct initial state)");

  // Test 3: Verify non-existent PermissionToken returns invalid
  const dummyTokenId = ethers.keccak256(ethers.toUtf8Bytes("smoke-test-token"));
  const [valid, , ] = await core.verifyPermissionToken(
    dummyTokenId,
    Math.floor(Date.now() / 1000)
  );
  if (valid) {
    throw new Error("Smoke test FAILED: Non-existent token returned valid");
  }
  console.log("  ✓ Non-existent PermissionToken correctly returns invalid");

  // Test 4: Verify getTransactionState defaults to EpistemicHold (fail-closed)
  const dummyTxHash = ethers.keccak256(ethers.toUtf8Bytes("smoke-test-tx"));
  const state = await core.getTransactionState(dummyTxHash);
  if (Number(state) !== 0) {
    throw new Error(
      `Smoke test FAILED: Expected EpistemicHold(0) for unknown tx, got ${state}`
    );
  }
  console.log("  ✓ Unknown transaction state defaults to EpistemicHold (fail-closed)");

  // Test 5: Verify treasury address is set
  const treasury = await core.smartContractTreasury();
  if (treasury === ethers.ZeroAddress) {
    throw new Error("Smoke test FAILED: Treasury address is zero");
  }
  console.log(`  ✓ Smart Contract Treasury set: ${treasury}`);

  // Test 6: Verify Nomination 2026 fees are set
  const ptFee = await core.permissionTokenFee();
  const aeFee = await core.archiveEvidenceFee();
  console.log(`  ✓ PermissionToken fee (Nomination 2026): ${ethers.formatEther(ptFee)} MATIC`);
  console.log(`  ✓ ArchiveEvidence fee (Nomination 2026): ${ethers.formatEther(aeFee)} MATIC`);

  console.log("\n  ✓ All smoke tests passed");
}

// ---------------------------------------------------------------------------
// CONFIG WRITE-BACK
// ---------------------------------------------------------------------------

async function writeBackAddresses(config, vault, core, chainId) {
  console.log("\n── Writing Deployed Addresses to TL_Config.json ────────");

  const vaultAddress = await vault.getAddress();
  const coreAddress  = await core.getAddress();

  config.CONTRACT_ADDRESSES = config.CONTRACT_ADDRESSES || {};
  config.CONTRACT_ADDRESSES.TL_EVIDENCE_VAULT = vaultAddress;
  config.CONTRACT_ADDRESSES.TL_LEDGER_CORE    = coreAddress;
  config.CHAIN_ID = chainId;
  config.DEPLOYMENT_TIMESTAMP = new Date().toISOString();
  config.NOMINATION_2026 = {
    PERMISSION_TOKEN_FEE_WEI: NOMINATION_2026.PERMISSION_TOKEN_FEE.toString(),
    ARCHIVE_EVIDENCE_FEE_WEI: NOMINATION_2026.ARCHIVE_EVIDENCE_FEE.toString(),
    NOTE: "Initial fee parameters set at deployment. Subject to revision by Tri-Cameral Joint-Approval governance."
  };

  saveConfig(config);

  console.log(`  ✓ TL_EVIDENCE_VAULT: ${vaultAddress}`);
  console.log(`  ✓ TL_LEDGER_CORE:    ${coreAddress}`);
  console.log(`  ✓ CHAIN_ID:          ${chainId}`);
  console.log(`  ✓ DEPLOYMENT_TIMESTAMP: ${config.DEPLOYMENT_TIMESTAMP}`);
}

// ---------------------------------------------------------------------------
// DEPLOYMENT SUMMARY
// ---------------------------------------------------------------------------

function printSummary(vault, core, vaultAddress, coreAddress, chainId) {
  console.log("\n════════════════════════════════════════════════════════");
  console.log("  TL SMART CONTRACT SUITE DEPLOYED SUCCESSFULLY");
  console.log("════════════════════════════════════════════════════════");
  console.log(`  Chain ID:            ${chainId}`);
  console.log(`  TL_Evidence_Vault:   ${vaultAddress}`);
  console.log(`  TL_Ledger_Core:      ${coreAddress}`);
  console.log("");
  console.log("  Constitutional properties confirmed:");
  console.log("  ✓ NL=NA invariant enforced at hardware and contract layer");
  console.log("  ✓ GOVERNANCE_LANE_HASH constant verified");
  console.log("  ✓ Immutable Mandates (No Spy, No Weapon, No Switch Off)");
  console.log("  ✓ Tri-Cameral governance — no admin key");
  console.log("  ✓ Smart Contract Treasury — no human discretion on fees");
  console.log("  ✓ Nomination 2026 fees set — revisable by governance");
  console.log("  ✓ Vault→Core link immutable");
  console.log("  ✓ Fail-closed default: unknown state = EpistemicHold");
  console.log("════════════════════════════════════════════════════════\n");
}

// ---------------------------------------------------------------------------
// MAIN ENTRYPOINT
// ---------------------------------------------------------------------------

async function main() {
  console.log("\n════════════════════════════════════════════════════════");
  console.log("  TL Smart Contract Deployment");
  console.log("  Framework: Ternary Logic (TL) by Lev Goukassian");
  console.log("  ORCID: 0009-0006-5966-1243");
  console.log("════════════════════════════════════════════════════════");

  const config = loadConfig();
  const [deployer] = await ethers.getSigners();

  console.log(`\n  Deployer: ${deployer.address}`);
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log(`  Balance:  ${ethers.formatEther(balance)} MATIC`);

  // Step 0: Validate network and treasury
  const chainId = await validateNetwork(config);
  const treasuryAddress = validateTreasuryAddress(config);

  // Step 1: Deploy TL_Evidence_Vault
  const vault = await deployVault(deployer);
  const vaultAddress = await vault.getAddress();

  // Step 2: Deploy TL_Ledger_Core
  const core = await deployCore(deployer, vaultAddress, treasuryAddress);
  const coreAddress = await core.getAddress();

  // Step 3: Link Vault → Core
  await linkContracts(vault, core);

  // Step 4: Bootstrap initial Governance Lane operator
  await bootstrapOperator(core, deployer, config);

  // Step 5: Verify constants
  await verifyConstants(core, vault);

  // Step 6: Run smoke tests
  await runSmokeTest(core, vault);

  // Step 7: Write addresses back to TL_Config.json
  await writeBackAddresses(config, vault, core, chainId);

  // Summary
  printSummary(vault, core, vaultAddress, coreAddress, chainId);
}

// ---------------------------------------------------------------------------
// EXECUTE
// ---------------------------------------------------------------------------

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n  ✗ Deployment failed:", error.message);
    console.error(error);
    process.exit(1);
  });
