# AI RMF Log Analyzer + POA&M Ticketing Workflow

An offline-friendly, RMF-aligned cyber workflow that ingests Windows security telemetry, detects suspicious activity, enriches findings with risk + recommended actions, exports POA&M records, and routes remediation tasks through a lightweight ticket lifecycle.

This repo demonstrates end-to-end **RMF operations automation** (traceability, auditable artifacts, human-in-the-loop decision support) rather than “AI for AI’s sake”.

---

## What this does (end-to-end)

1. **Ingest + Normalize Logs**
   - Reads synthetic JSONL Windows-like events and optional real Security log exports
   - Outputs a normalized CSV for downstream analysis

2. **Detect Suspicious Patterns (Explainable Rules)**
   - Failed login burst (4625)
   - New account created (4720)
   - Added to Administrators group (4732)
   - Audit log cleared (1102)
   - Encoded PowerShell process execution (4688 with `-enc`)

3. **RMF-Aligned Enrichment (Human-in-the-loop)**
   - Adds analyst-ready summary, RMF-style risk statement, and recommended actions
   - Maps each finding to **NIST SP 800-53** control families (e.g., AC, AU, IR, SI)

4. **POA&M + Ticketing Workflow**
   - Exports POA&M-style records (`poam.csv`)
   - Creates filesystem-backed tickets with ownership + due dates + lifecycle status
   - Supports comments, evidence attachments, and closure justification
   - Produces an ISSO/manager dashboard (`DASHBOARD.md`)

---

## Architecture (high level)

```text
Raw Logs
  ├─ data/raw/synthetic_logs.jsonl
  └─ data/raw/real_events.json (optional)
        |
        v
run_day1.py  -> data/processed/normalized_events.csv
        |
        v
detect.py    -> data/processed/findings.json
        |
        v
ai_summarize.py -> findings_enriched.json + ai_summary.md
        |
        v
poam_export.py  -> poam.csv
        |
        v
ticketing.py + update_ticket.py -> tickets/{open,in_progress,awaiting_validation,closed}
        |
        v
dashboard.py -> DASHBOARD.md


