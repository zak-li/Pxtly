<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../.github/assets/logos/logo-dark.svg">
    <img src="../.github/assets/logos/logo.svg" alt="Pxtly" width="300">
  </picture>
</p>

<br>

# Pxtly Chaincode (`rwa-token`)

Go smart contract running on the Pxtly Hyperledger Fabric channel (`rwa-channel`). It implements the on-chain tokenization workflow with a strict **2-of-2 endorsement quorum** between the Issuer (`BANK01MSP`) and the Regulator (`REG01MSP`).

## Architecture

Single-package Fabric chaincode deployed as a service (CCaaS).

* `doc.go` : Package documentation.
* `main.go` : Application entry point for CCaaS mode.
* `contract.go` : Core logic for tokenization, transfers, and status freezing.
* `access.go` : Strict Access Control List (ACL) mapping for MSP roles.
* `compliance.go` : Automated validation for ISIN, LEI, and MiCA formatting.
* `models.go` : On-chain data structures.
* `contract_test.go` : Comprehensive test suite.

## Usage

Run tests and compile locally:
```bash
go vet ./...
go test ./...
go build -o rwa-token .
```

## Chaincode as a Service (CCaaS)

To run the binary as a gRPC server for the Fabric peer:
```bash
export CHAINCODE_ID="<package-id>"
export CHAINCODE_SERVER_ADDRESS="0.0.0.0:9999"
./rwa-token
```

Or deploy using Docker:
```bash
docker build -f Dockerfile.ccaas -t rwa-token:ccaas .
```

## Endorsement Policy

All state transitions strictly require signatures from both key organizations:
```text
AND('BANK01MSP.peer','REG01MSP.peer')
```
Access control logic prevents unauthorized calls before they reach the endorsement phase, optimizing execution times.
