\# RMF / NIST 800-53 Control Mapping



This project maps detections to NIST 800-53 controls to support auditability and governance-oriented reporting.

Mappings are intentionally conservative and designed for analyst review.



\## Example Mappings



\### AUTH-001 Failed login burst (possible password guessing)

\- AC-7 (Unsuccessful Logon Attempts)

\- IA-2 (Identification and Authentication)

\- AU-6 (Audit Review, Analysis, and Reporting)



\### ACCT-001 New user account created

\- AC-2 (Account Management)

\- IA-2 (Identification and Authentication)

\- AU-6 (Audit Review, Analysis, and Reporting)



\### PRIV-001 User added to Administrators group

\- AC-2 (Account Management)

\- AC-6 (Least Privilege)

\- AU-6 (Audit Review, Analysis, and Reporting)



\### AUD-001 Audit log cleared

\- AU-9 (Protection of Audit Information)

\- AU-6 (Audit Review, Analysis, and Reporting)

\- IR-4 (Incident Handling)



\### PROC-001 Encoded PowerShell execution detected

\- SI-4 (System Monitoring)

\- AU-6 (Audit Review, Analysis, and Reporting)

\- IR-4 (Incident Handling)



\## Notes

\- Control mappings indicate governance relevance, not root cause.

\- Analysts should validate context and confirm whether an event constitutes an incident.



