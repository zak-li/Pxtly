import { state } from './state.js';
import { updateStatusIndicator, setActiveStep, hideErrorOverlay } from './ui/layout.js';
import { runEmitterAuth, runTokenize, runRegulatorAuth, runFreezeByEmitter, runFreezeByRegulator, runHistory } from './api/services.js';

function forceOfflineBascule() {
    state.isOffline = true;
    hideErrorOverlay();
    updateStatusIndicator();
    if (state.lastFailedAction) {
        state.lastFailedAction();
    }
}

function retryLastAction() {
    hideErrorOverlay();
    if (state.lastFailedAction) {
        state.lastFailedAction();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    state.emitterToken = sessionStorage.getItem("emitterToken") || null;
    state.regulatorToken = sessionStorage.getItem("regulatorToken") || null;

    document.getElementById("btn-login-emitter").addEventListener("click", runEmitterAuth);
    document.getElementById("btn-tokenize").addEventListener("click", runTokenize);
    document.getElementById("btn-login-regulator").addEventListener("click", runRegulatorAuth);
    document.getElementById("btn-freeze-emitter").addEventListener("click", runFreezeByEmitter);
    document.getElementById("btn-freeze-regulator").addEventListener("click", runFreezeByRegulator);
    document.getElementById("btn-history").addEventListener("click", runHistory);

    document.getElementById("btn-error-retry").addEventListener("click", retryLastAction);
    document.getElementById("btn-error-offline").addEventListener("click", forceOfflineBascule);

    const btnOffline = document.getElementById("btn-offline-force");
    btnOffline.addEventListener("click", () => {
        state.isOffline = !state.isOffline;
        updateStatusIndicator();
    });

    updateStatusIndicator();
    setActiveStep(1);

    const randomIsin = "FR" + Math.floor(1000000000 + Math.random() * 9000000000);
    document.getElementById("input-isin").value = randomIsin;

    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const token = hashParams.get('access_token');
    const urlState = hashParams.get('state');

    if (!token) {
        sessionStorage.clear();
        state.emitterToken = null;
        state.regulatorToken = null;
        state.activeAssetId = null;
        state.activeIsin = null;
    } else {
        window.history.replaceState({}, document.title, window.location.pathname);
        if (urlState === 'emitter') {
            state.emitterToken = token;
            sessionStorage.setItem("emitterToken", token);
            runEmitterAuth();
        } else if (urlState === 'regulator') {
            state.regulatorToken = token;
            sessionStorage.setItem("regulatorToken", token);
            runRegulatorAuth();
        }
    }

    if (state.emitterToken && urlState !== 'emitter') runEmitterAuth();
    if (state.regulatorToken && urlState !== 'regulator') runRegulatorAuth();
});
