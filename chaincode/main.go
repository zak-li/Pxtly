package main

import (
	"log"
	"os"

	"github.com/hyperledger/fabric-chaincode-go/shim"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

func main() {
	cc, err := contractapi.NewChaincode(&AssetTraceContract{})
	if err != nil {
		log.Panicf("Erreur création chaincode: %v", err)
	}

	serverAddr := os.Getenv("CHAINCODE_SERVER_ADDRESS")
	ccID := os.Getenv("CHAINCODE_ID")

	if serverAddr != "" && ccID != "" {
		server := &shim.ChaincodeServer{
			CCID:    ccID,
			Address: serverAddr,
			CC:      cc,
			TLSProps: shim.TLSProperties{
				Disabled: true,
			},
		}
		log.Printf("Démarrage CCaaS sur %s avec ID %s", serverAddr, ccID)
		if err := server.Start(); err != nil {
			log.Panicf("Erreur démarrage serveur CCaaS: %v", err)
		}
		return
	}

	if err := cc.Start(); err != nil {
		log.Panicf("Erreur démarrage chaincode: %v", err)
	}
}
