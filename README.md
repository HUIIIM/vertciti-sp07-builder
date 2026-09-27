[![CI](https://github.com/HUIIIM/vertciti-sp07-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/HUIIIM/vertciti-sp07-builder/actions/workflows/ci.yml)
[![Secret scan](https://github.com/HUIIIM/vertciti-sp07-builder/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/HUIIIM/vertciti-sp07-builder/actions/workflows/gitleaks.yml)

# vertciti-sp07-builder

Build tooling for the vertciti **SP-07** product page. SP-07 is the AI phone
receptionist (AI 电话接待员) offering, currently in first-order trial /
application-only mode.

## What's here

- `build-sp07-prod.py` — builds the SP-07 production `index.html` from a
  D111-safe base HTML file. Applies the v1.1 logo syntax normalization plus
  the SP-07 content edits, and fails loudly if any anchor is not found
  exactly once (no silent partial builds).
- `machine/` — machine-readable product data consumed by the builder:
  `catalog.json`, `categories.json`, `manifest.json`, `ratings.json`.

## Usage

```bash
python3 build-sp07-prod.py --src /path/to/base.html --dst-dir /path/to/out
```

Run `python3 build-sp07-prod.py --help` for all options.

## Status

Internal build tooling. The SP-07 offer itself is in first-order trial mode;
it is not presented here as generally available.

## CI / security

- GitHub Actions CI runs on push and PR (`.github/workflows/ci.yml`).
- Secret scanning (gitleaks) runs on push, PR, and on a schedule.
- See [.github/SECURITY.md](.github/SECURITY.md) and
  [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md).
