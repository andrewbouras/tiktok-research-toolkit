# Publish Checklist

- Confirm the repo contains synthetic/example data only
- Run `python3 scripts/publish_check.py`
- Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q`
- Verify no credentials are hardcoded in source or docs
- Verify no SQLite, media, cache, or export artifacts are staged
- Verify README quickstart still works on a clean workspace

