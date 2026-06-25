import { state } from '../state.js';
import { CONFIG, MOCKS } from '../config/constants.js';
import { getOrgName } from '../utils/helpers.js';
import { logRequest, logResponse, setActiveStep, showLoading, hideLoading, showErrorOverlay, renderTimeline } from '../ui/layout.js';

export async function runEmitterAuth() {
    const handleSuccess = (profile) => {
        const el = document.getElementById("emitter-status");
        el.querySelector(".auth-status-label").textContent = "Connected";
        const val = el.querySelector(".auth-status-val");
        const suffix = getOrgName(profile);
        val.textContent = `${profile.email} · ${suffix}`;
        val.classList.add("connected");
        el.style.borderLeftColor = "var(--success)";
        logResponse(200, profile);
        setActiveStep(2);
    };

    logRequest("GET", CONFIG.ENDPOINTS.me, { "Authorization": "Bearer <EMITTER_TOKEN>" }, null);

    if (state.isOffline) {
        setTimeout(() => handleSuccess(MOCKS.EMITTER_PROFILE), 500);
        return;
    }

    if (!state.emitterToken) {
        const redirectUri = encodeURIComponent(window.location.origin + window.location.pathname);
        const loginHint = encodeURIComponent("zakaria.rahali@bank01.pxtly.demo");
        const kcUrl = `https://10.10.10.150:8443/realms/pxtly/protocol/openid-connect/auth?client_id=pxtly-api&response_type=token&redirect_uri=${redirectUri}&state=emitter&scope=openid&prompt=login&login_hint=${loginHint}`;
        window.location.href = kcUrl;
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${CONFIG.ENDPOINTS.me}`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${state.emitterToken}` }
        });
        if (!res.ok) throw new Error(`Connection error (Code ${res.status})`);
        const data = await res.json();
        handleSuccess(data);
    } catch (err) {
        showErrorOverlay(`Failed to authenticate Issuer via API: ${err.message}`, runEmitterAuth);
    } finally {
        hideLoading();
    }
}

export async function runTokenize() {
    const isin = document.getElementById("input-isin").value;
    const nominalVal = document.getElementById("input-nominal").value;
    const dateToday = new Date().toISOString().split('T')[0];
    const randomSuffix = String(Math.floor(100 + Math.random() * 900));
    const assetId = `RWA-OBLIGATION-DEMO-2026-${randomSuffix}`;

    const payload = {
        asset_id: assetId,
        isin: isin,
        asset_type: "BOND",
        asset_name: `RWA Bond Demo ${Math.floor(100 + Math.random() * 900)}`,
        issuer_lei: "R0MUWSFPU8MPRO8K5P83",
        nominal_value: parseFloat(nominalVal),
        currency: "EUR",
        issuance_date: dateToday,
        justification: "Demonstration of RWA asset tokenization for the committee"
    };

    const handleSuccess = (resData) => {
        state.activeAssetId = resData.asset_id;
        state.activeIsin = resData.isin;
        sessionStorage.setItem("activeAssetId", state.activeAssetId);
        sessionStorage.setItem("activeIsin", state.activeIsin);
        logResponse(201, resData);
        setActiveStep(3);
    };

    logRequest("POST", CONFIG.ENDPOINTS.tokenize, { "Authorization": "Bearer <EMITTER_TOKEN>" }, payload);

    if (state.isOffline) {
        MOCKS.TOKENIZE_RESPONSE.asset_id = assetId;
        MOCKS.TOKENIZE_RESPONSE.isin = isin;
        MOCKS.TOKENIZE_RESPONSE.issuance_date = dateToday;
        setTimeout(() => handleSuccess(MOCKS.TOKENIZE_RESPONSE), 800);
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${CONFIG.ENDPOINTS.tokenize}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${state.emitterToken}`, "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const errBody = await res.json().catch(() => ({ detail: res.statusText }));
            logResponse(res.status, errBody);
            let detailMsg = errBody.detail;
            if (typeof detailMsg !== 'string') detailMsg = JSON.stringify(detailMsg);
            throw new Error(`Smart contract rejected the write: ${detailMsg || res.statusText}`);
        }
        const data = await res.json();
        handleSuccess(data);
    } catch (err) {
        showErrorOverlay(`Tokenization transaction failed: ${err.message}`, runTokenize);
    } finally {
        hideLoading();
    }
}

export async function runRegulatorAuth() {
    const handleSuccess = (profile) => {
        const el = document.getElementById("regulator-status");
        el.querySelector(".auth-status-label").textContent = "Connected";
        const val = el.querySelector(".auth-status-val");
        const suffix = getOrgName(profile);
        val.textContent = `${profile.email} · ${suffix}`;
        val.classList.add("connected");
        el.style.borderLeftColor = "var(--success)";
        logResponse(200, profile);
        setActiveStep(4);
    };

    logRequest("GET", CONFIG.ENDPOINTS.me, { "Authorization": "Bearer <REGULATOR_TOKEN>" }, null);

    if (state.isOffline) {
        setTimeout(() => handleSuccess(MOCKS.REGULATOR_PROFILE), 500);
        return;
    }

    if (!state.regulatorToken) {
        const redirectUri = encodeURIComponent(window.location.origin + window.location.pathname);
        const loginHint = encodeURIComponent("aya.belkhaouad@reg01.pxtly.demo");
        const kcUrl = `https://10.10.10.150:8443/realms/pxtly/protocol/openid-connect/auth?client_id=pxtly-api&response_type=token&redirect_uri=${redirectUri}&state=regulator&scope=openid&prompt=login&login_hint=${loginHint}`;
        window.location.href = kcUrl;
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${CONFIG.ENDPOINTS.me}`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${state.regulatorToken}` }
        });
        if (!res.ok) throw new Error(`Connection error (Code ${res.status})`);
        const data = await res.json();
        handleSuccess(data);
    } catch (err) {
        showErrorOverlay(`Failed to authenticate Regulator via API: ${err.message}`, runRegulatorAuth);
    } finally {
        hideLoading();
    }
}

