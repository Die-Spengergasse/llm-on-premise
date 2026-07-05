# Host Inventory

This directory records concrete hosts for the llm-on-premise stack.

| File | Purpose | Tracked? |
|---|---|---|
| `<hostname>.md` | Hardware specs + runtime role for one host (e.g. `gregor.md`) | yes |
| `README.md` | This file | yes |
| `secrets.local.md` | IPs, MACs, credentials, pointers to on-host secret stores | **no** (git-ignored) |

## Conventions

- **One file per host**, named by hostname (`gregor.md`, …). Specs are
  non-sensitive and version-controlled.
- Anything sensitive (IPs, MACs, keys, passwords) goes in
  `secrets.local.md`, which is listed in `.gitignore` and is never
  committed. IPs here are often DHCP/temporary — reference hosts by name
  in docs and resolve the current IP from `secrets.local.md` at task time.
- Language: English (matches the `infra/` = code/config convention).
- Mark unknowns as `TODO` rather than guessing.
- Record each host's role decision in `docs/ai/DECISIONS.md`.
- When a host is renamed or repurposed, move the superseded spec text to
  `docs/ai/HISTORY.md` and leave a one-line "history" subsection in the
  host file.

## Adding a host

1. Create `infra/hosts/<hostname>.md` with hardware specs and runtime role.
2. Add secrets (current IPs, MACs, key locations) to `secrets.local.md`.
3. Record the role decision in `docs/ai/DECISIONS.md`.
4. Commit via the `issue-workflow` skill, referencing the issue number.