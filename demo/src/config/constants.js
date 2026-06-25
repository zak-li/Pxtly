export const CONFIG = {
    API_URL: "http://10.10.10.150:8000",
    ENDPOINTS: {
        me: "/api/v1/auth/me",
        tokenize: "/api/v1/assets/tokenize",
        freeze: "/api/v1/assets/freeze",
        history: (assetId) => `/api/v1/assets/${assetId}/history`
    }
};

export const MOCKS = {
    EMITTER_PROFILE: {
        id: "5f529fd9-d1a5-4aa8-a4d8-a7be15758953",
        email: "zakaria.rahali@bank01.pxtly.demo",
        role: "EMETTEUR",
        msp_id: "BANK01MSP",
        first_name: "Zakaria",
        last_name: "Rahali"
    },
    REGULATOR_PROFILE: {
        id: "a826cd5c-0940-4d68-b2cb-8907986f7270",
        email: "aya.belkhaouad@reg01.pxtly.demo",
        role: "REGULATEUR",
        msp_id: "REG01MSP",
        first_name: "Aya",
        last_name: "Belkhaouad"
    },
    TOKENIZE_RESPONSE: {
        asset_id: "ASSET-12345-MOCK",
        isin: "FR0000123456",
        asset_type: "BOND",
        asset_name: "RWA Bond Demo Mock",
        issuer_org_id: "a1b2c3d4-0001-0001-0001-000000000001",
        current_owner_id: "a0000002-0002-0002-0002-000000000002",
        nominal_value: "15000000.0000",
        current_value: "15000000.0000",
        currency: "EUR",
        status: "ACTIF",
        issuance_date: new Date().toISOString().split('T')[0],
        fabric_tx_id: "mock_tx_id_tokenization_hash_value_1234567890abcdef",
        fabric_block_number: 142
    },
    FREEZE_REJECT_RESPONSE: {
        detail: "Insufficient privileges. Minimum role required: REGULATOR | SUPER_ADMIN"
    },
    FREEZE_ACCEPT_RESPONSE: {
        asset_id: "ASSET-12345-MOCK",
        isin: "FR0000123456",
        asset_type: "BOND",
        asset_name: "RWA Bond Demo Mock",
        issuer_org_id: "a1b2c3d4-0001-0001-0001-000000000001",
        current_owner_id: "a0000002-0002-0002-0002-000000000002",
        nominal_value: "15000000.0000",
        current_value: "15000000.0000",
        currency: "EUR",
        status: "FROZEN",
        issuance_date: new Date().toISOString().split('T')[0],
        fabric_tx_id: "mock_tx_id_freeze_hash_value_1234567890abcdef",
        fabric_block_number: 143
    },
    HISTORY_RESPONSE: [
        {
            tx_id: "mock_tx_id_tokenization_hash_value_1234567890abcdef",
            timestamp: new Date(Date.now() - 300000).toISOString(),
            actor_msp: "BANK01MSP",
            actor_dn: "CN=admin@bank01.finance-trust.com,OU=admin,L=Paris,ST=Ile-de-France,C=FR",
            action: "TOKENIZED",
            from_owner: "",
            to_owner: "CN=admin@bank01.finance-trust.com,OU=admin,L=Paris,ST=Ile-de-France,C=FR",
            amount: "15000000",
            justification: "Demonstration of RWA asset tokenization for the committee",
            block_number: 142
        },
        {
            tx_id: "mock_tx_id_freeze_hash_value_1234567890abcdef",
            timestamp: new Date().toISOString(),
            actor_msp: "REG01MSP",
            actor_dn: "CN=admin@reg01-regulateur.finance-trust.com,OU=admin,L=Paris,ST=Ile-de-France,C=FR",
            action: "FROZEN",
            from_owner: "",
            to_owner: "",
            amount: "0",
            justification: "Suspicion of non-compliance for audit",
            block_number: 143
        }
    ]
};
