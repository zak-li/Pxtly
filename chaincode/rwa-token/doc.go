// Package main is the rwa-token chaincode for AIP Qx.
//
// It runs on the rwa-channel Hyperledger Fabric channel and implements
// the on-chain side of the tokenisation workflow:
//
//   - TokenizeAsset / TransferAsset       — issuer-side state changes (BANK01MSP)
//   - FreezeAsset / UnfreezeAsset         — regulator-side state changes (REG01MSP)
//   - GetAsset / GetAssetHistory /        — read-only views (both MSPs)
//     GetProvenanceTrail / QueryAssets
//
// State changes require the 2-of-2 endorsement policy
// AND('BANK01MSP.peer','REG01MSP.peer') declared in fabric/config/configtx.yaml.
//
// The binary supports two execution modes:
//
//   - Peer-launched: the peer spawns the chaincode container after a successful
//     lifecycle install.
//   - Chaincode-as-a-Service (CCaaS): when CHAINCODE_ID and CHAINCODE_SERVER_ADDRESS
//     are set, the binary starts a gRPC server that the peer connects to. This
//     is the mode used in the AIP Qx production deployment — see
//     fabric/scripts/deploy-chaincode.sh.
package main
