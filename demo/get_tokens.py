#!/usr/bin/env python3
"""
get_tokens.py
-------------
Helper script to retrieve JWT access tokens for:
  - Emitter (zakaria.rahali@bank01.pxtly.demo)
  - Regulator (aya.belkhaouad@reg01.pxtly.demo)
from Keycloak and write them to `config.local.js` for the demo frontend.
"""
import os
import sys
import json
import httpx
from dotenv import load_dotenv

# Load env variables from workspace .env (parent directory)
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_project_root, ".env"))

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL", "https://10.10.10.150:8443")
REALM = os.environ.get("DEMO_KEYCLOAK_REALM", "pxtly")
CLIENT_ID = os.environ.get("DEMO_KEYCLOAK_CLIENT_ID", "pxtly-api")
CLIENT_SECRET = os.environ.get("DEMO_KEYCLOAK_CLIENT_SECRET")

# If DEMO_KEYCLOAK_CLIENT_SECRET is missing, check standard env
if not CLIENT_SECRET:
    CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")

if not CLIENT_SECRET:
    sys.exit("Error: KEYCLOAK_CLIENT_SECRET / DEMO_KEYCLOAK_CLIENT_SECRET missing in .env")

# Simulated user accounts credentials
USERS = {
    "EMITTER": {
        "username": "zakaria.rahali@bank01.pxtly.demo",
        "password": "Zakaria_5110_Secure!"
    },
    "REGULATOR": {
        "username": "aya.belkhaouad@reg01.pxtly.demo",
        "password": "Aya_4812_Secure!"
    }
}

TOKEN_URL = f"{KEYCLOAK_URL.rstrip('/')}/realms/{REALM}/protocol/openid-connect/token"

# Insecure TLS checks (self-signed certs)
verify_tls = False

print(f"Connecting to Keycloak: {TOKEN_URL}")
tokens = {}

for role, creds in USERS.items():
    print(f"Requesting token for {role} ({creds['username']})...")
    data = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": creds["username"],
        "password": creds["password"],
        "scope": "openid email profile"
    }
    try:
        r = httpx.post(TOKEN_URL, data=data, verify=verify_tls, timeout=10)
        r.raise_for_status()
        tokens[role] = r.json()["access_token"]
        print(f"-> Token successfully retrieved for {role}!")
    except Exception as e:
        print(f"Error fetching token for {role}: {e}")
        if 'r' in locals() and r.text:
            print(f"Response: {r.text}")
        sys.exit(1)

# Write to config.local.js
config_content = f"""// Configuration locale auto-générée pour la démonstration.
// Ce fichier contient les tokens JWT valides récupérés de Keycloak.
// Ne pas commiter ce fichier !
window.CONFIG_LOCAL = {{
  EMITTER_TOKEN: "{tokens['EMITTER']}",
  REGULATOR_TOKEN: "{tokens['REGULATOR']}"
}};
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
local_config_path = os.path.join(script_dir, "config.local.js")
with open(local_config_path, "w", encoding="utf-8") as f:
    f.write(config_content)

print(f"\nSuccess! JWT tokens saved to '{local_config_path}'.")
print("You can now open the demo frontend in your browser.")
