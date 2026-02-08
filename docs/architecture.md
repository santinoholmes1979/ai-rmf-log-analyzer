\# Architecture



\## Goal

Normalize security-relevant events, detect high-signal behaviors, map findings to NIST 800-53 controls, and generate analyst + executive outputs.



\## Pipeline

Raw logs (or synthetic examples)

&nbsp;  ↓

Normalization (consistent schema)

&nbsp;  ↓

Rule-based detections (auditable logic)

&nbsp;  ↓

Control mapping (NIST 800-53)

&nbsp;  ↓

Enrichment (context, triage fields)

&nbsp;  ↓

Reporting (Markdown summary + JSON artifacts)



\## Components

\- `detect.py`

&nbsp; - Reads input events

&nbsp; - Writes:

&nbsp;   - `data/processed/normalized\_events.csv`

&nbsp;   - `data/processed/findings.json`

\- `ai\_summarize.py`

&nbsp; - Reads findings

&nbsp; - Writes:

&nbsp;   - `data/processed/findings\_enriched.json`

&nbsp;   - `data/processed/ai\_summary.md`

\- `run\_pipeline.py`

&nbsp; - Runs both steps with one command



\## Design Principles

\- Offline-first

\- Explainable (rule-based + explicit mappings)

\- Human-in-the-loop decision support

\- Outputs are auditable artifacts (CSV/JSON/MD)



