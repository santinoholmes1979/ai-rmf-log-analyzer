import json
import csv
from pathlib import Path
from datetime import datetime

def main():
    root = Path(__file__).resolve().parent
    enriched_path = root / "data" / "processed" / "findings_enriched.json"
    out_csv = root / "data" / "processed" / "poam.csv"

    findings = json.loads(enriched_path.read_text(encoding="utf-8-sig"))

    cols = [
        "poam_id",
        "date_identified",
        "severity",
        "weakness_or_deficiency",
        "nist_800_53_controls",
        "risk_statement",
        "recommended_actions",
        "status",
        "notes",
    ]

    today = datetime.now().date().isoformat()

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()

        for i, fin in enumerate(findings, start=1):
            w.writerow({
                "poam_id": f"POAM-{i:03d}",
                "date_identified": today,
                "severity": fin.get("severity"),
                "weakness_or_deficiency": f"{fin.get('rule_id')} - {fin.get('title')}",
                "nist_800_53_controls": ", ".join(fin.get("nist_800_53_controls", [])),
                "risk_statement": fin.get("risk_statement"),
                "recommended_actions": " | ".join(fin.get("recommended_actions", [])),
                "status": "Open",
                "notes": fin.get("rmf_note", ""),
            })

    print(f"[OK] Wrote: {out_csv}")

if __name__ == "__main__":
    main()
