# Changelog

All notable changes to Pxtly are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Changed
- **Rebrand**: the platform is renamed from `AIP Qx` to **Pxtly** across
  every user-facing surface (README, CHANGELOG, Dockerfile labels, LICENSE,
  CONTRIBUTING, chaincode docs, report PDF header, simulation banners).
  Internal infrastructure names — Keycloak realm `qx`, container names
  `qx-api` / `qx-celery-worker`, Prometheus job `qx-api`, JWT claim
  `qx_role`, Grafana dashboard title — are left untouched to avoid an
  invasive redeploy.
- **Logos**: new brand mark under `.github/assets/logos/` —
  `logo.svg` (default) and `logo-dark.svg` (for dark backgrounds),
  with matching PNG variants. README uses a `<picture>` element so
  GitHub renders the right one per OS theme.
- **Project layout** (earlier this cycle): `dlt-nodes/` → `fabric/`,
  `database/` → `db/`, `deployment/` → `stack/`.
- **JWT claim** (earlier this cycle): `pex_role` renamed to `qx_role`
  across the API, gRPC interceptors, Keycloak protocol mappers and
  user-attribute migration.

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
