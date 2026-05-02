import json, requests

GRAFANA = "http://10.10.10.150:3000"
AUTH    = ("admin", "admin")
DS      = "ffgx1hbr25a0wc"

def ds():
    return {"type": "prometheus", "uid": DS}

def q(expr, legend="", ref="A"):
    return {
        "datasource": ds(),
        "expr": expr,
        "legendFormat": legend or "__auto",
        "refId": ref,
        "instant": False,
        "range": True,
    }

def stat(pid, title, expr, x, y, w, h, unit="short", thresholds=None,
         mappings=None, fixed=None, decimals=None, color_mode="value",
         graph="area", text_mode="auto", legend=""):
    field = {"unit": unit, "custom": {}}
    if fixed:
        field["color"] = {"mode": "fixed", "fixedColor": fixed}
        field["thresholds"] = {"mode": "absolute", "steps": [{"color": fixed, "value": None}]}
    else:
        field["color"] = {"mode": "thresholds"}
        field["thresholds"] = thresholds or {"mode": "absolute", "steps": [{"color": "blue", "value": None}]}
    if mappings:
        field["mappings"] = mappings
    if decimals is not None:
        field["decimals"] = decimals
    return {
        "id": pid, "title": title, "type": "stat",
        "datasource": ds(),
        "targets": [q(expr, legend or title, "A")],
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"]},
            "colorMode": color_mode,
            "graphMode": graph,
            "justifyMode": "center",
            "orientation": "auto",
            "textMode": text_mode,
            "wideLayout": True,
            "showPercentChange": False,
            "percentChangeColorMode": "standard"
        },
        "fieldConfig": {"defaults": field, "overrides": []}
    }

def gauge(pid, title, expr, x, y, w, h, unit="percent", thresholds=None, max_v=100):
    return {
        "id": pid, "title": title, "type": "gauge",
        "datasource": ds(),
        "targets": [q(expr, title, "A")],
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "options": {
            "reduceOptions": {"calcs": ["lastNotNull"]},
            "showThresholdLabels": False,
            "showThresholdMarkers": True,
            "orientation": "auto",
            "minVizHeight": 75,
            "minVizWidth": 75,
            "sizing": "auto"
        },
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "min": 0,
                "max": max_v,
                "color": {"mode": "thresholds"},
                "thresholds": thresholds or {"mode": "absolute", "steps": [
                    {"color": "green", "value": None},
                    {"color": "yellow", "value": 70},
                    {"color": "red", "value": 90}
                ]},
                "custom": {}
            },
            "overrides": []
        }
    }

def timeseries(pid, title, targets, x, y, w, h, unit="short", fill=18,
               line_width=2, overrides=None, legend_mode="list", show_legend=True):
    return {
        "id": pid, "title": title, "type": "timeseries",
        "datasource": ds(),
        "targets": targets,
        "gridPos": {"x": x, "y": y, "w": w, "h": h},
        "options": {
            "tooltip": {"mode": "multi", "sort": "desc"},
            "legend": {
                "displayMode": legend_mode if show_legend else "hidden",
                "placement": "bottom",
                "calcs": ["mean", "max"] if legend_mode == "table" else [],
                "showLegend": show_legend
            }
        },
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "custom": {
                    "drawStyle": "line",
                    "lineInterpolation": "smooth",
                    "lineWidth": line_width,
                    "fillOpacity": fill,
                    "gradientMode": "opacity",
                    "spanNulls": True,
                    "showPoints": "never",
                    "pointSize": 5,
                    "stacking": {"mode": "none", "group": "A"},
                    "axisLabel": "",
                    "axisPlacement": "auto",
                    "scaleDistribution": {"type": "linear"},
                    "thresholdsStyle": {"mode": "off"}
                }
            },
            "overrides": overrides or []
        }
    }

panels = []
pid = 1

# ─── Row 1: Top KPI strip (6 hero cards, h=5) ─────────────────────────────────
y = 0

panels.append(stat(pid, "Services Up", 'sum(up)', 0, y, 4, 5,
    unit="short", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "red", "value": None},
        {"color": "yellow", "value": 3},
        {"color": "green", "value": 5}
    ]})); pid += 1

panels.append(stat(pid, "Request Rate", 'sum(rate(http_requests_total[2m]))', 4, y, 4, 5,
    unit="reqps", color_mode="value", fixed="blue", graph="area",
    decimals=1)); pid += 1

panels.append(stat(pid, "Latency p95",
    'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[2m])) by (le))',
    8, y, 4, 5, unit="s", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 0.5},
        {"color": "red", "value": 1.5}
    ]})); pid += 1

panels.append(stat(pid, "Error Rate",
    'sum(rate(http_requests_total{status=~"5.."}[2m])) / clamp_min(sum(rate(http_requests_total[2m])), 0.001) * 100',
    12, y, 4, 5, unit="percent", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 1},
        {"color": "red", "value": 5}
    ]})); pid += 1

