\# Threat Model (High-Level)



\## Assets

\- Integrity of audit logs and security telemetry

\- Privileged group membership and account state

\- Analyst trust in detection outputs

\- Governance traceability (controls mapping, reporting)



\## Adversary Behaviors Modeled (Examples)

\- Password guessing / brute-force patterns

\- Unauthorized account creation

\- Privilege escalation (admin group changes)

\- Defense evasion (audit log clearing)

\- Suspicious execution patterns (encoded PowerShell)



\## Assumptions

\- Inputs are representative of host/auth/audit telemetry

\- Pipeline is used for decision support, not as an autonomous enforcement system

\- Findings require analyst confirmation



\## Out of Scope

\- Malware classification

\- Network IDS/IPS correlation

\- Full incident response automation

\- True attribution



