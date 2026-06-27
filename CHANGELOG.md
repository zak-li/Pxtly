# Changelog

All notable changes to Pxtly are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.1] - 2026-06-27

### Added
- **Docker publish workflow**: Automated Docker image build and push
  to GitHub Container Registry (`ghcr.io/zak-li/x-engine`) on
  every push to `master` and on version tags.
- **Interactive frontend demo**: Full interactive demonstration UI under
  `demo/` with Vite, an offline simulator mode (with a dynamic plug icon
  and animated tooltip), and a standalone token helper (`get_tokens.py`).
- **CLI documentation**: Comprehensive CLI usage guide and REPL
  architecture overview added under `cli/README.md`.
- **Mock data generator**: `db/generate_mock_data.py` for clean,
  reproducible test fixtures.

### Changed
- **License**: Switched from Apache 2.0 to AGPLv3 for strict
  copyleft protection.
- **CLI**: Enhanced TUI with improved ASCII chart rendering, updated
  auth flow (PKCE token storage), and console output.
- **Core**: Updated Fabric client network/wallet modules, added new
  asset routing endpoints, and refined schemas.
- **Database**: Updated schema definitions, seed data, and migration
  config. Sanitized fixtures by removing stale CSV/JSON mock files.
- **Fabric**: Updated deployment scripts, connection profiles, and
  Docker Compose configuration.
- **README**: Streamlined badges to essential indicators (version,
  license, CI, issues, last commit, docker, ruff, pytest). Added
  Pxtly etymology section.

### Fixed
- **Linting**: Resolved project-wide Ruff formatting and Bandit
  security issues across `core/`, `scripts/`, `tests/`, and `stack/`.
- **Docker build**: Fixed `.dockerignore` to include `fabric/config/`
  in the build context for runtime connection profiles.
- **Tests**: Updated `conftest.py` and end-to-end compliance flow
  tests for compatibility with the updated schemas.

### Removed
- Stale fixture files (`compliance_kyc_aml.json`,
  `fabric_wallets.json`, `fabric_world_state.json`, and CSV history
  files) replaced by the mock data generator.
- Outdated architecture SVG diagrams and compliance flow diagram.

---

## [2.0.0] - 2026-05-31

### Added
- **CLI** is now a first-class part of the repository under `cli/`.
  Mirrors every REST endpoint via 12 Typer sub-apps, stores tokens
  in the OS keyring, runs OAuth 2.0 Authorization Code + PKCE
  natively, and writes a redacted local audit log to
  `~/.pxtly/audit.log`.
- **Brand assets** under `.github/assets/logos/` with `logo.svg`
  (default, dark fill for light backgrounds) and `logo-dark.svg`
  (light fill for dark backgrounds), with matching PNGs. README
  uses a `<picture>` element so GitHub renders the right variant
  per OS theme.

### Changed
- **Brand purge**: every internal slug, container name, network,
  Keycloak realm, JWT claim, Celery app, Prometheus job, Grafana
  uid, Loki service tag, theme directory, and configuration default
  is now anchored on the `pxtly` namespace. No legacy brand
  identifiers remain anywhere in the source tree.
- **License**: switched to Apache 2.0. No change-date condition,
  explicit patent grant, SPDX standard identifier.
- **Project layout**: top-level directories renamed for clarity to
  `fabric/`, `db/`, and `stack/`.
- **Chaincode**: flattened to a single `chaincode/` package (one Go
  module, one binary).
- **Scripts**: consolidated under domain subfolders
  `scripts/benchmarks/{fhe,zkp}.py` and
  `scripts/simulations/{dashboard,full,jitter,game_theory}.py`.
  `install_latex.sh` moved to `scripts/install_latex.sh`.
- **Database seeds**: SQL file numbering collision resolved; the
  `db/sql/` chain is now 01 to 08 with one file per prefix.

### Removed
- Orphan `.gitignore` / `.dockerignore` entries whose targets no
  longer existed (legacy `network/wallets`, `frontend/`, named dead
  scripts).
- Dead SQLite audit log mechanism from `cli/cache.py` and the
  matching `_seed_from_cache` call in the dashboard.

### Migration notes
This is a **breaking** release for any deployed instance because
the Keycloak realm name, client identifier, and JWT audience all
change. To upgrade an existing deployment:

1. Stop the API and Celery containers.
2. Re-run `stack/keycloak/setup-realm.py` against the running
   Keycloak. It creates the new realm and client; the previous
   realm and client can be deleted from the Admin Console once the
   migration is verified end-to-end.
3. Re-run `stack/keycloak/migrate-users.py` so the new role
   attribute is set on each Keycloak user.
4. Update `.env`: set `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID`, and
   `KEYCLOAK_CLIENT_SECRET` to the values from step 2.
5. `docker compose down && docker compose up -d` to recreate
   containers under their new names.

All existing access tokens become invalid because the audience
changes; every user must log in again.

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
- **Security and Ops**: HashiCorp Vault integration, Neo4j graph
  scanning, and a complete Prometheus / Grafana monitoring stack.

[2.0.1]: https://github.com/zak-li/pxtly/releases/tag/v2.0.1
[2.0.0]: https://github.com/zak-li/pxtly/releases/tag/v2.0.0
[1.0.0]: https://github.com/zak-li/pxtly/releases/tag/v1.0.0
