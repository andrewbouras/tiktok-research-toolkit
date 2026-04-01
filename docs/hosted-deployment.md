# Hosted Deployment

The first-class supported mode is local-first. Hosted deployment is optional and should be treated as an operational layer on top of a working local workspace.

## Recommended hosted approach

- Run the same packaged app inside a managed VM or container
- Mount a persistent workspace volume outside the image
- Keep credentials in environment variables, not in `study_config.yaml`
- Back up the workspace directory, not the repo clone

## Not the default

Machine-specific sharing tools such as Tailscale can still be used, but they are intentionally not the primary setup path for public adopters.

