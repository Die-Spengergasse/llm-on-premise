# Open WebUI — Chat Frontend

Open WebUI läuft als Docker-Container auf gregor und ist das
user-facing Chat-Interface für Schüler und Lehrer.

## Service

| Eigenschaft | Wert |
|-------------|------|
| Container | `open-webui` (Docker, `ghcr.io/open-webui/open-webui:main` v0.10.2) |
| Port | `:3000` (→ Container `:8080`) |
| Auth | LDAP gegen `ldap.spengergasse.at:636` (Schul-AD) |
| Backend | LiteLLM `:11434` (OpenAI-compatible) |
| STT | Aktuell lokal (whisper `:11437`); geplant: Groq Cloud |
| DB | SQLite: `/opt/litellm/open-webui-data/webui.db` |

## Modellauswahl

Open WebUI zeigt alle Modelle aus LiteLLM `/v1/models`. Aktuell:

| Modell | Quelle | Zweck |
|--------|--------|-------|
| `qwen3:1.7b` | lokal (ollama via LiteLLM) | General Chat |
| `qwen2.5-coder:3b` | lokal | Coding |
| `llama3.2:3b` | lokal | General Chat (Alternative) |
| `whisper-1` | lokal (whisper via LiteLLM) | STT (Speech-to-Text) |

**Geplant:** Cloud-Modelle (OpenCode Zen Big Pickle, Groq Llama 70B, DeepSeek)

## Model-Capabilities konfigurieren

**Kritisch:** Siehe `docs/ai/TIPS.md` für die vollständige Erklärung.

### Pro Modell erforderlich (in Open WebUI SQLite DB):

**1. `base_model_id = NULL` (nicht `''`!)**

```sql
-- Prüfen
SELECT id, base_model_id FROM model;
-- Fixen
UPDATE model SET base_model_id = NULL WHERE base_model_id = '';
```

Ohne `NULL` werden alle Capabilities/Params **silently ignored**.

**2. Params (`model.params` JSON):**

```json
{
  "function_calling": "none",
  "tool_choice": "none",
  "max_tokens": 58579
}
```

Für Qwen3 zusätzlich: `"reasoning_tags": false, "think": false`

**3. Capabilities (`model.meta.capabilities`):**

```json
{
  "builtin_tools": false,
  "web_search": false,
  "code_interpreter": false,
  "terminal": false,
  "image_generation": false,
  "citations": true,
  "vision": true,
  "file_upload": true
}
```

### DB direkt bearbeiten

```bash
sudo python3 -c "
import sqlite3, json
db = sqlite3.connect('/opt/litellm/open-webui-data/webui.db')
# ... queries and updates ...
db.close()
"
```

## Web Search / RAG

**Status:** Nicht funktional mit aktuellen kleinen Modellen.

Open WebUI v0.10.2 implementiert Web Search als **native Function Call**,
nicht als automatische Context-Injection. Kleine Modelle (1.7B-3B) können
das `web_search`-Tool nicht zuverlässig aufrufen.

Mit `function_calling: "none"` (unser aktueller Fix) ist Web Search
komplett deaktiviert.

**SearXNG** ist verfügbar unter `https://searxng.claw.graf.priv.at` —
bereit für Nutzung sobald ein größeres Modell (7B+) läuft.

## Audio / STT

Aktuelle Konfiguration (Admin Panel → Settings → Audio):
- STT Engine: `openai`
- API Base: `http://litellm:11434/v1` (via LiteLLM zu lokalem whisper)
- Model: `whisper-1`

**Geplant:** Migration zu Groq Cloud (`https://api.groq.com/openai/v1`)
um 3.9 GB VRAM freizugeben für ein lokales 7B-Modell.

## LDAP-Auth

```
Server: ldap.spengergasse.at:636 (LDAPS)
Search Filter: (sAMAccountName={{login}})
Base DN: OU=Automatisch gewartete Benutzer,OU=Benutzer,OU=SPG,DC=htl-wien5,DC=schule
```

Erst-Login via Schul-AD = Admin.

## HTTPS

**Offen (Issue #14):** Mic-Zugriff benötigt Secure Context (HTTPS).
Caddy oder nginx als Reverse Proxy vor `:3000` geplant.
