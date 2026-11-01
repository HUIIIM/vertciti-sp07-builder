# vertciti-sp07-builder

SP07 builder tooling. Public repository, proprietary license: all rights
reserved, Copyright (c) 2026 VERTCITY LLC. "Public" means visible as a
showcase surface; it does not grant code-reuse rights.

## How work happens here

- Direction arrives in-repo: GitHub Issues labeled `jarvis-task`, PR
  review comments, and `CLAUDE.md` / `LOOP.md`. Read both at session start.
- External Claude works on `claude/*` branches and opens PRs; it never
  merges its own PRs. Jarvis reviews and merges.
- Review verdicts exist only as PR comments.

## Working rules

- All GitHub Actions references are pinned to commit SHAs in this repo.
- The license text is the ruling-set proprietary text; do not replace it
  with an open-source license.