panels.append(stat(pid, "CPU",
    '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)',
    16, y, 4, 5, unit="percent", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 70},
        {"color": "red", "value": 90}
    ]})); pid += 1

panels.append(stat(pid, "Memory",
    '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    20, y, 4, 5, unit="percent", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 75},
        {"color": "red", "value": 90}
    ]})); pid += 1
y += 5

# ─── Row 2: Service Availability timeline (full width, h=5) ────────────────────
panels.append({
    "id": pid, "title": "Service Availability",
    "type": "state-timeline",
    "datasource": ds(),
    "targets": [
        q('up{job="node-exporter"}', "System", "A"),
        q('up{job="rwa-api"}', "RWA API", "B"),
        q('up{job="postgres"}', "PostgreSQL", "C"),
        q('up{job="redis"}', "Redis", "D"),
        q('up{job="prometheus"}', "Prometheus", "E"),
    ],
    "gridPos": {"x": 0, "y": y, "w": 24, "h": 5},
    "options": {
        "mergeValues": True, "showValue": "never",
        "alignValue": "center", "rowHeight": 0.9,
        "legend": {"displayMode": "list", "placement": "bottom", "showLegend": True},
        "tooltip": {"mode": "single"}
    },
    "fieldConfig": {
        "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {"mode": "absolute", "steps": [
                {"color": "red", "value": None},
                {"color": "green", "value": 1}
            ]},
            "mappings": [{"type": "value", "options": {
                "0": {"text": "DOWN", "color": "red", "index": 0},
                "1": {"text": "UP", "color": "green", "index": 1}
            }}],
            "custom": {"lineWidth": 0, "fillOpacity": 80}
        },
        "overrides": []
    }
}); pid += 1
y += 5

# ─── Row 3: API Traffic & Latency (h=10) ───────────────────────────────────────
panels.append(timeseries(pid, "Request Rate",
    [q('sum(rate(http_requests_total[2m]))', "Total", "A")],
    0, y, 12, 10, unit="reqps", fill=25, line_width=3, show_legend=False,
    overrides=[
        {"matcher": {"id": "byName", "options": "Total"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "blue"}}
        ]}
    ])); pid += 1

panels.append({
    "id": pid, "title": "Latency Distribution",
    "type": "heatmap",
    "datasource": ds(),
    "targets": [q('sum(rate(http_request_duration_seconds_bucket[2m])) by (le)', "{{le}}", "A")],
    "gridPos": {"x": 12, "y": y, "w": 12, "h": 10},
    "options": {
        "calculate": False,
        "yAxis": {"unit": "s", "decimals": 2},
        "color": {"scheme": "Spectral", "mode": "scheme", "exponent": 0.5, "reverse": True, "steps": 64},
        "tooltip": {"show": True, "yHistogram": False},
        "legend": {"show": True},
        "rowsFrame": {"layout": "auto"},
        "cellGap": 1,
        "filterValues": {"le": 1e-9}
    },
    "fieldConfig": {
        "defaults": {"custom": {"scaleDistribution": {"type": "log", "log": 2}, "hideFrom": {"tooltip": False, "viz": False, "legend": False}}},
        "overrides": []
    }
}); pid += 1
y += 10

# ─── Row 4: System resources (h=8) ─────────────────────────────────────────────
panels.append(timeseries(pid, "CPU and Memory",
    [
        q('100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)', "CPU %", "A"),
        q('(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100', "Memory %", "B"),
    ],
    0, y, 12, 8, unit="percent", fill=20, line_width=2,
    legend_mode="table",
    overrides=[
        {"matcher": {"id": "byName", "options": "CPU %"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "blue"}}
        ]},
        {"matcher": {"id": "byName", "options": "Memory %"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "purple"}}
        ]},
    ])); pid += 1

panels.append(timeseries(pid, "Disk and Network",
    [
        q('sum(rate(node_disk_read_bytes_total[2m]))', "Disk Read", "A"),
        q('sum(rate(node_disk_written_bytes_total[2m]))', "Disk Write", "B"),
        q('sum(rate(node_network_receive_bytes_total{device!~"lo|docker.*|br.*|veth.*"}[2m]))', "Net In", "C"),
        q('sum(rate(node_network_transmit_bytes_total{device!~"lo|docker.*|br.*|veth.*"}[2m]))', "Net Out", "D"),
    ],
    12, y, 12, 8, unit="Bps", fill=12, line_width=2,
    legend_mode="table")); pid += 1
y += 8

# ─── Row 5: Data tier (h=8) ────────────────────────────────────────────────────
panels.append(timeseries(pid, "PostgreSQL Activity",
    [
        q('sum(rate(pg_stat_database_xact_commit[2m]))', "Commits/s", "A"),
        q('sum(rate(pg_stat_database_xact_rollback[2m]))', "Rollbacks/s", "B"),
        q('pg_stat_activity_count{state="active"}', "Active Connections", "C"),
    ],
    0, y, 12, 8, unit="short", fill=18, line_width=2,
    legend_mode="table",
    overrides=[
        {"matcher": {"id": "byName", "options": "Commits/s"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "green"}}
        ]},
        {"matcher": {"id": "byName", "options": "Rollbacks/s"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "red"}}
        ]},
        {"matcher": {"id": "byName", "options": "Active Connections"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "blue"}},
            {"id": "custom.axisPlacement", "value": "right"}
        ]}
    ])); pid += 1

