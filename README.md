# TikTok Research Toolkit

Open-source, local-first infrastructure for reproducible short-form health video studies. The public repo contains the software, templates, tests, docs, and a synthetic demo workspace only. Real study data, media caches, live databases, and user-generated outputs belong in private workspaces outside the repo.

## Quick start

For contributors:

```bash
uv sync --extra dashboard --extra dev
```

Fallback if `uv` is not available:

```bash
python3 -m pip install -e ".[dashboard,dev]"
```

Create a demo workspace and run the dashboard:

```bash
tiktok-research init-demo /tmp/tiktok-demo
tiktok-research run-dashboard /tmp/tiktok-demo
```

Create a blank study workspace:

```bash
tiktok-research init-study /tmp/my-study --study-name "My Lab TikTok Study"
```

Import a legacy workbook/json/transcript workflow:

```bash
tiktok-research import-legacy /tmp/imported-study \
  --workbook /path/to/TikTok_UI_Video_Coding_Template_v2.xlsx \
  --metadata-json /path/to/collected_videos.json \
  --transcripts-dir /path/to/transcripts \
  --replacement-json /path/to/replacement_candidates.json \
  --database /path/to/research_dashboard.sqlite3
```

## Public command surface

- `tiktok-research init-demo`
- `tiktok-research init-study`
- `tiktok-research import-legacy`
- `tiktok-research run-dashboard`
- `tiktok-research collect`
- `tiktok-research transcribe`
- `tiktok-research judge`
- `tiktok-research replace-sample`
- `tiktok-research export`

## Workspace layout

Every study workspace follows the same top-level layout:

- `inputs/`
- `data/`
- `exports/`
- `cache/`
- `logs/`
- `study_config.yaml`

The toolkit keeps the repo clean by design: workspaces hold user-specific state, while the repo holds code and public templates.

## Optional providers

The core dashboard and coding flow run without any paid APIs. Optional adapters can be enabled in `study_config.yaml`:

- `providers.tiktok` for TikTok Research API collection
- `providers.openai` for Whisper transcription and optional LLM judging
- `providers.anthropic` for optional LLM judging

Credentials are referenced by environment-variable name only. Secrets must never be committed to the repo.

## Docs

- [Quickstart](docs/quickstart.md)
- [Hosted deployment](docs/hosted-deployment.md)
- [Distribution and archival](docs/distribution.md)
- [Publish checklist](docs/publish-checklist.md)
- [Data policy](DATA_POLICY.md)
