import json
from pathlib import Path
from datetime import datetime

STATUS_DIRS = ["open", "in_progress", "awaiting_validation", "closed"]

ALLOWED_TRANSITIONS = {
    "open": ["in_progress"],
    "in_progress": ["awaiting_validation", "open"],
    "awaiting_validation": ["closed", "in_progress"],
    "closed": ["in_progress"],  # reopen allowed
}

def find_ticket(root: Path, ticket_id: str):
    for status in STATUS_DIRS:
        path = root / "tickets" / status / f"{ticket_id}.json"
        if path.exists():
            return status, path
    return None, None

def load_ticket(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save_ticket(path: Path, ticket: dict):
    path.write_text(json.dumps(ticket, indent=2), encoding="utf-8")

def move_ticket(root: Path, ticket_id: str, new_status: str):
    if new_status not in STATUS_DIRS:
        raise ValueError(f"Invalid status: {new_status}")

    old_status, old_path = find_ticket(root, ticket_id)
    if not old_path:
        raise FileNotFoundError(f"Ticket not found: {ticket_id}")

    allowed = ALLOWED_TRANSITIONS.get(old_status, [])
    if new_status not in allowed:
        raise ValueError(f"Transition not allowed: {old_status} -> {new_status}")

    ticket = load_ticket(old_path)
    ticket["status"] = new_status
    ticket["last_updated"] = datetime.now().isoformat(timespec="seconds")

    new_path = root / "tickets" / new_status / f"{ticket_id}.json"
    save_ticket(new_path, ticket)

    old_path.unlink()
    return old_status, new_status, new_path

def add_comment(root: Path, ticket_id: str, comment: str):
    status, path = find_ticket(root, ticket_id)
    if not path:
        raise FileNotFoundError(f"Ticket not found: {ticket_id}")
    ticket = load_ticket(path)

    ticket.setdefault("comments", [])
    ticket["comments"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "comment": comment
    })
    ticket["last_updated"] = datetime.now().isoformat(timespec="seconds")

    save_ticket(path, ticket)
    return status, path

def add_evidence(root: Path, ticket_id: str, evidence_item: str):
    status, path = find_ticket(root, ticket_id)
    if not path:
        raise FileNotFoundError(f"Ticket not found: {ticket_id}")
    ticket = load_ticket(path)

    ticket.setdefault("evidence", [])
    ticket["evidence"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "evidence": evidence_item
    })
    ticket["last_updated"] = datetime.now().isoformat(timespec="seconds")

    save_ticket(path, ticket)
    return status, path

def close_ticket(root: Path, ticket_id: str, justification: str):
    # Add justification and move to closed
    add_comment(root, ticket_id, f"CLOSURE JUSTIFICATION: {justification}")
    old_status, new_status, new_path = move_ticket(root, ticket_id, "closed")
    return old_status, new_status, new_path

def usage():
    print("""
Usage:
  python update_ticket.py move <TICKET-###> <open|in_progress|awaiting_validation|closed>
  python update_ticket.py comment <TICKET-###> "comment text"
  python update_ticket.py evidence <TICKET-###> "evidence text or file path"
  python update_ticket.py close <TICKET-###> "closure justification"
""".strip())

def main():
    import sys
    root = Path(__file__).resolve().parent

    if len(sys.argv) < 3:
        usage()
        return

    cmd = sys.argv[1].lower()
    ticket_id = sys.argv[2]

    try:
        if cmd == "move":
            if len(sys.argv) != 4:
                usage(); return
            new_status = sys.argv[3]
            old_status, new_status, new_path = move_ticket(root, ticket_id, new_status)
            print(f"[OK] Moved {ticket_id}: {old_status} -> {new_status} ({new_path})")

        elif cmd == "comment":
            if len(sys.argv) < 4:
                usage(); return
            comment = " ".join(sys.argv[3:])
            status, path = add_comment(root, ticket_id, comment)
            print(f"[OK] Comment added to {ticket_id} ({status}): {path}")

        elif cmd == "evidence":
            if len(sys.argv) < 4:
                usage(); return
            evidence_item = " ".join(sys.argv[3:])
            status, path = add_evidence(root, ticket_id, evidence_item)
            print(f"[OK] Evidence added to {ticket_id} ({status}): {path}")

        elif cmd == "close":
            if len(sys.argv) < 4:
                usage(); return
            justification = " ".join(sys.argv[3:])
            old_status, new_status, new_path = close_ticket(root, ticket_id, justification)
            print(f"[OK] Closed {ticket_id}: {old_status} -> {new_status} ({new_path})")

        else:
            usage()

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
