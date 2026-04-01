# Data Policy

This repository is code-first and template-first. It is intentionally not a container for real study artifacts.

## Public in this repo

- Source code
- Tests
- User-facing docs
- Blank/import templates
- Synthetic demo data

## Must stay out of this repo

- Real participant or study workspaces
- Downloaded media or audio caches
- Real transcripts
- Live SQLite databases
- LLM scoring outputs from real studies
- Backups, exports, or adjudication logs from active projects
- API keys, tokens, and environment files containing secrets

## Workspace rule

User workspaces should live outside the repo and hold all study-specific state under:

- `inputs/`
- `data/`
- `exports/`
- `cache/`
- `logs/`

