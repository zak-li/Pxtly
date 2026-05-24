#!/usr/bin/env bash
set -euo pipefail
SPASS="$1"  # sudo password passed as arg

echo "==> Setting up keycloak_db..."

DB_EXISTS=$(echo "$SPASS" | sudo -S -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='keycloak_db'" 2>/dev/null)
if [ "$DB_EXISTS" != "1" ]; then
  echo "$SPASS" | sudo -S -u postgres psql -c "CREATE DATABASE keycloak_db"
  echo "  keycloak_db created"
else
  echo "  keycloak_db already exists"
fi

USER_EXISTS=$(echo "$SPASS" | sudo -S -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='keycloak_user'" 2>/dev/null)
if [ "$USER_EXISTS" != "1" ]; then
  echo "$SPASS" | sudo -S -u postgres psql -c "CREATE USER keycloak_user WITH PASSWORD 'KcDb@2026!SecurePass'"
  echo "  keycloak_user created"
else
  echo "  keycloak_user already exists"
  echo "$SPASS" | sudo -S -u postgres psql -c "ALTER USER keycloak_user WITH PASSWORD 'KcDb@2026!SecurePass'"
fi

echo "$SPASS" | sudo -S -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE keycloak_db TO keycloak_user"
echo "$SPASS" | sudo -S -u postgres psql -d keycloak_db -c "GRANT ALL ON SCHEMA public TO keycloak_user"
echo "  Grants done"
echo "==> DB setup complete"
