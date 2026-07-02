# Host Inventory

This directory records concrete hosts for the llm-on-premise stack.

| File | Purpose | Tracked? |
|---|---|---|
| `inventory.md` | Hardware specs per host (role, CPU, RAM, GPU, PSU, power notes) | yes |
| `README.md` | This file | yes |
| `secrets.local.md` | IPs, MACs, credentials | **no** (git-ignored) |

## Conventions

- Specs are non-sensitive: keep them in `inventory.md` (version-controlled).
- Anything sensitive goes in `secrets.local.md`, which is listed in
  `.gitignore` and is never committed.
- Language: English (matches the `infra/` = code/config convention).
- One section per host, ordered by addition date; mark unknowns as `TODO`
  rather than guessing.
- Record each host's role decision in `docs/ai/DECISIONS.md`.

## Adding a host

1. Append a block to `inventory.md`.
2. Add secrets (if any) to `secrets.local.md`.
3. Record the role decision in `docs/ai/DECISIONS.md`.
4. Commit via the `issue-workflow` skill, referencing the issue number.
