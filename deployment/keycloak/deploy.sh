#!/usr/bin/env bash
# deploy.sh — Bootstrap Keycloak on the RWA platform server (10.10.10.150).
# Run once from a machine that can SSH to the server.
#
#   Usage:  bash deploy.sh

set -euo pipefail

REMOTE_USER="zakaria"
REMOTE_HOST="10.10.10.150"
REMOTE_DIR="/opt/rwa/keycloak"
COMPOSE_FILE="docker-compose.keycloak.yml"

echo "==> Copying deployment files to ${REMOTE_HOST}:${REMOTE_DIR}"
ssh "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p ${REMOTE_DIR}/tls"
scp "${COMPOSE_FILE}" ".env.keycloak"          "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"
scp tls/tls.crt tls/tls.key                    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/tls/"
scp setup-realm.py requirements-setup.txt       "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"

echo "==> Creating keycloak_db on the PostgreSQL server"
ssh "${REMOTE_USER}@${REMOTE_HOST}" bash << 'ENDSSH'
  set -euo pipefail
  source /opt/rwa/keycloak/.env.keycloak

  psql postgresql://rwaadmin:r0wTEPX08zRu5@10.10.10.150:5432/rwadb \
    -c "SELECT 1 FROM pg_database WHERE datname='keycloak_db'" | grep -q 1 \
  || psql postgresql://rwaadmin:r0wTEPX08zRu5@10.10.10.150:5432/rwadb \
       -c "CREATE DATABASE keycloak_db;"

  psql postgresql://rwaadmin:r0wTEPX08zRu5@10.10.10.150:5432/rwadb \
    -c "SELECT 1 FROM pg_roles WHERE rolname='${KEYCLOAK_DB_USER}'" | grep -q 1 \
  || psql postgresql://rwaadmin:r0wTEPX08zRu5@10.10.10.150:5432/rwadb \
       -c "CREATE USER ${KEYCLOAK_DB_USER} WITH PASSWORD '${KEYCLOAK_DB_PASSWORD}';
           GRANT ALL PRIVILEGES ON DATABASE keycloak_db TO ${KEYCLOAK_DB_USER};"
ENDSSH

echo "==> Starting Keycloak container"
ssh "${REMOTE_USER}@${REMOTE_HOST}" bash << 'ENDSSH'
  set -euo pipefail
  cd /opt/rwa/keycloak
  docker compose --env-file .env.keycloak -f docker-compose.keycloak.yml up -d --wait
  echo "Keycloak started. Waiting for health check..."
  for i in $(seq 1 20); do
    if curl -fso /dev/null http://localhost:8080/health/ready; then
      echo "Keycloak is healthy!"
      break
    fi
    echo "  ... attempt $i/20"
    sleep 5
  done
ENDSSH

echo "==> Configuring realm, client, and roles via Admin API"
ssh "${REMOTE_USER}@${REMOTE_HOST}" bash << 'ENDSSH'
  set -euo pipefail
  cd /opt/rwa/keycloak
  source .env.keycloak
  pip3 install -q -r requirements-setup.txt
  python3 setup-realm.py \
    --keycloak-url "http://localhost:8080" \
    --admin-user  "${KEYCLOAK_ADMIN_USER}" \
    --admin-pass  "${KEYCLOAK_ADMIN_PASSWORD}"
ENDSSH

echo ""
echo "==> Keycloak deployed and configured successfully!"
echo "    Admin UI: http://10.10.10.150:8080/admin"
echo "    HTTPS:    https://10.10.10.150:8443"