panels.append(timeseries(pid, "Redis Activity",
    [
        q('rate(redis_keyspace_hits_total[2m])', "Hits/s", "A"),
        q('rate(redis_keyspace_misses_total[2m])', "Misses/s", "B"),
        q('redis_memory_used_bytes', "Memory Used", "C"),
    ],
    12, y, 12, 8, unit="short", fill=18, line_width=2,
    legend_mode="table",
    overrides=[
        {"matcher": {"id": "byName", "options": "Hits/s"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "green"}}
        ]},
        {"matcher": {"id": "byName", "options": "Misses/s"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "red"}}
        ]},
        {"matcher": {"id": "byName", "options": "Memory Used"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "orange"}},
            {"id": "unit", "value": "bytes"},
            {"id": "custom.axisPlacement", "value": "right"}
        ]}
    ])); pid += 1
y += 8

# ─── Row 6: Business KPIs (h=5) ───────────────────────────────────────────────
panels.append(stat(pid, "Total Transactions", 'sum(rwa_transactions_total)',
    0, y, 5, 5, unit="short", color_mode="value", fixed="purple", graph="area")); pid += 1

panels.append(stat(pid, "Average AML Score", 'avg(rwa_aml_score_avg)',
    5, y, 5, 5, unit="percentunit", decimals=2, color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 0.5},
        {"color": "red", "value": 0.8}
    ]})); pid += 1

panels.append(stat(pid, "Compliance Blocks", 'sum(rwa_compliance_blocks_total)',
    10, y, 5, 5, unit="short", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 10},
        {"color": "red", "value": 50}
    ]})); pid += 1

panels.append(stat(pid, "KYC Expiring", 'sum(rwa_kyc_expiring_count)',
    15, y, 5, 5, unit="short", color_mode="background",
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "yellow", "value": 5},
        {"color": "red", "value": 20}
    ]})); pid += 1

panels.append(stat(pid, "Circuit Breaker", 'max(rwa_circuit_breaker_state)',
    20, y, 4, 5, color_mode="background", graph="none",
    mappings=[{"type": "value", "options": {
        "0": {"text": "CLOSED", "color": "green", "index": 0},
        "1": {"text": "OPEN", "color": "red", "index": 1},
        "2": {"text": "HALF-OPEN", "color": "yellow", "index": 2}
    }}],
    thresholds={"mode": "absolute", "steps": [
        {"color": "green", "value": None},
        {"color": "red", "value": 1}
    ]})); pid += 1
y += 5

# ─── Row 7: Business trends (h=8) ─────────────────────────────────────────────
panels.append(timeseries(pid, "Transaction Rate",
    [q('rate(rwa_transactions_total[2m])', "{{type}}", "A")],
    0, y, 12, 8, unit="ops", fill=25, line_width=3,
    legend_mode="table")); pid += 1

panels.append(timeseries(pid, "AML Score Trend",
    [q('avg(rwa_aml_score_avg)', "AML Score", "A")],
    12, y, 12, 8, unit="percentunit", fill=30, line_width=3, show_legend=False,
    overrides=[
        {"matcher": {"id": "byName", "options": "AML Score"}, "properties": [
            {"id": "color", "value": {"mode": "fixed", "fixedColor": "purple"}},
            {"id": "min", "value": 0},
            {"id": "max", "value": 1}
        ]}
    ])); pid += 1

# ─── Build & Deploy ───────────────────────────────────────────────────────────
dash = {
    "uid": "rwa-platform",
    "title": "RWA Platform",
    "tags": ["rwa", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "schemaVersion": 38,
    "version": 1,
    "panels": panels,
    "time": {"from": "now-3h", "to": "now"},
    "timepicker": {},
    "graphTooltip": 1,
    "fiscalYearStartMonth": 0,
    "liveNow": False,
    "weekStart": ""
}

for uid in ["rwa-ops-v2", "rwa-ops-professional", "rwa-monitoring"]:
    dr = requests.delete(f"{GRAFANA}/api/dashboards/uid/{uid}", auth=AUTH, timeout=10)
    print(f"Delete {uid}: HTTP {dr.status_code}")

with open("deployment/monitoring/grafana_dashboard.json", "w") as f:
    json.dump(dash, f, indent=2)
print(f"Saved JSON ({len(panels)} panels)")

r = requests.post(
    f"{GRAFANA}/api/dashboards/db",
    json={"dashboard": dash, "overwrite": True, "folderId": 0},
    headers={"Content-Type": "application/json"},
    auth=AUTH, timeout=15
)
print(f"Deploy HTTP {r.status_code}: {r.json()}")