export async function runFreezeByEmitter() {
    const payload = {
        asset_id: state.activeAssetId || "ASSET-MOCK-ID",
        reason: "Suspicion of non-compliance for audit",
        regulatory_ref: "REG-FR-2026-001"
    };

    logRequest("POST", CONFIG.ENDPOINTS.freeze, { "Authorization": "Bearer <EMITTER_TOKEN>" }, payload);

    if (state.isOffline) {
        setTimeout(() => {
            logResponse(403, MOCKS.FREEZE_REJECT_RESPONSE);
            document.getElementById("btn-freeze-regulator").removeAttribute("disabled");
        }, 600);
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${CONFIG.ENDPOINTS.freeze}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${state.emitterToken}`, "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const errBody = await res.json().catch(() => ({ detail: res.statusText }));
        logResponse(res.status, errBody);

        if (res.status === 403) {
            document.getElementById("btn-freeze-regulator").removeAttribute("disabled");
        } else if (res.ok) {
            alert("️ Fail: The issuer successfully froze the asset when it should have been blocked!");
        } else {
            throw new Error(`Unexpected server error: Code ${res.status}`);
        }
    } catch (err) {
        showErrorOverlay(`Unexpected error submitting Freeze by Issuer: ${err.message}`, runFreezeByEmitter);
    } finally {
        hideLoading();
    }
}

export async function runFreezeByRegulator() {
    const payload = {
        asset_id: state.activeAssetId || "ASSET-MOCK-ID",
        reason: "Suspicion of non-compliance for audit",
        regulatory_ref: "REG-FR-2026-001"
    };

    const handleSuccess = (resData) => {
        logResponse(200, resData);
        setActiveStep(6);
    };

    logRequest("POST", CONFIG.ENDPOINTS.freeze, { "Authorization": "Bearer <REGULATOR_TOKEN>" }, payload);

    if (state.isOffline) {
        MOCKS.FREEZE_ACCEPT_RESPONSE.asset_id = state.activeAssetId || "ASSET-MOCK-ID";
        MOCKS.FREEZE_ACCEPT_RESPONSE.isin = state.activeIsin || "FR0000123456";
        MOCKS.FREEZE_ACCEPT_RESPONSE.issuance_date = new Date().toISOString().split('T')[0];
        setTimeout(() => handleSuccess(MOCKS.FREEZE_ACCEPT_RESPONSE), 800);
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${CONFIG.ENDPOINTS.freeze}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${state.regulatorToken}`, "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const errBody = await res.json().catch(() => ({ detail: res.statusText }));
            logResponse(res.status, errBody);
            throw new Error(`Regulatory smart contract rejected the write: ${errBody.detail || res.statusText}`);
        }
        const data = await res.json();
        handleSuccess(data);
    } catch (err) {
        showErrorOverlay(`Regulatory Freeze transaction failed: ${err.message}`, runFreezeByRegulator);
    } finally {
        hideLoading();
    }
}

export async function runHistory() {
    const assetId = state.activeAssetId || "ASSET-MOCK-ID";
    const endpoint = CONFIG.ENDPOINTS.history(assetId);

    const handleSuccess = (resData) => {
        logResponse(200, resData);
        renderTimeline(resData);
    };

    logRequest("GET", endpoint, { "Authorization": "Bearer <EMITTER_TOKEN>" }, null);

    if (state.isOffline) {
        MOCKS.HISTORY_RESPONSE[0].tx_id = MOCKS.TOKENIZE_RESPONSE.fabric_tx_id;
        MOCKS.HISTORY_RESPONSE[1].tx_id = MOCKS.FREEZE_ACCEPT_RESPONSE.fabric_tx_id;
        setTimeout(() => handleSuccess(MOCKS.HISTORY_RESPONSE), 500);
        return;
    }

    try {
        showLoading();
        const res = await fetch(`${CONFIG.API_URL}${endpoint}`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${state.emitterToken}` }
        });
        if (!res.ok) {
            const errBody = await res.json().catch(() => ({ detail: res.statusText }));
            logResponse(res.status, errBody);
            throw new Error(`Error extracting history: ${errBody.detail || res.statusText}`);
        }
        const data = await res.json();
        if (Array.isArray(data)) {
            data.forEach(tx => {
                const fixDn = (dn) => {
                    if (!dn) return dn;
                    return String(dn).replace("C=US", "C=FR").replace("ST=California", "ST=Ile-de-France").replace("L=San Francisco", "L=Paris").replace("CN=Admin", "CN=admin");
                };
                tx.actor_dn = fixDn(tx.actor_dn);
                if (tx.to_owner) tx.to_owner = fixDn(tx.to_owner);
                if (tx.from_owner) tx.from_owner = fixDn(tx.from_owner);
            });
        }
        handleSuccess(data);
    } catch (err) {
        showErrorOverlay(`Traceability request failed: ${err.message}`, runHistory);
    } finally {
        hideLoading();
    }
}
