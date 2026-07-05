# Host: gregor

> Status: **active** — interim inference + gateway host (2026-07-05).
> Predecessor name: `dev-rig-01` (inventoried 2026-07-02, hostname `TODO`).
> See `docs/ai/HISTORY.md` for the original `dev-rig-01` inventory text.

## Hardware specs

| Field | Value |
|---|---|
| Role | Interim inference + gateway host (ollama + LiteLLM); **not** a vLLM backend (8 GB VRAM too small for target models) |
| Hostname | gregor |
| CPU | Intel Xeon E3-1230 v6 @ 3.50 GHz (4 cores / 8 threads, Kaby Lake) |
| Motherboard | Gigabyte GR-X150-PRO ECC *(model unverified — TODO confirm)* |
| RAM | 15 GiB ECC |
| GPU | NVIDIA GeForce RTX 2070 SUPER, 8192 MiB GDDR6 (Turing, compute 7.5), driver 580.159.03 |
| GPU power sockets | 2x 8-pin |
| PSU | Corsair VX550W / CMPSU-550VX — 550 W, +12 V @ 41 A (~492 W) |
| PSU PCIe connectors | 1x (6+2)-pin + 1x 6-pin (see power-connector history below) |
| Storage | 246 GB root LV (`ubuntu-vg-ubuntu-lv`), 187 GB free (2026-07-05) |
| Network | enp0s31f6 (LAN, DHCP), tun0 (WireGuard) — IPs/MACs in `secrets.local.md` |
| OS / kernel | Ubuntu, kernel 7.0.0-27-generic |
| Added | 2026-07-02 (as dev-rig-01); renamed gregor 2026-07-05 |

## Runtime role (2026-07-05)

Single-GPU inference + STT gateway box, all stack config under `/opt/litellm/`.
**Live configs are backed up in `infra/litellm/` (this repo)** — see the README
there for the file map. Migration to management VM: `rsync -a /opt/litellm <vm>:`
+ `docker compose up -d`. `api_base` resolves to gregor's current WireGuard IP
from `secrets.local.md`.

