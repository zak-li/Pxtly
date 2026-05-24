#!/usr/bin/env bash
SPASS="$1"

echo "==> Adding ufw rules for Docker bridge networks (172.16.0.0/12)..."
# Allow Docker containers to reach PostgreSQL and Redis
echo "$SPASS" | sudo -S ufw allow from 172.16.0.0/12 to any port 5432 comment "PostgreSQL from Docker"
echo "$SPASS" | sudo -S ufw allow from 172.16.0.0/12 to any port 6379 comment "Redis from Docker"
echo "$SPASS" | sudo -S ufw allow 8080/tcp comment "Keycloak HTTP"
echo "$SPASS" | sudo -S ufw allow 8443/tcp comment "Keycloak HTTPS"
echo "$SPASS" | sudo -S ufw reload
echo "==> ufw rules updated"
echo "$SPASS" | sudo -S ufw status | grep -E "8080|8443|5432|6379"
