# Publish Checklist

- Confirm the repo contains synthetic/example data only
- Run `python3 scripts/publish_check.py`
- Run `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q`
- Confirm `pyproject.toml` and `CITATION.cff` carry the release version you intend to publish
- Verify no credentials are hardcoded in source or docs
- Verify no SQLite, media, cache, or export artifacts are staged
- Verify README quickstart still works on a clean workspace
- Create or update the Git tag that will back the GitHub Release, for example `v0.1.0`
- Publish the GitHub Release and confirm the release assets include the wheel, source tarball, and desktop archives
- If Zenodo is connected, confirm the release minted a DOI and that the metadata matches `CITATION.cff`
- If publishing to PyPI, run the manual PyPI workflow only after the Trusted Publisher has been configured on PyPI
