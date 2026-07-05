# CONVENTIONS — llm-on-premise

## Sprache
- README und README-sichtbare Dokumentation: Deutsch
- Code, Konfiguration, Issues, AGENTS.md: Englisch
- docs/ai/ knowledge files: Deutsch

## Kommunikation
- Issues in Englisch (für GitHub-Community)
- Schulintern Deutsch

## Git
- Jeder Commit referenziert ein Issue (#N)
- issue-workflow Skill verwenden
- trunk-based development (main)

## LLM-Stack (gregor — `/opt/litellm/`)
- Containers-Konfiguration lebt unter `/opt/litellm/` (`compose.yaml`, `config.yaml`, `single_gpu_guard.py`, `models_proxy.py`, `.env`, `pgdata/`, `data/`, `cache/`). Migration auf die Management-VM = `rsync -a /opt/litellm <vm>:` + `docker compose up -d` — keine Config-Edits nötig.
- `api_base` in LiteLLM `config.yaml` IMMER als gregors WireGuard-IP `http://10.8.0.18:11435` angeben (migriert ohne Edit), nie `127.0.0.1`.
- Secrets (Master/Salt/Proxy/Opencode-Keys, Postgres-PW) in `/opt/litellm/.env` — niemals committen.
- opencode.json `provider`-Eintrag für kataloggestützte Provider: nur `{ "options": { "baseURL", "apiKey" } }` — KEIN `models`/`npm`/`name` (der models.dev-Katalog liefert beides). Discovery-Source = `OPENCODE_MODELS_URL=http://10.8.0.18:11436` in `~/.bash_aliases` (später shared).
- Neues Modell anlegen: `ollama pull`/`create` + Eintrag in `/opt/litellm/config.yaml` `model_list` + `docker compose restart litellm`. Der models-Proxy übernimmt es beim nächsten Refresh (~60 min) automatisch in den opencode-Picker.
- Kontextoverride: dafür einen eigenen ollama-Tag (`ollama create <name>-128k -f Modelfile` mit `PARAMETER num_ctx`) + LiteLLM-Eintrag anlegen. Nicht denselben ollama-Manifest zweimal in LiteLLM listen — `/v1/models` dedupliziert (Alias-Tags sind verwirrend).
- Single-GPU-Residency-Regel wird client-agnostisch in LiteLLM (SingleGpuGuard) durchgesetzt, nicht pro Client. Clients kricken bei Konflikt ein 429 (Retry-After 5).
