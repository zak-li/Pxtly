#!/usr/bin/env bash
echo "=== Testing TCP connectivity to 10.10.10.150:5432 from Keycloak container ==="
docker exec rwa-keycloak bash -c "timeout 5 bash -c 'cat /dev/null > /dev/tcp/10.10.10.150/5432' && echo 'TCP OK' || echo 'TCP FAILED'"

echo "=== Testing JDBC from container (psql via apt if available) ==="
docker exec rwa-keycloak bash -c "which psql 2>/dev/null && psql postgresql://keycloak_user:KcDb@2026\!SecurePass@10.10.10.150:5432/keycloak_db -c 'SELECT 1' 2>&1 || echo 'psql not in container'"

echo "=== ufw status ==="
echo "$1" | sudo -S ufw status 2>/dev/null || echo "ufw not active"
