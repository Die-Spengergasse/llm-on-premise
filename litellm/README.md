# LiteLLM — API Gateway & Proxy

LiteLLM läuft als Docker-Container auf gregor und fungiert als zentraler
Gateway zwischen Clients (Open WebUI, opencode) und Backends (ollama, whisper,
cloud APIs).

## Warum LiteLLM?

Auf gregor (Single-GPU) ist LiteLLM streng genommen Overhead — Open WebUI
könnte direkt auf ollama zugreifen. Zwei Gründe rechtfertigen den Proxy:

1. **SingleGpuGuard** — erzwingt Single-Model-Residency auf der 8 GB GPU.
   Ohne den Guard könnten whisper + LLM gleichzeitig laden → OOM.
2. **models.dev-Proxy** — speist die LiteLLM-Modelle in den opencode-Picker ein.

Für die Produktion (2600 Schüler) wird LiteLLM unverzichtbar:
Virtual Keys + Budgets, Rate Limiting, Multi-Backend-Routing, Audit Logging.

## Service

| Eigenschaft | Wert |
|-------------|------|
| Container | `litellm` (Docker, `ghcr.io/berriai/litellm:main-stable` v1.91.0) |
| Port | `:11434` |
| Config | `config.yaml` (Framework-Settings, `model_list` leer) |
| DB-Mode | `store_model_in_db=true` — Modelle in Postgres `LiteLLM_ProxyModelTable` |
| Postgres | `litellm-db` Container, Port intern |
| Compose | `compose.yaml` (enthält auch open-webui, whisper, models-proxy) |

## Architektur

```
Clients (Open WebUI, opencode)
    │ Bearer <virtual-key>
    ▼
LiteLLM :11434 ──► SingleGpuGuard (busy→429 / idle→swap)
    │
    ├──► ollama :11435 (LLM-Modelle)
    ├──► whisper :11437 (STT)
    └──► [geplant: Groq, DeepSeek, OpenCode Zen]
```

## Config-Dateien

| Datei | Zweck |
|-------|-------|
| `config.yaml` | Framework-Settings: callbacks, request_timeout, master_key/db_url. `model_list` ist leer (DB-Mode). |
| `compose.yaml` | Docker-Compose mit allen Services: litellm, db, models-proxy, open-webui, whisper |
| `single_gpu_guard.py` | Custom Plugin: Single-GPU-Residency-Regel |
| `models_proxy.py` | HTTP-Server :11436: merged models.dev + LiteLLM-Katalog für opencode |
| `.env.example` | Template für `/opt/litellm/.env` (Master-Key, Salt, Postgres-PW, etc.) |

## Modelle verwalten (DB-Mode)

**Neues Modell hinzufügen:**

1. `ollama pull <tag>` oder `ollama create <tag> -f Modelfile`
2. In LiteLLM Postgres eintragen:
   ```sql
   INSERT INTO "LiteLLM_ProxyModelTable"
     (model_id, model_name, litellm_params, model_info, created_by, updated_by)
   VALUES (
     '<unique-id>', '<tag>',
     '{"model": "ollama/<tag>", "api_base": "http://10.8.0.18:11435", "num_retries": 0}',
     '{"supports_function_calling": false}',
     'admin', 'admin'
   );
   ```
3. `docker compose restart litellm`
4. In Open WebUI DB eintragen (siehe `/openwebui/README.md`)

**Modell entfernen:**
```sql
DELETE FROM "LiteLLM_ProxyModelTable" WHERE model_name = '<tag>';
```

## Keys

| Key | Zweck | Wo |
|-----|-------|----|
| Master Key | Admin-Zugriff (API, DB) | `/opt/litellm/.env` → `LITELLM_MASTER_KEY` |
| opencode-gregor | Virtual Key für opencode | LiteLLM Postgres (via `/key/list`) |
| catalog-proxy | Virtual Key für models-proxy | `/opt/litellm/.env` → `LITELLM_PROXY_KEY` |
| Open WebUI | Virtual Key für Open WebUI | Open WebUI DB (`config` table) |

**WICHTIG:** Token/Auth-Konzept für die Schul-Deployment ist ungeklärt.
Siehe GitHub Issue (Token-Konzept).

## SingleGpuGuard

Das Custom-Plugin (`single_gpu_guard.py`) implementiert:
- Single-Model-Residency auf der 8 GB GPU
- `busy→429` (Retry-After 5s), `same model→ACCEPT`, `idle→atomic swap`
- Staleness-Self-Heal (geleakter Counter nach 660s)
- ollama `/api/ps` Reconcile (Out-of-band-Load-Korrektur)
- Traces: `ACCEPT`/`SAME`/`SWAP`/`REJECT`/`STALE-RESET`/`RECONCILE`

Guard-Log: `/opt/litellm/data/guard.log` (append-only, bind-mounted)

## Nützliche Kommandos

```bash
# Modelle auflisten
MASTER_KEY=$(grep LITELLM_MASTER_KEY /opt/litellm/.env | cut -d= -f2)
curl -s -H "Authorization: Bearer $MASTER_KEY" http://localhost:11434/v1/models | jq '.data[].id'

# Guard-Log
tail -f /opt/litellm/data/guard.log

# LiteLLM neustarten
sudo docker compose -f /opt/litellm/compose.yaml restart litellm

# DB direkt abfragen
sudo docker exec litellm-db psql -U litellm -c 'SELECT model_name FROM "LiteLLM_ProxyModelTable"'
```
