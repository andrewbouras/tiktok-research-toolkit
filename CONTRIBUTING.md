# Contributing

## Development setup

Preferred:

```bash
uv sync --extra dashboard --extra dev
```

Fallback:

```bash
python3 -m pip install -e ".[dashboard,dev]"
```

## Before opening a PR

- Run `python3 scripts/publish_check.py`
- Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q`
- Make sure no real study artifacts or secrets are introduced
- Keep user-facing docs aligned with any CLI or workspace changes

## Scope guardrails

- Do not add real TikTok datasets or live study outputs to the repo
- Do not hardcode credentials or machine-specific paths
- Keep the public command surface under `tiktok-research`

