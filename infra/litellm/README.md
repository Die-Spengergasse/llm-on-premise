# LiteLLM Stack — gregor

Live config files for the gregor inference + STT host.
These files are version-controlled here; the live copies are at `/opt/litellm/`.

## Contents

| File | Live path | Purpose |
|---|---|---|
| `config.yaml` | `/opt/litellm/config.yaml` | LiteLLM model_list + plugins |
| `compose.yaml` | `/opt/litellm/compose.yaml` | Docker Compose (litellm, db, models-proxy, whisper) |
| `single_gpu_guard.py` | `/opt/litellm/single_gpu_guard.py` | LiteLLM callback for single-GPU model residency |
| `models_proxy.py` | `/opt/litellm/models_proxy.py` | Merging proxy for models.dev catalog (port :11436) |
| `.env.example` | — | Template; copy to `.env` and fill secrets |
| `.env` | `/opt/litellm/.env` | **Not tracked** (secrets: DB pw, API keys) |
| `opencode.json.example` | — | Template for client config |
| `opencode-env.sh` | — | Shell snippet for `OPENCODE_MODELS_URL` |
| `whisper-data/` | `/opt/litellm/whisper-data/` | **Not tracked** (model cache + API key) |
| `cache/` | `/opt/litellm/cache/` | **Not tracked** (models-proxy disk cache) |

## Blob inventory

5 removed ollama tags' unique blobs (~22.6 GiB) are at `/opt/litellm/blob-inventory/`
(not in git). See `infra/hosts/gregor.md` for restore instructions.

## Host info

See `infra/hosts/gregor.md` for hardware specs, runtime roles, and model details.
