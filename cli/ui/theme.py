"""
cli/ui/theme.py
---------------
Centralised design tokens.
Corporate Institutional palette -- deep navy / slate / electric-blue.
"""

V1      = "#60a5fa"   # blue-400   highlights / user inputs
V2      = "#3b82f6"   # blue-500   primary accent / spinners
V3      = "#1d4ed8"   # blue-700   deep accent / blockchain ops
V4      = "#1e3a8a"   # blue-900   shadow / borders
MUTED   = "#64748b"   # slate-500  secondary text
DIM     = "#475569"   # slate-600  prompt colour
DIM2    = "#334155"   # slate-700  panel borders
SUCCESS = "#10b981"   # emerald-500
WARN    = "#f59e0b"   # amber-500
DANGER  = "#ef4444"   # red-500
NEUTRAL = "#cbd5e1"   # slate-300  body text
OFFLINE = "#b45309"   # amber-700  offline mode badge
CYAN    = "#00e5ff"

# Original banner preserved -- unicode block chars render in all modern terminals
BANNER_ART: list[str] = [
    f"           [{V2}]██████████████[/]",
    f"         [{V2}]██████████████████[/]",
    f"       [{V2}]██████████████████████[/]",
    f"       [{V2}]█████[/][{CYAN}]█[/][{V2}]██████████[/][{CYAN}]█[/][{V2}]█████[/]",
    f"       [{V2}]██████████████████████[/]",
    f"       [{V2}]██████████████████████[/]",
    f"         [{V2}]██████████████████[/]",
    f"           [{V2}]████      ████[/]          [{V2}]v3.0[/]",
]

# ---------------------------------------------------------------------------
# Textual CSS -- validated against Textual 0.x / 8.x layout engine.
#
# Key rules:
#  - Screen uses layout: vertical (default) so children stack top-to-bottom.
#  - #body is the flex region that fills all remaining space via height: 1fr.
#  - Left/right columns use height: 100% so they fill their parent Horizontal.
#  - Nested panes use height: 1fr / height: auto as appropriate.
#  - No "layers" property (removed -- caused rendering artefacts).
# ---------------------------------------------------------------------------

DASHBOARD_CSS = """
Screen {
    background: #0D1117;
    color: #cbd5e1;
    layout: vertical;
}

/* ---- Top status bar ---- */

#topbar {
    height: 1;
    background: #0D1117;
    border-bottom: solid #1e3a8a;
    layout: horizontal;
    padding: 0 2;
}

#topbar-title {
    color: #3b82f6;
    text-style: bold;
    width: 1fr;
    content-align: left middle;
}

#topbar-env {
    color: #475569;
    content-align: right middle;
    width: auto;
}

/* ---- Main body ---- */

#body {
    height: 1fr;
    layout: horizontal;
}

/* ---- Left column (60%) ---- */

#left-col {
    width: 60%;
    height: 100%;
    layout: vertical;
    border-right: solid #1e3a8a;
}

#health-pane {
    height: auto;
    min-height: 11;
    max-height: 13;
    border-bottom: solid #1e3a8a;
    padding: 0 1 1 1;
}

#stream-pane {
    height: 1fr;
    padding: 0 1;
}

/* ---- Right column (40%) ---- */

#right-col {
    width: 40%;
    height: 100%;
    layout: vertical;
}

#audit-pane {
    height: 1fr;
    padding: 0 1;
}

#stats-pane {
    height: 7;
    border-top: solid #1e3a8a;
    padding: 0 1 1 1;
}

/* ---- Pane headers ---- */

.pane-header {
    color: #3b82f6;
    text-style: bold;
    height: 1;
    margin-bottom: 1;
    border-bottom: solid #1e3a8a;
    padding: 0 1;
}

/* ---- DataTable ---- */

DataTable {
    background: #0D1117;
    height: 1fr;
}

DataTable > .datatable--header {
    background: #0D1117;
    color: #3b82f6;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #1e3a8a;
    color: #e2e8f0;
}

DataTable > .datatable--even-row {
    background: #030d1a;
}

/* ---- RichLog ---- */

RichLog {
    background: #0D1117;
    height: 1fr;
    padding: 0 1;
    scrollbar-color: #1e3a8a;
    scrollbar-background: #0D1117;
}

/* ---- Footer ---- */

Footer {
    background: #0D1117;
    color: #475569;
}

Footer > .footer--key {
    color: #3b82f6;
    background: #0D1117;
}
"""
