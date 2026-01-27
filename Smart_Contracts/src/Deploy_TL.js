// Deploy_TL.js
// Script to deploy the Ternary Logic Economic Suite

const hre = require("hardhat");

async function main() {
  console.log("--- Starting Ternary Logic Deployment ---");

  // 1. Deploy the Vault (Storage)
  const VaultFactory = await hre.ethers.getContractFactory("TL_Evidence_Vault");
  const vault = await VaultFactory.deploy();
  await vault.waitForDeployment();
  console.log(`[+] TL_Evidence_Vault deployed to: ${await vault.getAddress()}`);

  // 2. Deploy the Core (Logic), passing the Vault address
  const CoreFactory = await hre.ethers.getContractFactory("TL_Ledger_Core");
  const core = await CoreFactory.deploy(await vault.getAddress());
  await core.waitForDeployment();
  console.log(`[+] TL_Ledger_Core deployed to:   ${await core.getAddress()}`);

  // 3. Link them: Authorize Core to write to Vault
  const tx = await vault.setLedgerCore(await core.getAddress());
  await tx.wait();
  console.log("[+] Vault linked. Core authorized to write evidence.");

  console.log("--- Deployment Complete ---");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
