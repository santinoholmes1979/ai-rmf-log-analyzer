
print("RUN_DAY1 STARTED")

import json
import csv
from pathlib import Path

def read_real_events_json(path: Path):
    if not path.exists():
        print(f"[INFO] No real events file found (ok): {path}")
        return []

    raw_text = path.read_text(encoding="utf-8-sig").lstrip("\ufeff")
    data = json.loads(raw_text)

    if isinstance(data, dict):
        data = [data]

    events = []
    for e in data:
        events.append({
            "source": "real",
            "host": e.get("MachineName") or "UNKNOWN",
            "timestamp": str(e.get("TimeCreated") or ""),
            "event_id": e.get("Id"),
            "level": e.get("LevelDisplayName"),
            "provider": e.get("ProviderName"),
            "user": None,
            "ip": None,
            "message": e.get("Message"),
            "tags": None,
        })
    return events

def read_jsonl(path: Path):
    events = []
    if not path.exists():
        print(f"[WARN] Missing synthetic file: {path}")
        return events
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.lstrip("\ufeff")
            events.append(json.loads(line))
    return events

def write_csv(events, out_path: Path):
    cols = ["source","host","timestamp","event_id","level","provider","user","ip","message","tags"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for e in events:
            w.writerow({c: e.get(c) for c in cols})

def main():
    root = Path(__file__).resolve().parent
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"

    print(f"[INFO] Project root: {root}")
    print(f"[INFO] Raw dir: {raw_dir}")

    synthetic = read_jsonl(raw_dir / "synthetic_logs.jsonl")
    real = read_real_events_json(raw_dir / "real_events.json")
    events = synthetic + real

    print(f"[INFO] Synthetic events: {len(synthetic)}")
    print(f"[INFO] Real events: {len(real)}")
    print(f"[INFO] Total events: {len(events)}")

    for e in events[:5]:
        print(f"{e.get('timestamp')} | {e.get('event_id')} | {e.get('level')} | {e.get('source')}")

    out_csv = processed_dir / "normalized_events.csv"
    write_csv(events, out_csv)
    print(f"[OK] Saved: {out_csv}")

if __name__ == "__main__":
    main()
