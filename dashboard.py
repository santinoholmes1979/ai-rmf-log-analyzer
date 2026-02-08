import json
from pathlib import Path
from datetime import datetime, date

STATUS_DIRS = ["open", "in_progress", "awaiting_validation", "closed"]
SEV_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

def load_all_tickets(root: Path):
    tickets = []
    for status in STATUS_DIRS:
        folder = root / "tickets" / status
        if not folder.exists():
            continue
        for p in folder.glob("*.json"):
            t = json.loads(p.read_text(encoding="utf-8-sig"))
            t["_path"] = str(p)
            t["_status_dir"] = status
            tickets.append(t)
    return tickets

def is_overdue(ticket):
    try:
        due = date.fromisoformat(ticket.get("due_date"))
        return date.today() > due and ticket.get("status") != "Closed"
    except Exception:
        return False

def main():
    root = Path(__file__).resolve().parent
    out_md = root / "DASHBOARD.md"

    tickets = load_all_tickets(root)

    by_status = {s: 0 for s in STATUS_DIRS}
    by_sev = {}
    overdue = []

    for t in tickets:
        s = t.get("_status_dir") or "open"
        by_status[s] += 1
        sev = t.get("severity", "Unknown")
        by_sev[sev] = by_sev.get(sev, 0) + 1
        if is_overdue(t):
            overdue.append(t)

    active = [t for t in tickets if t.get("_status_dir") in ("open", "in_progress", "awaiting_validation")]
    active.sort(key=lambda x: (SEV_ORDER.get(x.get("severity", "Low"), 99), x.get("due_date","9999-12-31")))

    control_counts = {}
    for t in tickets:
        controls = str(t.get("nist_controls","")).split(",")
        for c in [x.strip() for x in controls if x.strip()]:
            control_counts[c] = control_counts.get(c, 0) + 1

    lines = []
    lines.append("# RMF Ticketing Dashboard")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")

    lines.append("## Status Summary")
    for s in STATUS_DIRS:
        lines.append(f"- **{s}**: {by_status[s]}")
    lines.append("")

    lines.append("## Severity Summary")
    for sev, cnt in sorted(by_sev.items(), key=lambda x: SEV_ORDER.get(x[0], 99)):
        lines.append(f"- **{sev}**: {cnt}")
    lines.append("")

    lines.append("## Overdue Tickets")
    if not overdue:
        lines.append("- None")
    else:
        for t in sorted(overdue, key=lambda x: x.get("due_date","")):
            lines.append(f"- **{t['ticket_id']}** ({t.get('severity')}) due {t.get('due_date')} — {t.get('weakness')}")
    lines.append("")

    lines.append("## Top Active Tickets (by severity then due date)")
    if not active:
        lines.append("- None")
    else:
        for t in active[:10]:
            lines.append(f"- **{t['ticket_id']}** [{t.get('_status_dir')}] ({t.get('severity')}) due {t.get('due_date')} — {t.get('weakness')}")
    lines.append("")

    lines.append("## NIST 800-53 Control Impact Rollup")
    for c, cnt in sorted(control_counts.items(), key=lambda x: (-x[1], x[0]))[:15]:
        lines.append(f"- **{c}**: {cnt}")
    lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote: {out_md}")

if __name__ == "__main__":
    main()

