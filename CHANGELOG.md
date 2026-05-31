# Changelog

All notable changes to Pxtly are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- **Brand assets** under `.github/assets/logos/` — `logo.svg`
  (default, dark fill for light backgrounds) and `logo-dark.svg`
  (light fill for dark backgrounds), with matching PNGs. The README
  uses a `<picture>` element so GitHub renders the right variant
  per OS theme.

### Changed
- **Project layout**: top-level directories renamed for clarity —
  `dlt-nodes/` → `fabric/`, `database/` → `db/`, `deployment/` → `stack/`.
- **Chaincode**: flattened to a single `chaincode/` package (one Go
  module, one binary) — previously nested under `chaincode/rwa-token/`
  with redundant `cmd/` and `internal/` layers.
- **Scripts**: consolidated under domain subfolders —
  `scripts/benchmarks/{fhe,zkp}.py` and
  `scripts/simulations/{dashboard,full,jitter,game_theory}.py`.
  `stack/scripts/install_latex.sh` moved to `scripts/install_latex.sh`.
- **Database seeds**: SQL file numbering collision resolved — the
  `db/sql/` chain is now 01 → 08 with one file per prefix.
- **JWT claim**: renamed to `qx_role` across the API, gRPC
  interceptors, Keycloak protocol mappers and user-attribute migration.

### Removed
- Orphan `.gitignore` / `.dockerignore` entries whose targets no
  longer existed (legacy `network/wallets`, `frontend/`, named dead
  scripts, etc.).
- Dead `SQLite audit_log` mechanism from `cli/cache.py` and the
  matching `_seed_from_cache` call in the dashboard.

---

## [1.0.0] - 2026-05-10

### Added
- **Core Engine**: Initial release of the tokenisation platform
  (FastAPI + gRPC + Celery).
- **DLT Network**: Hyperledger Fabric 2.5 permissioned network with a
  Go chaincode deployed as Chaincode-as-a-Service.
- **Compliance Suite**: MiCA validation, AML sanctions screening,
  FHE-based fraud scoring, and zk-KYC workflows.
- **AI Agent**: Regulatory RAG agent powered by ChromaDB and Groq.
- **Security & Ops**: HashiCorp Vault integration, Neo4j graph scanning,
  and a complete Prometheus / Grafana monitoring stack.

[Unreleased]: https://github.com/zak-li/pxtly/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/zak-li/pxtly/releases/tag/v1.0.0
