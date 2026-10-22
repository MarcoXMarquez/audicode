# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0-beta]

First public beta of AudiCode, a fork of Odysseus focused on ISO/IEC 27701:2025 privacy audits.

### Added
- Native desktop app (`pywebview`) and Windows x64 standalone build (`AudiCode-v0.1.0-windows-x64.zip`).
- Eight ISO/IEC 27701:2025 audit skills (privacy policy, consent, data minimization, PII rights, PIA, transfers, processor contracts, incident response), prioritized over web search in the agent loop.
- `audit` (read-only) and `remediate` agents plus the `@general` subagent.
- Local document parsers (PDF, Office, slides, XLSX), CPU OCR and pills for long pasted text.
- Interactive skill demonstration modal, pre-flight model detection and Claude Desktop-style dark UI.
- Model backends: local Ollama or cloud providers with keys stored encrypted from the UI.
- English and Spanish READMEs, deployment notes (Docker), CONTRIBUTING and SECURITY documents.

### Known limitations
- macOS and Linux builds are not available yet; run from source.
