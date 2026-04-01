# Distribution and Archival

This repo is set up so we can grow distribution in three layers:

1. GitHub repository and releases as the source of truth
2. Zenodo archival for DOI-backed citation
3. PyPI and desktop binaries when we want a broader non-technical install path

## Zenodo DOI

The repo is ready to use `CITATION.cff` as the metadata source for Zenodo. We intentionally do not ship a `.zenodo.json` file so Zenodo can continue reading the root `CITATION.cff`.

Recommended setup:

1. Sign in to [Zenodo GitHub integration](https://zenodo.org/account/settings/github/).
2. Enable the `andrewbouras/tiktok-research-toolkit` repository.
3. Create a GitHub Release from a version tag such as `v0.1.0`.
4. Wait for Zenodo to archive that release and mint the DOI.
5. Paste the minted DOI back into `CITATION.cff` for the next release cycle if you want the citation file to include it.

Before each archived release:

- Update `pyproject.toml` version.
- Update `CITATION.cff` version and release date.
- Keep release notes focused on what changed, who the toolkit is for, and any migration notes for existing studies.

## GitHub Releases

GitHub Releases should be the public handoff point for the community:

- source tarball and wheel for Python users
- desktop archives for non-technical researchers on macOS and Windows
- release notes that explain setup, changes, and known limits

Use semantic tags such as `v0.1.0`, `v0.2.0`, and `v1.0.0`.

The repo includes a release-assets workflow that can build:

- `dist/*.whl`
- `dist/*.tar.gz`
- `dist/TikTokResearchToolkit-<platform>-<arch>.zip`

## PyPI Later

PyPI is intentionally a later step, after the GitHub repo and release flow feel stable.

When you are ready:

1. Create the project on [PyPI](https://pypi.org/).
2. Add a Trusted Publisher for this GitHub repository and workflow.
3. Run the manual PyPI publish workflow from GitHub Actions.

This keeps long-lived API tokens out of the repo and avoids credential sprawl.

## Desktop Binaries Later

Desktop binaries are also a later distribution layer. The main idea is:

1. Keep the local-first browser dashboard as the underlying product.
2. Build single-file desktop launchers for macOS and Windows.
3. Attach those archives to GitHub Releases so non-technical researchers can download them directly.

The current PyInstaller packaging script creates a zipped platform archive in `dist/` so release assets are easy to attach and preserve.
