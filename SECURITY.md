# Security Policy

## Supported versions

The latest tagged release and the default branch are supported for security fixes.

## Reporting a vulnerability

Please do not open public issues for suspected secrets exposure, unsafe defaults, or data leakage paths. Report privately to the project maintainers and include:

- a short description of the issue
- reproduction steps
- affected command, workflow, or file
- whether the issue can expose private study data or credentials

## Secure-by-default expectations

- Credentials are referenced by environment-variable name only.
- The publish check blocks obvious secrets and non-public artifact types.
- Demo data must remain synthetic.

