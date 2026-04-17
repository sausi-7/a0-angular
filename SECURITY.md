# Security Policy

## Reporting a vulnerability

Please do **not** open a public GitHub issue for security vulnerabilities.

Instead, email the maintainers at **sau7singh@gmail.com** with:

- A description of the issue
- Steps to reproduce
- The affected version or commit
- Any suggested remediation

You will receive an acknowledgement within 72 hours. We aim to provide a fix or a timeline for one within 14 days.

## Scope

In scope:
- Remote code execution via the agent loop or schematic tools
- Path traversal / sandbox escape from generated-project workspace
- Credential leakage (BYOK keys at rest or in transit)
- Auth bypass (once auth ships in Phase 3)
- Server-side injection in the FastAPI backend

Out of scope:
- Vulnerabilities in third-party dependencies (file upstream)
- Attacks requiring already-compromised local machine access
- Social engineering

## Handling BYOK secrets

- User-supplied API keys are encrypted at rest using a key derived from a per-deployment secret in `A0_SECRET_KEY`.
- Keys are never logged. If you find a log line that includes a key, that is a security bug — please report it.

## Disclosure

We practice coordinated disclosure. After a fix ships, we publish an advisory via GitHub Security Advisories with credit to the reporter (or anonymous, if preferred).
