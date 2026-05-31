# `rwa-token` chaincode

Go smart contract that runs on the Pxtly Hyperledger Fabric channel
(`rwa-channel`). Implements the on-chain side of the tokenisation
workflow with the **2-of-2 endorsement quorum** between `BANK01MSP`
(issuer) and `REG01MSP` (regulator).

## Layout

Single-package Fabric chaincode (one module, one binary) — files split
by concern:

| File                | Role                                                              |
|---------------------|-------------------------------------------------------------------|
| `doc.go`            | Package documentation (godoc reads it as the package summary).    |
| `main.go`           | Entry point. Selects peer-launched vs CCaaS mode at start-up.     |
| `contract.go`       | `AssetTraceContract` — Tokenize/Transfer/Freeze/Unfreeze + reads. |
| `access.go`         | MSP/DN extraction (`verifyRole`) and per-function ACL map.        |
| `compliance.go`     | Format validators (AssetID, ISIN, LEI, currency) + MiCA Art. 68.  |
| `models.go`         | On-chain types (`FinancialAsset`, `ProvenanceRecord`, statuses).  |
| `contract_test.go`  | Unit tests (`go test ./...`).                                     |
| `Dockerfile.ccaas`  | Image for Chaincode-as-a-Service mode.                            |
| `go.mod` / `go.sum` | Go module: `github.com/zak-li/pxtly/chaincode`.                  |
| `.gitignore`        | Excludes Go build artefacts (`*.exe`, `*.test`, vendored deps).   |

## Build & test

Run from this directory:

```bash
go vet ./...
go test ./...
go build -o rwa-token .
```

CI runs the same three commands — see [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) (`go-build` job).

## Run as CCaaS

The binary acts as a gRPC server when the two env vars below are set;
the peer connects to it instead of spawning a chaincode container.

```bash
export CHAINCODE_ID="<package-id-from-peer-lifecycle>"
export CHAINCODE_SERVER_ADDRESS="0.0.0.0:9999"
./rwa-token
```

Build the image with:

```bash
docker build -f Dockerfile.ccaas -t rwa-token:ccaas .
```

## Endorsement policy

State changes require **2-of-2** endorsement:

```
AND('BANK01MSP.peer','REG01MSP.peer')
```

Declared in [`fabric/config/configtx.yaml`](../fabric/config/configtx.yaml) and enforced by the peer at
commit time. The function-level ACL in `access.go` is an extra gate
on the proposal side — it rejects calls from a non-authorised MSP
*before* the proposal is endorsed, saving a round-trip.
