#!/bin/bash
set -e

export PATH=$PATH:~/fabric-project/bin
export FABRIC_CFG_PATH=~/rwa-platform/fabric/config
export ORDERER_CA=~/rwa-platform/crypto-config/ordererOrganizations/finance-trust.com/orderers/orderer.finance-trust.com/tls/ca.crt

function bnp() {
  export CORE_PEER_LOCALMSPID=BANK01MSP
  export CORE_PEER_MSPCONFIGPATH=~/rwa-platform/crypto-config/peerOrganizations/bank01.finance-trust.com/users/Admin@bank01.finance-trust.com/msp
  export CORE_PEER_TLS_ROOTCERT_FILE=~/rwa-platform/crypto-config/peerOrganizations/bank01.finance-trust.com/peers/peer0.bank01.finance-trust.com/tls/ca.crt
  export CORE_PEER_ADDRESS=peer0.bnpparibas.finance-trust.com:7051
}

function amf() {
  export CORE_PEER_LOCALMSPID=REG01MSP
  export CORE_PEER_MSPCONFIGPATH=~/rwa-platform/crypto-config/peerOrganizations/reg01-regulateur.finance-trust.com/users/Admin@reg01-regulateur.finance-trust.com/msp
  export CORE_PEER_TLS_ROOTCERT_FILE=~/rwa-platform/crypto-config/peerOrganizations/reg01-regulateur.finance-trust.com/peers/peer0.reg01-regulateur.finance-trust.com/tls/ca.crt
  export CORE_PEER_ADDRESS=peer0.amf-regulateur.finance-trust.com:7091
}

echo "=== Installing chaincode on BNP peer ==="
bnp
peer lifecycle chaincode install ~/rwa-platform/rwa-token-ccaas.tar.gz || true

echo "=== Installing chaincode on AMF peer ==="
amf
peer lifecycle chaincode install ~/rwa-platform/rwa-token-ccaas.tar.gz || true

sleep 5

bnp
export PKG_ID=$(peer lifecycle chaincode queryinstalled \
  | grep "rwa-token_1.0" | awk '{print $3}' | tr -d ',')
echo "PKG_ID = $PKG_ID"

echo "=== Approving chaincode for BNP ==="
bnp
peer lifecycle chaincode approveformyorg \
  -o orderer.finance-trust.com:7050 --tls --cafile $ORDERER_CA \
  --channelID rwa-channel --name rwa-token \
  --version 1.2 --package-id $PKG_ID --sequence 1

sleep 3

echo "=== Approving chaincode for AMF ==="
amf
peer lifecycle chaincode approveformyorg \
  -o orderer.finance-trust.com:7050 --tls --cafile $ORDERER_CA \
  --channelID rwa-channel --name rwa-token \
  --version 1.2 --package-id $PKG_ID --sequence 1

sleep 3

bnp
peer lifecycle chaincode checkcommitreadiness \
  --channelID rwa-channel --name rwa-token \
  --version 1.2 --sequence 1 --output json

echo "=== Committing chaincode ==="
peer lifecycle chaincode commit \
  -o orderer.finance-trust.com:7050 --tls --cafile $ORDERER_CA \
  --channelID rwa-channel --name rwa-token \
  --version 1.2 --sequence 1 \
  --peerAddresses peer0.bnpparibas.finance-trust.com:7051 \
  --tlsRootCertFiles ~/rwa-platform/crypto-config/peerOrganizations/bank01.finance-trust.com/peers/peer0.bank01.finance-trust.com/tls/ca.crt \
  --peerAddresses peer0.amf-regulateur.finance-trust.com:7091 \
  --tlsRootCertFiles ~/rwa-platform/crypto-config/peerOrganizations/reg01-regulateur.finance-trust.com/peers/peer0.reg01-regulateur.finance-trust.com/tls/ca.crt

echo "Chaincode rwa-token déployé sur rwa-channel."
