# Changelog

All notable changes to Pxtly are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] - 2026-05-31

### Added
- **CLI** is now a first-class part of the repository under `cli/`.
  Mirrors every REST endpoint via 12 Typer sub-apps, stores tokens
  in the OS keyring, runs OAuth 2.0 Authorization Code + PKCE
  natively, and writes a redacted local audit log to
  `~/.pxtly/audit.log`.
- **Brand assets** under `.github/assets/logos/` — `logo.svg`
  (default, dark fill for light backgrounds) and `logo-dark.svg`
  (light fill for dark backgrounds), with matching PNGs. README
  uses a `<picture>` element so GitHub renders the right variant
  per OS theme.

### Changed
- **Full brand purge**: every internal identifier carrying the
  legacy `qx` slug is renamed to `pxtly`. No `qx`, `regx`, `aip`,
  `aip-qx`, or `pex` remain anywhere in the source tree:
    - Keycloak realm     `qx` -> `pxtly`
    - Keycloak client    `qx-api` -> `pxtly-api`
    - JWT claim          `qx_role` -> `pxtly_role`
    - Celery app name    `qx-tasks` -> `pxtly-tasks`
    - Docker compose proj`qx` -> `pxtly` (+ network, containers)
    - Container names    `qx-api` -> `pxtly-api`,
                         `qx-celery-worker` -> `pxtly-celery-worker`,
                         `qx-keycloak` -> `pxtly-keycloak`
    - Prometheus job     `qx-api` -> `pxtly-api`, alerts group too
    - Grafana dashboard  uid `qx` -> `pxtly`, provider name same
    - Loki service tag   `qx-api` -> `pxtly-api`
    - Keycloak theme dir `themes/qx` -> `themes/pxtly`
- **License**: switched from BUSL 1.1 to Apache 2.0. No change-date
  condition, explicit patent grant, SPDX standard identifier.
- **Project layout**: top-level directories renamed for clarity —
  `dlt-nodes/` -> `fabric/`, `database/` -> `db/`,
  `deployment/` -> `stack/`.
- **Chaincode**: flattened to a single `chaincode/` package (one Go
  module, one binary) — previously nested under
  `chaincode/rwa-token/` with redundant `cmd/` and `internal/` layers.
- **Scripts**: consolidated under domain subfolders —
  `scripts/benchmarks/{fhe,zkp}.py` and
  `scripts/simulations/{dashboard,full,jitter,game_theory}.py`.
  `stack/scripts/install_latex.sh` moved to `scripts/install_latex.sh`.
- **Database seeds**: SQL file numbering collision resolved — the
  `db/sql/` chain is now 01 -> 08 with one file per prefix.

### Removed
- Orphan `.gitignore` / `.dockerignore` entries whose targets no
  longer existed (legacy `network/wallets`, `frontend/`, named dead
  scripts, etc.).
- Dead `SQLite audit_log` mechanism from `cli/cache.py` and the
  matching `_seed_from_cache` call in the dashboard.

### Migration notes
Renaming the Keycloak realm and client_id is a **breaking change**
for any deployed instance. To upgrade:

1. Stop the API + Celery containers.
2. Re-run `stack/keycloak/setup-realm.py` against the running
   Keycloak — it will create the new `pxtly` realm and `pxtly-api`
   client (the old `qx` realm and `qx-api` client can be deleted
   from the Admin Console once migration is verified).
3. Re-run `stack/keycloak/migrate-users.py` so the
   `pxtly_role` user attribute is set on each Keycloak user.
4. Update `.env` with `KEYCLOAK_REALM=pxtly`,
   `KEYCLOAK_CLIENT_ID=pxtly-api`, and the new client secret.
5. `docker compose down && docker compose up -d` to recreate
   containers under the new names.

All existing JWTs become invalid; users must log in again.

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

[2.0.0]: https://github.com/zak-li/pxtly/releases/tag/v2.0.0
[1.0.0]: https://github.com/zak-li/pxtly/releases/tag/v1.0.0
