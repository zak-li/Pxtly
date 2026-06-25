export function getOrgName(profile) {
    if (profile.organization && profile.organization.name) return profile.organization.name;
    if (profile.msp_id === "BANK01MSP") return "Bank 01";
    if (profile.msp_id === "REG01MSP") return "Regulatory Authority";
    if (profile.email && profile.email.includes("bank01")) return "Bank 01";
    if (profile.email && profile.email.includes("reg01")) return "Regulatory Authority";
    return profile.msp_id || profile.role || "Unknown Organization";
}

export function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

export function syntaxHighlight(json) {
    if (!json) return "";
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\u[a-zA-Z0-9]{4}|\[^u]|[^\"])*"(\s*:)?|(true|false|null)|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function (match) {
        let cls = 'token-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'token-key';
            } else {
                cls = 'token-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'token-boolean';
        } else if (/null/.test(match)) {
            cls = 'token-null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}
