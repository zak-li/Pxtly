// Command rwa-token is the Pxtly Hyperledger Fabric chaincode.
//
// AssetTraceContract is the entry type registered with the contract API.
// Its methods fall into three groups, each with its own MSP authorisation:
//
//   - Issuer (BANK01MSP):  TokenizeAsset, TransferAsset
//   - Regulator (REG01MSP): FreezeAsset, UnfreezeAsset
//   - Read-only (both):    GetAsset, GetAssetHistory, GetProvenanceTrail,
//                          QueryAssets
//
// State changes additionally require the 2-of-2 endorsement policy declared
// in fabric/config/configtx.yaml — the per-function ACL in access.go is an
// early gate that rejects forbidden calls *before* endorsement is solicited.
//
// The binary supports two execution modes, selected at start-up by env vars:
//
//   - Peer-launched: default. The peer spawns this binary inside a chaincode
//     container after a successful lifecycle install.
//   - Chaincode-as-a-Service (CCaaS): when CHAINCODE_ID and CHAINCODE_SERVER_ADDRESS
//     are set, the binary starts a gRPC server that the peer connects to. This
//     is the mode used by the Pxtly production deployment — see
//     fabric/scripts/deploy-chaincode.sh.
package main
