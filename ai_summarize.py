import json
from pathlib import Path
from datetime import datetime

# --- simple RMF-style templates (works without any API calls) ---
SEVERITY_GUIDANCE = {
    "Critical": "Immediate response required; potential compromise or loss of audit integrity.",
    "High": "Likely security impact; requires timely investigation and remediation.",
    "Medium": "Suspicious behavior; investigate to confirm legitimacy and tune controls.",
    "Low": "Informational; track trends and verify expected behavior.",
}

DEFAULT_ACTIONS = {
    "AUTH-001": [
        "Validate whether the source IP is expected (VPN, admin subnet, known jump box).",
        "Check for additional failed logins for the same user across other hosts.",
        "If suspicious: reset credentials, review MFA status, and block IP if appropriate.",
        "Confirm AC-7 lockout policy and alert thresholds are enforced."
    ],
    "ACCT-001": [
        "Confirm account creation authorization (ticket/change record).",
        "Review who initiated creation and from what host.",
        "Check whether the account has been used for interactive logons.",
        "Ensure account provisioning follows AC-2 approval workflow."
    ],
    "PRIV-001": [
        "Confirm the group membership change is authorized and documented.",
        "Identify the actor who made the change and the originating system.",
        "Review recent activity for the newly-privileged account (logons, processes).",
        "Verify least privilege and remove membership if not required."
    ],
    "AUD-001": [
        "Treat as potential incident: preserve evidence and notify incident response.",
        "Determine which account cleared logs and why; validate authorization.",
        "Check for gaps in audit coverage and whether forwarding/central logging exists.",
        "Verify AU-9 protections (access controls, forwarding, write-once storage)."
    ],
    "PROC-001": [
        "Decode and review the PowerShell command if possible; look for persistence or payload download.",
        "Correlate process creation with network connections and file writes.",
        "Verify whether script execution policy controls are enforced.",
        "If suspicious: isolate host and initiate incident handling procedures."
    ],
}

DEFAULT_RISK = {
    "AUTH-001": "Repeated authentication failures may indicate credential guessing, increasing the likelihood of unauthorized access if controls (e.g., lockout/MFA) are ineffective.",
    "ACCT-001": "Unauthorized account creation can enable persistence and unauthorized access, undermining account management controls and auditability.",
    "PRIV-001": "Unapproved elevation to administrative privileges can enable lateral movement and system compromise, violating least privilege expectations.",
    "AUD-001": "Clearing audit logs reduces visibility and may indicate anti-forensic activity, impairing detection, response, and accountability.",
    "PROC-001": "Obfuscated PowerShell execution may indicate malicious command execution and can facilitate defense evasion, persistence, or payload delivery.",
}

def rmf_summary(finding: dict) -> str:
    rule_id = finding.get("rule_id")
    severity = finding.get("severity")
    title = finding.get("title")
    controls = ", ".join(finding.get("nist_800_53_controls", []))
    guidance = SEVERITY_GUIDANCE.get(severity, "")

    return (
        f"**{title}**\n\n"
        f"- **Rule:** {rule_id}\n"
        f"- **Severity:** {severity} — {guidance}\n"
        f"- **NIST 800-53 Controls:** {controls}\n"
    )

def main():
    root = Path(__file__).resolve().parent
    findings_path = root / "data" / "processed" / "findings.json"
    out_findings_path = root / "data" / "processed" / "findings_enriched.json"
    out_md = root / "data" / "processed" / "ai_summary.md"

    findings = json.loads(findings_path.read_text(encoding="utf-8-sig"))

    enriched = []
    lines = []
    lines.append(f"# AI-Assisted RMF Findings Summary")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")

    for f in findings:
        rule_id = f.get("rule_id")
        summary = rmf_summary(f)
        risk = DEFAULT_RISK.get(rule_id, "Potential security risk identified; investigate and assess impact.")
        actions = DEFAULT_ACTIONS.get(rule_id, ["Investigate and validate legitimacy.", "Document outcome and remediate as appropriate."])

        f["ai_summary"] = summary
        f["risk_statement"] = risk
        f["recommended_actions"] = actions

        enriched.append(f)

        # Markdown section
        lines.append(f"## [{f.get('severity')}] {f.get('rule_id')} — {f.get('title')}\n")
        lines.append(summary)
        lines.append(f"**Risk statement (RMF-style):** {risk}\n")
        lines.append("**Recommended actions:**")
        for a in actions:
            lines.append(f"- {a}")
        lines.append("")  # blank line

    out_findings_path.write_text(json.dumps(enriched, indent=2), encoding="utf-8")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Wrote: {out_findings_path}")
    print(f"[OK] Wrote: {out_md}")

if __name__ == "__main__":
    main()
