# Architecture

Living structural map of the system as of 2026-07-05.

## Overview

On-premise LLM-Infrastruktur für die Spengergasse. Aktuell (Übergang)
auf einem Single-GPU-Host **gregor** (RTX 2070 SUPER, 8 GB VRAM):
ollama als Inference-Backend, LiteLLM (Docker) als auth+Rate-Limit+Routing-Gateway,
ein Custom-LiteLLM-Plugin (**SingleGpuGuard**) erzwingt Single-Model-
Residency auf der einen GPU, und ein models.dev-Merging-Proxy speist
die Modellliste dynamisch in opencode ein. Langfristig zieht LiteLLM auf
die Management-VM (Issue #3) um; das gesamte Stack-Verzeichnis `/opt/litellm`
ist portabel (`rsync` + `docker compose up`), `api_base` zeigt immer auf
gregors WireGuard-IP `<WG_IP_GREGOR>` (siehe `infra/hosts/secrets.local.md`; temporär/DHCP — migriert ohne Config-Edit, da kompose/LiteLLM bei gleichem Hostnamen bleibt).

## Why LiteLLM?

Auf gregor (Single-GPU Dev-Box) ist LiteLLM streng genommen Overhead —
Open WebUI könnte direkt auf ollama zugreifen. Zwei Gründe rechtfertigen
den Proxy heute:

1. **SingleGpuGuard** — erzwingt Single-Model-Residency auf der 8 GB GPU.
   Ohne den Guard könnten whisper + LLM gleichzeitig laden → OOM. Das ist
   der Killer-Faktor für die aktuelle Hardware.
2. **models.dev-Proxy** — speist die LiteLLM-Modelle in den opencode-Picker
   ein (`OPENCODE_MODELS_URL`). Ohne LiteLLM kein opencode-Discovery.

Für die Produktions-Deployment (2600 Schüler, mehrere Backends) wird
LiteLLM unverzichtbar: Virtual Keys + Budgets (Issue #6), Rate Limiting,
Multi-Backend-Routing, Audit Logging, Model-Access-Groups.

Ohne LiteLLM: Ollama → Open WebUI (1 Hop, einfacher).
Mit LiteLLM: Ollama → LiteLLM → Open WebUI (3 Hops, aber Guard + Auth + Routing).

```
                  ┌─────────────────────────────────────────────┐
   Clients        │  opencode (TUI) / Open WebUI / API-Clients   │
   (Schulnetz     │  OPENCODE_MODELS_URL=<WG_IP_GREGOR>:11436     │
    + VPN)        └──────────────────┬──────────────────────────┘
                                          │  :11434  Bearer <virtual-key>
         ┌────────────────────────────────┴───────────────────────────┐
         │  gregor (<WG_IP_GREGOR>)                                      │
         │                                                              │
         │  ┌─────────────────┐  /v1/chat/completions  ┌──────────────┐ │
         │  │ LiteLLM :11434  │ ───────────────────►  │ ollama :11435│ │
         │  │ + Postgres 16   │   SingleGpuGuard:      │ MAX_LOADED=  │ │
         │  │ + catalog-proxy │   busy→429/ idle→swap   │ 1            │ │
         │  │   Key :11436    │                        │ KEEP_ALIVE=  │ │
         │  │ + Open WebUI    │                        │ -1           │ │
         │  │   :3000         │                        └──────────────┘ │
         │  │ + whisper :11437│                                         │
         │  └────────▲────────┘                                         │
         │           │ /v1/models                                       │
         │           └──────► models-proxy injiziert litellm-Provider   │
         │                    in upstream models.dev-Katalog           │
         └──────────────────────────────────────────────────────────────┘
```

## Komponenten auf gregor (`/opt/litellm/`)

| Datei/Dienst | Zweck |
|---|---|
| `compose.yaml` | docker-compose: services litellm + db (Postgres 16) + models-proxy + open-webui + whisper |
| `config.yaml` | LiteLLM Framework-Settings (callbacks, request_timeout, master_key/db_url via env). `model_list` leer — Modelle in Postgres DB (`store_model_in_db=true`) |
| `single_gpu_guard.py` | Custom CustomLogger-Plugin: per-backend (api_base) Single-Residency-Regel, litellm_call_id-Matching |
| `models_proxy.py` | HTTP-Server :8000: GET /api.json = upstream models.dev + litellm-Provider (Modelle aus LiteLLM /v1/models); UA-Fix wg. Cloudflare 403 |
| `open-webui-data/` | Open WebUI SQLite DB (`webui.db`), vector_db, uploads, cache |
| `.env` | LITELLM_MASTER_KEY / SALT_KEY / POSTGRES_PASSWORD / DATABASE_URL / LITELLM_PROXY_KEY / LITELLM_PUBLIC_URL |
| `pgdata/` | bind-mount Postgres-Daten (portabel) |
| `data/` | LiteLLM guard.log etc. |
| `cache/` | Proxy-Disk-Cache (upstream.json / merged.json / litellm_models.json) — Resilienz bei Proxy/Upstream-Ausfall |
| `Modelfile.qwen3-1.7b` | Tuned Modelfile: qwen3:1.7b, 24K ctx, konservative Params, "Do NOT use tools" system prompt |
| `Modelfile.qwen2.5-coder-3b` | Tuned Modelfile: qwen2.5-coder:3b, 24K ctx, "Do NOT use tools" |
| `Modelfile.llama3.2-3b` | Tuned Modelfile: llama3.2:3b, 24K ctx, "Do NOT use tools" |
| `ollama.service` | systemd unit: `OLLAMA_KV_CACHE_TYPE=q8_0`, `MAX_LOADED_MODELS=1`, `KEEP_ALIVE=-1`, `FLASH_ATTENTION=1` |

## Directory-Struktur (Repository)

```
llm-on-premise/
├── docs/ai/              # Wissensbasis (siehe Tabelle unten)
├── docs/praesentation/   # Eröffnungskonferenz-Slides + ZID-Archiv
├── docs/extern/          # externes Kursangebot etc.
├── infra/hosts/          # <hostname>.md per host (gregor.md) + secrets.local.md (git-ignored)
└── .github/workflows/    # GitHub Pages deploy
```

## Knowledge Files (`docs/ai/`)

| File | Purpose | Update mode |
|------|---------|-------------|
| HANDOFF.md | Offene Aufgaben für nächste Sitzung | Overwrite |
| DECISIONS.md | Aktive Entscheidungen | Append; superseded → HISTORY.md |
| ARCHITECTURE.md | Living structural map | Overwrite |
| CONVENTIONS.md | Laufende Regeln zur Befolgung | Append |
| PITFALLS.md | Fallstricke und nicht-offensichtliche Fehler | Append |
| DOMAIN.md | Domänenregeln (Schule + Modell-Spezifika) | Append |
| STATE.md | Aktueller Projektstatus | Overwrite |
| HISTORY.md | Archiv superseded Einträge (append-only) | Append-only |

## Data Flows

- Schüler/Lehrer → opencode-Picker → `litellm/qwen3:1.7b` (etc.) → LiteLLM `:11434` (Bearer virtual-key) → SingleGpuGuard (busy→429 / idle→swap) → ollama `:11435` → GPU.
- Open WebUI → LiteLLM `:11434` (Bearer virtual-key) → SingleGpuGuard → ollama `:11435` → GPU. STT via whisper `:11437`.
- opencode model-discovery: Client `GET http://<WG_IP_GREGOR>:11436/api.json` (OPENCODE_MODELS_URL; IP aus `infra/hosts/secrets.local.md`) → models-proxy merged upstream models.dev + `litellm`-Provider (Modelle aus `GET :11434/v1/models`) → Picker; Refresh alle ~60 min.
- Neues Modell: `ollama pull`/`create` + Eintrag in LiteLLM DB (`LiteLLM_ProxyModelTable` via UI oder SQL, `store_model_in_db=true`) + Open WebUI `model` table (`base_model_id = NULL`!) → automatisch im Katalog. `config.yaml` `model_list` bleibt leer.
- Migration auf Management-VM (Issue #3): `rsync -a /opt/litellm <vm>:` + `docker compose up -d`; `api_base` bleibt `http://<WG_IP_GREGOR>:11435` (IP aus `infra/hosts/secrets.local.md`), `OPENCODE_MODELS_URL` bleibt `:11436` (gregor), erreichbar über WireGuard.

## Known Gaps (siehe PITFALLS.md / DECISIONS.md)

- Kein ufw: `:11435` (ollama) direkt erreichbar → Bypass um LiteLLM-Auth möglich (Issue #4).
- `OPENCODE_MODELS_URL` aktuell nur in georgs `~/.bash_aliases` — Schüler noch nicht versorgt.