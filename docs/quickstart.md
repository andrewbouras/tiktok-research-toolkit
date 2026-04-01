# Quickstart

## 1. Install

Preferred for contributors:

```bash
uv sync --extra dashboard --extra dev
```

Fallback:

```bash
python3 -m pip install -e ".[dashboard,dev]"
```

## 2. Create a demo workspace

```bash
tiktok-research init-demo /tmp/tiktok-demo
tiktok-research run-dashboard /tmp/tiktok-demo
```

## 3. Create a real study workspace

```bash
tiktok-research init-study /tmp/my-study --study-name "My Study"
```

Then either import your legacy files or populate the workbook and metadata JSON in the workspace `inputs/` directory.

