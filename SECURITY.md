# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.

## Data Encryption

The backend encrypts PHI fields such as `Memory.content` using a symmetric key.
Set the key with the `APP_ENCRYPTION_KEY` environment variable. The key must be
an URL-safe base64 string generated by `cryptography.Fernet.generate_key()`.
Rotate the key periodically and store it securely outside of source control
(e.g. in your deployment secrets manager).

## Secret Scanning

A Gitleaks workflow scans all pushes and pull requests for hardcoded secrets. Configure branch protection to require this check. Developers can run `python scripts/scan_for_secrets.py` locally before committing.

## Automated Security and Quality Checks

bekonOS uses a GitHub Actions workflow (`full-checks.yml`) that performs
comprehensive security and quality scans on every push and Pull Request:

- Gitleaks and repository history secret scanning
- Dependency vulnerability audits (`pnpm audit`, `pip-audit`)
- Static analysis (`bandit` and `npm audit`/SonarCloud)
- Dead code and duplicate detection
- Linting, formatting, and unit/integration tests
- Container image vulnerability scanning
- License compliance and changelog/version bump verification

All jobs must pass before code can be merged. The Codex Agent automatically
tries to fix any failing check and re-runs the workflow.

The workflow also validates all AGENTS files using `scripts/validate_agents.py`.
The Codex Agent must ensure every check succeeds before merging. If a check
fails, the agent will attempt to auto-correct issues (formatting, linting,
dependency updates) and rerun the workflow.

## License Compliance Policy

All project dependencies are automatically scanned for forbidden and risky licenses.
Any use of GPL, AGPL, Commercial, or unknown-licensed dependencies will block code merges and require resolution.
Last scan: 2025-07-15 — Status: PASS
See LICENSES-python.md and LICENSES-node.md for a current, full list.
