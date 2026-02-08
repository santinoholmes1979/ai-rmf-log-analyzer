\# AI RMF Log Analyzer



\*\*Offline-first log normalization, detection, and RMF-aligned reporting (NIST 800-53)\*\*



---



\## Executive Summary



AI RMF Log Analyzer is a lightweight security analytics pipeline that:

1\) normalizes raw log events,

2\) detects high-signal suspicious behaviors,

3\) maps findings to \*\*NIST 800-53 controls\*\*, and

4\) generates an auditable \*\*executive summary\*\* for governance and incident response.



Designed for \*\*disconnected environments\*\* and \*\*human-in-the-loop\*\* review.



---



\## What It Produces



\- `data/processed/findings.json` — detections with severity, description, and mapped controls

\- `data/processed/findings\_enriched.json` — detections enriched for analyst triage

\- `data/processed/ai\_summary.md` — leadership-ready brief

\- `data/processed/normalized\_events.csv` — normalized event trail



---



\## Quick Start



```powershell

python .\\run\_pipeline.py

notepad .\\data\\processed\\ai\_summary.md

---

## For Recruiters / Hiring Managers

- **Offline-first:** Core detection and reporting run without cloud dependencies.
- **Explainable by design:** Detections are rule-based and explicitly mapped to NIST 800-53 controls.
- **Human-in-the-loop:** Outputs support analyst judgment; no autonomous enforcement.
- **Audit-ready outputs:** CSV, JSON, and Markdown artifacts provide traceability.
- **Dependencies:** Python standard library only (no third-party runtime packages).

This project is intended to demonstrate governance-aligned security analytics suitable for regulated or restricted environments.




