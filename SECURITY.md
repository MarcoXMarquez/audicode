# Security Policy

## Supported versions

Only the latest release (currently `v0.1.0-beta`) receives security fixes.

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Use GitHub's private reporting instead:
<https://github.com/MarcoXMarquez/audicode/security/advisories/new>

Include a description, reproduction steps, affected version and impact. We aim to acknowledge reports within a few days and to coordinate a fix and disclosure with you. This is a volunteer, beta-stage project, so there are no guaranteed response times or bug bounties.

## Deployment hardening

- When exposing AudiCode beyond localhost, set `AUTH_ENABLED=true`, serve it over HTTPS behind a reverse proxy, and set `SECURE_COOKIES=true`.
- Provider API keys are stored encrypted in `data/api_keys.json` with the key in `data/.key`. Protect and back up `data/` and never commit it.
- The agents can read files and run tools; run them only on material you are allowed to process.
- Prefer a local Ollama model for confidential material: cloud providers receive whatever you send them.

## Not legal advice

AudiCode is an assistive tool. Its output is not legal advice, is not a certification of ISO/IEC 27701 (or GDPR/LGPD/LFPDPPP/other) compliance, and may contain errors. Have results reviewed by a qualified professional.
