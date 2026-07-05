# History

Chronological archive of superseded decisions and pruned entries.
Entries here are no longer active truth. Never delete from this file.

## 2026-07-05 (Knowledge-Persistence Run)
- Initial creation of `HISTORY.md`. No entries were relocated from active files this session — all persisted knowledge was net-new (LiteLLM/Postgres/SingleGpuGuard/models-proxy stack on gregor). The prior `STATE.md` focus (Eröffnungskonferenz-Präsentation, ZID-Pitch) is **not** superseded and was carried forward into the new `STATE.md` "Completed" list.
- **Origin**: knowledge-persistence skill run by session 2026-07-05.
- **Reason**: file creation; no prune happened.

## 2026-07-05 (SUPERSEDED 2026-07-05, origin: infra/hosts/inventory.md, reason: box renamed dev-rig-01 → gregor + repurposed): dev-rig-01 inventory
- Full original text of `infra/hosts/inventory.md` (deleted 2026-07-05; merged into `infra/hosts/gregor.md`):
  ```
  Role: Dev / test / experiment rig (not a vLLM backend)
  Hostname: TODO
  CPU: TODO
  RAM: TODO
  GPU: NVIDIA RTX 2070, 8 GB GDDR6 (Turing, 2018)   [note: actually RTX 2070 SUPER]
  GPU power sockets: 2x 8-pin
  Motherboard: Gigabyte GR-X150-PRO ECC (model unverified)
  PSU: Corsair VX550W / CMPSU-550VX — 550 W, +12 V @ 41 A (~492 W)
  PSU PCIe connectors: 1x (6+2)-pin + 1x 6-pin
  Storage: TODO / Network: TODO / Added: 2026-07-02
  Power fix (decided 2026-07-02): 6-pin → 8-pin PCIe adapter; no Y-splitter; no EPS adapter.
  Open precheck: confirm two PSU PCIe leads are separate cables, not daisy-chain.
  Role rationale: 8 GB cannot run GLM-5.2/DeepSeek V4/Qwen 3.6 at usable precision.
  ```
- **Origin**: `infra/hosts/inventory.md` (single-section file).
- **Reason**: the box was renamed `gregor` and repurposed as the interim inference+gateway host on 2026-07-05. Per-host files (`infra/hosts/gregor.md`) now replace the single `inventory.md`; the dev-rig-01 era is summarised in gregor.md's "History" subsection.

## 2026-07-05 (REDACTION RUN)
- Scrubbed gregor's raw WireGuard IP and Docker/LAN IPs from all `docs/ai/*` files; replaced with the placeholder `<WG_IP_GREGOR>` + a pointer to `infra/hosts/secrets.local.md` (git-ignored). Both IPs are temporary/DHCP and belong only in `secrets.local.md`. Port numbers (`:11434/:11435/:11436`) kept (operationally essential, harmless without the IP). No credentials were ever committed.
- **Note**: the prior commit `124ebed` (2026-07-05, knowledge-persistence run) contains the raw IP in git history. Forward-only redaction chosen (RFC1918, VPN-only, no creds) — the IP remains in that one historical commit; no force-push performed.