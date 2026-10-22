# Contributing to AudiCode

Thanks for your interest in AudiCode. This guide is short on purpose.

## Setup

```bash
git clone https://github.com/MarcoXMarquez/audicode.git
cd audicode
python -m venv venv
venv\Scripts\activate             # Windows (source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
pip install -r requirements-dev.txt   # test/lint tooling
python audicode_desktop.py
```

You need a model backend: local [Ollama](https://ollama.com) (`ollama pull qwen2.5-coder:7b`) or a cloud API key entered in the app UI.

## Workflow

1. Fork the repository and create a branch (`git checkout -b feat/new-iso-control`).
2. Keep changes focused; one topic per pull request.
3. Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, ...).
4. Run the tests (`pytest`) if present and make sure the desktop app starts via `python audicode_desktop.py`.
5. Open a pull request describing what changed and why.

## Adding a privacy skill

Skills live in `skills/<skill-name>/`. Each one needs a valid `SKILL.md` and deterministic verification rules mapped to **ISO/IEC 27701:2025** controls. Do not include real personal data in examples or fixtures.

## Security and secrets

Never commit API keys, `.env`, or anything under `data/`. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

AudiCode is a fork of Odysseus and is licensed under AGPL-3.0. By contributing you agree your contributions are licensed under the same terms.
