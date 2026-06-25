<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../.github/assets/logos/logo-dark.svg">
    <img src="../.github/assets/logos/logo.svg" alt="Pxtly" width="300">
  </picture>
</p>

<br>

# Pxtly Interactive Demo Guide

Deploy and run the interactive demonstration environment.

## Quick Start

1. **Activate the Python virtual environment**:
   ```powershell
   .venv\Scripts\activate
   ```

2. **Generate Keycloak tokens**:
   Run the helper script to authenticate and save valid JWTs locally:
   ```bash
   python get_tokens.py
   ```

3. **Start the Vite Development Server**:
   ```bash
   npm install
   npm run dev
   ```
   The browser will open automatically at **`http://localhost:5500/`**.

## Network Configuration

Ensure `ALLOWED_ORIGINS` in your `.env` file includes `http://localhost:5500` to permit CORS requests from the frontend to the FastAPI backend.

## Offline Simulator

If network connectivity drops during a presentation, click the **Offline Simulator** plug icon in the top right corner. In case of API failure, a prompt will allow you to instantly switch to offline mode using mocked ledger data to preserve the presentation flow.

## Scenario Outline

1. **Issuer Login**: Authenticates the issuer organization via an independent OIDC identity provider.
2. **Tokenize Asset**: Smart contract validates formatting and registers the asset on the Fabric ledger.
3. **Regulator Login**: Authenticates the regulator with distinct supervisory privileges.
4. **Freeze (By Issuer)**: Fabric Chaincode enforces access control by rejecting the issuer's freeze attempt (403 Forbidden).
5. **Freeze (By Regulator)**: The regulator successfully freezes the asset, immutably modifying the ledger state.
6. **View History**: Displays cryptographic blocks as an unalterable visual timeline.
