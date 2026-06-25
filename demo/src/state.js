export const state = {
    isOffline: false,
    emitterToken: sessionStorage.getItem("emitterToken") || null,
    regulatorToken: sessionStorage.getItem("regulatorToken") || null,
    activeAssetId: sessionStorage.getItem("activeAssetId") || null,
    activeIsin: sessionStorage.getItem("activeIsin") || null,
    lastFailedAction: null
};
