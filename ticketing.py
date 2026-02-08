import json
from pathlib import Path
from datetime import datetime, timedelta
import csv

STATUS_DIRS = ["open", "in_progress", "awaiting_validation", "closed"]

def ensure_dirs(root: Path):
    for s in STATUS_DIRS:
        (root / "tickets" / s).mkdir(parents=True, exist_ok=True)

def load_poam(path: Path):
    rows = []
    with path.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def create_ticket(poam_row, ticket_id, owner="Cyber Ops"):
    today = datetime.now()

    sla_days = {
        "Critical": 7,
        "High": 14,
        "Medium": 30,
        "Low": 60
    }.get(poam_row["severity"], 30)

    return {
        "ticket_id": ticket_id,
        "status": "Open",
        "owner": owner,
        "created_date": today.isoformat(timespec="seconds"),
        "due_date": (today + timedelta(days=sla_days)).date().isoformat(),
        "severity": poam_row["severity"],
        "weakness": poam_row["weakness_or_deficiency"],
        "nist_controls": poam_row["nist_800_53_controls"],
        "risk_statement": poam_row["risk_statement"],
        "recommended_actions": poam_row["recommended_actions"],
        "evidence": [],
        "comments": [],
    }

def write_ticket(root: Path, status: str, ticket: dict):
    path = root / "tickets" / status / f"{ticket['ticket_id']}.json"
    path.write_text(json.dumps(ticket, indent=2), encoding="utf-8")
    return path

def main():
    root = Path(__file__).resolve().parent
    ensure_dirs(root)

    poam_path = root / "data" / "processed" / "poam.csv"
    poam_rows = load_poam(poam_path)

    print(f"[INFO] Loaded POA&M rows: {len(poam_rows)}")

    for i, row in enumerate(poam_rows, start=1):
        ticket_id = f"TICKET-{i:03d}"
        ticket = create_ticket(row, ticket_id)
        path = write_ticket(root, "open", ticket)
        print(f"[OK] Created ticket: {path}")

if __name__ == "__main__":
    main()
