<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../.github/assets/logos/logo-dark.svg">
    <img src="../.github/assets/logos/logo.svg" alt="Pxtly" width="300">
  </picture>
</p>

<br>

# Pxtly Command Line Interface (CLI)

Interactive terminal client for the Pxtly platform. Built with Typer and Rich, it provides institutional users and administrators with direct access to the asset tokenisation control plane, blockchain transactions, and compliance engines.

## Architecture

Modular Python CLI application designed for both interactive REPL usage and automated CI/CD environments.

* `main.py` : Typer application root and entry point.
* `commands/` : Sub-commands grouped by domain (`auth`, `assets`, `transactions`, `compliance`, etc.).
* `ui/` : Interactive REPL and terminal dashboard rendering using Rich.
* `api/` & `http/` : SDK bindings and HTTP clients to interact with the backend APIs.
* `security/` : Local keystore, cryptographic operations, and token management.
* `async_runner.py` : Event-loop management for asynchronous API calls.
* `network_state.py` : Real-time connection and backend status management.

## Usage

### Interactive Mode (REPL)

Run the CLI without arguments to launch the interactive, auto-completing prompt:
```bash
python -m cli.main
```

### Scripting Mode

Execute specific sub-commands directly from the shell for pipeline automation:
```bash
python -m cli.main auth login --org BANK01
python -m cli.main assets list
python -m cli.main audit view-transaction --tx-id TX-1234
```

## Core Sub-Systems

- **Assets & Transactions**: Tokenisation workflows and transfers.
- **Agent**: Direct integration with the AI decision engine for data queries.
- **Audit**: Cryptographic block verification and ledger timeline inspection.
- **ZKP (Zero-Knowledge Proofs)**: Manage and verify ZK-KYC credentials.
- **Tribunal**: Supervisory and regulatory freezing actions.
