import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# -----------------------
# Helpers
# -----------------------
def load_normalized_csv(path: Path):
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["event_id"] = int(r["event_id"]) if r.get("event_id") else None
            rows.append(r)
    return rows

def parse_ts(ts: str):
    if not ts:
        return None
    try:
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)
    except Exception:
        return None

def add_finding(findings, rule_id, severity, title, evidence, nist_controls, rmf_note):
    findings.append({
        "rule_id": rule_id,
        "severity": severity,
        "title": title,
        "evidence": evidence,
        "nist_800_53_controls": nist_controls,
        "rmf_note": rmf_note,
    })

# -----------------------
# Detection Rules
# -----------------------
def rule_failed_login_burst(events, window_minutes=5, threshold=3):
    failed = [e for e in events if e.get("event_id") == 4625]
    buckets = defaultdict(list)

    for e in failed:
        key = (e.get("user"), e.get("ip"))
        dt = parse_ts(e.get("timestamp", ""))
        if dt:
            buckets[key].append((dt, e))

    findings = []
    for (user, ip), items in buckets.items():
        items.sort(key=lambda x: x[0])
        for i in range(len(items)):
            start = items[i][0]
            end = start + timedelta(minutes=window_minutes)
            window = [it for (t, it) in items if start <= t <= end]
            if len(window) >= threshold:
                add_finding(
                    findings,
                    "AUTH-001",
                    "Medium",
                    "Failed login burst (possible password guessing)",
                    {"user": user, "ip": ip, "count": len(window), "window_minutes": window_minutes},
                    ["AC-7", "IA-2", "AU-6"],
                    "Supports monitoring of authentication anomalies and audit review."
                )
                break
    return findings

def rule_admin_account_created(events):
    findings = []
    for e in events:
        if e.get("event_id") == 4720:
            add_finding(
                findings,
                "ACCT-001",
                "High",
                "New user account created",
                {"event": e},
                ["AC-2", "IA-2", "AU-6"],
                "Account creation must be authorized and auditable."
            )
    return findings

def rule_added_to_admin_group(events):
    findings = []
    for e in events:
        if e.get("event_id") == 4732:
            add_finding(
                findings,
                "PRIV-001",
                "High",
                "User added to Administrators group",
                {"event": e},
                ["AC-2", "AC-6", "AU-6"],
                "Privilege escalation should follow least privilege principles."
            )
    return findings

def rule_audit_log_cleared(events):
    findings = []
    for e in events:
        if e.get("event_id") == 1102:
            add_finding(
                findings,
                "AUD-001",
                "Critical",
                "Audit log cleared",
                {"event": e},
                ["AU-9", "AU-6", "IR-4"],
                "Audit integrity loss may indicate anti-forensics activity."
            )
    return findings

def rule_encoded_powershell(events):
    findings = []
    for e in events:
        msg = (e.get("message") or "").lower()
        if e.get("event_id") == 4688 and "powershell" in msg and (" -enc " in msg or "encodedcommand" in msg):
            add_finding(
                findings,
                "PROC-001",
                "High",
                "Encoded PowerShell execution detected",
                {"event": e},
                ["SI-4", "AU-6", "IR-4"],
                "Obfuscated command execution may indicate malicious activity."
            )
    return findings

# -----------------------
# Main
# -----------------------
def main():
    root = Path(__file__).resolve().parent
    normalized = root / "data" / "processed" / "normalized_events.csv"
    out_findings = root / "data" / "processed" / "findings.json"

    events = load_normalized_csv(normalized)

    findings = []
    findings += rule_failed_login_burst(events)
    findings += rule_admin_account_created(events)
    findings += rule_added_to_admin_group(events)
    findings += rule_audit_log_cleared(events)
    findings += rule_encoded_powershell(events)

    out_findings.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"[OK] Findings written: {len(findings)} -> {out_findings}")

    for f in findings:
        print(f"- [{f['severity']}] {f['rule_id']} {f['title']} -> Controls: {', '.join(f['nist_800_53_controls'])}")

if __name__ == "__main__":
    main()
