import { state } from '../state.js';
import { CONFIG } from '../config/constants.js';
import { syntaxHighlight, escapeHtml } from '../utils/helpers.js';

export function updateStatusIndicator() {
    const text = document.getElementById("connection-status-text");
    const plugSvg = document.getElementById("btn-offline-force");
    const tooltipText = document.getElementById("offline-tooltip");
    
    if (state.isOffline) {
        text.className = "status-text status-offline";
        text.textContent = "Offline Mode";
        if (plugSvg) plugSvg.style.color = "var(--warning)";
        if (tooltipText) {
            tooltipText.textContent = "Go online";
            tooltipText.style.setProperty("--tooltip-bg", "var(--warning)");
            tooltipText.style.setProperty("--tooltip-color", "#000");
        }
    } else {
        text.className = "status-text status-online";
        text.textContent = "Online Mode";
        if (plugSvg) plugSvg.style.color = "var(--success)";
        if (tooltipText) {
            tooltipText.textContent = "Go offline";
            tooltipText.style.setProperty("--tooltip-bg", "var(--success)");
            tooltipText.style.setProperty("--tooltip-color", "#000");
        }
    }
}

export function setActiveStep(stepNum) {
    const stepCards = {
        1: "card-emitter-auth",
        2: "card-tokenize",
        3: "card-regulator-auth",
        4: "card-freeze",
        6: "card-traceability"
    };

    for (const [num, id] of Object.entries(stepCards)) {
        const card = document.getElementById(id);
        const inputs = card.querySelectorAll("input, button");
        const cardNum = parseInt(num, 10);

        if (cardNum === stepNum) {
            card.classList.remove("locked", "done");
            card.classList.add("active");
            inputs.forEach(el => el.removeAttribute("disabled"));
        } else if (cardNum < stepNum) {
            card.classList.remove("locked", "active");
            card.classList.add("done");
            inputs.forEach(el => el.removeAttribute("disabled"));
        } else {
            card.classList.add("locked");
            card.classList.remove("active", "done");
            inputs.forEach(el => el.setAttribute("disabled", "true"));
        }
    }
}

export function showLoading() {
    const overlay = document.getElementById("loading-overlay");
    if (overlay) overlay.classList.remove("hidden");
}

export function hideLoading() {
    const overlay = document.getElementById("loading-overlay");
    if (overlay) overlay.classList.add("hidden");
}

export function logRequest(method, path, headers, body) {
    const consoleReq = document.getElementById("console-request");
    const headerLines = Object.entries(headers)
        .map(([k, v]) => `  ${k}: ${v.substring(0, 15)}${v.length > 15 ? '...' : ''}`)
        .join("\n");

    let bodyStr = "// No request payload";
    if (body) {
        bodyStr = JSON.stringify(body, null, 2);
    }

    const displayUrl = CONFIG.API_URL ? `${CONFIG.API_URL}${path}` : `http://10.10.10.150:8000${path} (via Proxy)`;
    consoleReq.innerHTML = `<span class="token-key">${method}</span> <span class="token-string">${displayUrl}</span>\n` +
        `<span class="token-key">Headers:</span>\n${headerLines}\n` +
        `<span class="token-key">Body:</span>\n${syntaxHighlight(bodyStr)}`;
}

export function logResponse(status, body) {
    const consoleRes = document.getElementById("console-response");
    let statusColorClass;
    if (status < 300) {
        statusColorClass = "token-boolean";
    } else if (status >= 400) {
        statusColorClass = "token-key";
    } else {
        statusColorClass = "token-number";
    }

    consoleRes.innerHTML = `<span class="token-key">HTTP Status:</span> <span class="${statusColorClass}">${status}</span>\n\n` +
        `<span class="token-key">JSON Response:</span>\n${syntaxHighlight(JSON.stringify(body, null, 2))}`;
}

export function showErrorOverlay(message, onRetry) {
    document.getElementById("error-message").innerText = message;
    document.getElementById("error-overlay").classList.remove("hidden");
    state.lastFailedAction = onRetry;
}

export function hideErrorOverlay() {
    document.getElementById("error-overlay").classList.add("hidden");
}

export function renderTimeline(historyArray) {
    const timelineEl = document.getElementById("blockchain-timeline");
    timelineEl.innerHTML = "";

    if (!historyArray || historyArray.length === 0) {
        timelineEl.innerHTML = `<span class="timeline-empty">No transactions found on the ledger for this asset.</span>`;
        return;
    }

    const gridHtml = `
        <div class="tx-grid">
            <div class="tx-grid-head">Block #</div>
            <div class="tx-grid-head">Action</div>
            <div class="tx-grid-head">DLT Actor</div>
            <div class="tx-grid-head">DN Certificate</div>
            <div class="tx-grid-head">Amount (EUR)</div>
            <div class="tx-grid-head">Fabric TxID</div>
            <div class="tx-grid-head">Timestamp</div>
            ${historyArray.map((tx, idx) => {
        const actionClass = tx.action === "TOKENIZED" ? "tokenize" : "freeze";
        const dateStr = new Date(tx.timestamp).toLocaleString("fr-FR");
        const amount = parseFloat(tx.amount) || 0;
        const blockNumber = tx.block_number || (142 + idx);
        const dnShort = String(tx.actor_dn).split(",")[0];
        const txIdShort = String(tx.tx_id).substring(0, 16) + "...";

        return `
                    <div class="tx-cell">${escapeHtml(blockNumber)}</div>
                    <div class="tx-cell tx-action ${actionClass}">${escapeHtml(tx.action)}</div>
                    <div class="tx-cell" title="${escapeHtml(tx.actor_msp)}">${escapeHtml(tx.actor_msp)}</div>
                    <div class="tx-cell" title="${escapeHtml(tx.actor_dn)}">${escapeHtml(dnShort)}</div>
                    <div class="tx-cell" style="text-align:right; font-family:var(--font-mono)">${amount.toLocaleString("fr-FR")}</div>
                    <div class="tx-cell" title="${escapeHtml(tx.tx_id)}" style="font-family:var(--font-mono); color:#5b93ff">${escapeHtml(txIdShort)}</div>
                    <div class="tx-cell">${escapeHtml(dateStr)}</div>
                `;
    }).join('')}
        </div>
    `;
    timelineEl.innerHTML = gridHtml;
}