| Service | Port | Bound by | Notes |
|---|---|---|---|
| ollama (backend) | `:11435` | host systemd (`OLLAMA_HOST=0.0.0.0:11435`) | `MAX_LOADED_MODELS=1`, `KEEP_ALIVE=-1`, `FLASH_ATTENTION=1`. **Known gap:** no ufw — directly reachable, bypasses LiteLLM auth (Issue #4). |
| LiteLLM (gateway) | `:11434` | Docker (published) | `ghcr.io/berriai/litellm:main-stable`; virtual keys, Postgres-backed (`db` service, internal). ufw cannot filter this port (Docker DOCKER chain). |
| models.dev merging-proxy | `:11436` | Docker (`python:3.12-alpine`) | injects `litellm` provider into upstream catalog; opencode `OPENCODE_MODELS_URL` points here. |
| Postgres 16 (LiteLLM DB) | internal | Docker (not published) | `db` service, bundled. LiteLLM `:main-stable` rejects SQLite (fatal). |
| Open WebUI | `:3000` | Docker (published) | `ghcr.io/open-webui/open-webui:main`; LDAP auth against `ldap.spengergasse.at:636`; STT via whisper-1 through LiteLLM. Mic requires HTTPS — pending (Caddy/nginx). |

### Custom LiteLLM plugin

`SingleGpuGuard` (`/opt/litellm/single_gpu_guard.py`) enforces single-model
residency on the one GPU: a different model requested while the resident
model is busy → HTTP 429 (busy model stays); same model → allowed (serialized
by ollama's `NUM_PARALLEL=1`); idle → atomic swap. Per-backend (`api_base`)
state, matched via `litellm_call_id`. **Self-healing (2026-07-05):** (1)
staleness reset — a leaked `in_flight` counter (lost callback on aborted
streams) self-heals after `_STALE_AFTER=660s` (reset+swap instead of 429);
(2) ollama `/api/ps` reconcile — the guard polls ollama's actually-loaded
model and adopts it when idle, correcting out-of-band loads (`ollama run`
on the host, `:11435` bypass). `api_base` is resolved from `config.yaml`
(pre_call has `litellm_params` still empty). Traces: `ACCEPT/SAME/SWAP/
REJECT/STALE-RESET/RECONCILE` in `/opt/litellm/data/guard.log`. See
`docs/ai/PITFALLS.md` for the implementation gotchas.

### Models (ollama, 2026-07-05)

**Live in ollama (2 tags, max-context-only):**
- `gemma4:e2b-128k` (e2b @ 128K = arch max, q4_K_M, 7.16 GB)
- `gemma4:e4b-128k` (e4b-it-qat @ 128K = arch max, Q4_0, 6.15 GB; sweet spot:
  ~6.35 GB VRAM, 1.4 GB KV headroom)

**Removed from ollama + inventoried (2026-07-05, Session 2):** the 5 4K-default
variants (`e2b`, `e4b`, `e4b-it-qat`, `12b`, `12b-it-qat`) were `ollama rm`'d
because they leaked into opencode's picker. Their 11 unique blobs (~22,6 GiB;
shared weight blobs survived via the kept `-128k` tags) + 5 manifests are in
**`/opt/litellm/blob-inventory/`** (NOT git; README + `tag-digest-map.json` with
restore steps). Restore at >8 GB HW (Issues #2/#5/#7): copy blobs+manifests back
to `~/.ollama/models/` + `systemctl restart ollama`. Sweet-spot context note:
e4b/e2b = 128K native; 256K is 12B+ only (see `docs/ai/DOMAIN.md`).

**Catalog flow (correction of an earlier wrong belief):** LiteLLM does NOT
auto-discover ollama tags. The catalog source-of-truth is `config.yaml`
`model_list` (the 2 entries above), loaded at LiteLLM startup. `/v1/models` is
**key-scoped** — it returns the requesting virtual key's `models` allowance, not
the router's. Both gregor keys (`opencode-gregor`, `catalog-proxy`) have
`models = '{}'` so they inherit the live proxy catalog; do NOT pin a model list
on them or the picker will go stale again (see `docs/ai/PITFALLS.md`).

**Add a model in future:** `ollama pull <tag>` → add `model_list` entry to
`/opt/litellm/config.yaml` → `docker compose restart litellm`. No key edit
needed while keys keep `models = '{}'`.

## Power-connector history (from dev-rig-01 inventory)

The card has two 8-pin sockets; the PSU provides one usable 8-pin
(the 6+2 lead) and one 6-pin — a shortfall of one 8-pin. Wattage is
ample (~310 W load vs. ~492 W on the 12 V rail); this is purely a
connector-shape mismatch.

**Fix (decided 2026-07-02):** 6-pin to 8-pin PCIe adapter on the PSU's
6-pin lead. Card socket 1 ← 6+2 lead; card socket 2 ← 6-pin + adapter;
each fed from its own cable.

**Adapter spec:** 1-to-1 PCIe 6-pin (female, PSU) to 8-pin (male, GPU),
18 AWG. Example: Cable Matters 2-pack (ASIN B01DV1Z32Y).

**Avoid:** any Y-splitter that fans a single PSU connector to both card
sockets (overload/fire risk). Avoid EPS/CPU 6-to-8 adapters (wrong
pinout — damages GPU).

**Open precheck:** physically confirm the two PSU PCIe leads are
separate cables, not a single daisy-chain, before final install.
*(Status TODO — see Issue #12.)*

## History

- **2026-07-02**: inventoried as `dev-rig-01`, hostname `TODO`, role
  "Dev / test / experiment rig (**not** a vLLM backend)". Power fix
  decided (6→8 pin adapter, no Y-splitter). Original spec text preserved
  in `docs/ai/HISTORY.md`.
- **2026-07-05**: box renamed **gregor** and repurposed as the interim
  inference + gateway host (ollama + LiteLLM + Postgres + models-proxy +
  SingleGpuGuard). Still not a vLLM backend (8 GB VRAM constraint
  unchanged). Management-VM migration tracked in Issue #3.