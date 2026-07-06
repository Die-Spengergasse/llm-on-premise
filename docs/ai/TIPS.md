# TIPS — llm-on-premise

Tips & Tricks for Open WebUI administration, database operations, and
known configuration patterns. Additive knowledge — read before digging
into a new Open WebUI issue.

## Open WebUI Database

### Location
- **Host path:** `/opt/litellm/open-webui-data/webui.db` (SQLite)
- **Container path:** `/app/backend/data/webui.db`

### Access via Python (sudo needed, file is root-owned)
```python
sudo python3 -c "
import sqlite3, json
db = sqlite3.connect('/opt/litellm/open-webui-data/webui.db')
# ... queries ...
db.close()
"
```

### Key Tables

#### `model` — one row per model in the catalog
Columns: `id` (model ID), `params` (JSON), `meta` (JSON), `base_model_id`, `name`, ...

```python
row = db.execute('SELECT params, meta FROM model WHERE id=?', ('qwen3:4b',)).fetchone()
params = json.loads(row[0])  # {"tool_choice": "none", "reasoning_tags": false, ...}
meta = json.loads(row[1])    # {"capabilities": {...}, "profile_image_url": "...", ...}
```

#### `config` — all Open WebUI settings (key-value)
Columns: `key` (str), `value` (JSON string), `updated_at`

```python
rows = db.execute('SELECT key, value FROM config').fetchall()
```

Keys matching `web.search.*` control web search. Keys matching `rag.*` control RAG pipeline.

### Access from Docker (alternative)
```bash
docker exec open-webui sqlite3 /app/backend/data/webui.db "SELECT ..."
```
(Only works if the container has `sqlite3` installed.)

## Model Capabilities (meta.capabilities)

Edit the `meta` JSON column on the `model` table:

```python
meta = json.loads(row[1])
meta['capabilities']['web_search'] = True         # show/hide globe icon
meta['capabilities']['builtin_tools'] = False      # internal tools (write_note, etc.)
meta['capabilities']['code_interpreter'] = False
meta['capabilities']['terminal'] = False
meta['capabilities']['image_generation'] = False
meta['capabilities']['citations'] = True
meta['capabilities']['vision'] = True
meta['capabilities']['file_upload'] = True
db.execute('UPDATE model SET meta=? WHERE id=?', (json.dumps(meta), 'qwen3:4b'))
db.commit()
```

Changes take effect after restarting the container:
```bash
sudo docker compose -f /opt/litellm/compose.yaml restart open-webui
```

## Model Parameters (params)

Edit the `params` JSON column on the `model` table:

```python
params = json.loads(row[0])
params['tool_choice'] = 'none'              # prevent model from calling ANY tool
params['function_calling'] = 'none'         # tell Open WebUI the model cannot do FC
params['function_calling'] = 'native'       # enable native FC (let model call tools)
params['reasoning_tags'] = False            # hide thinking/section tags
params['think'] = False                     # disable Qwen3 thinking blocks
params['max_tokens'] = 58579                # token limit
db.execute('UPDATE model SET params=? WHERE id=?', (json.dumps(params), 'qwen3:4b'))
db.commit()
```

### Common param presets

**Locked-down mode (text only, no tools, no thinking):**
```json
{"function_calling": "none", "tool_choice": "none", "reasoning_tags": false, "max_tokens": 58579, "think": false}
```

**FC enabled, only web_search available:**
```json
{"function_calling": "native", "max_tokens": 58579}
```
(Also requires `capabilities.web_search=true`, `capabilities.builtin_tools=false`)

**Legacy FC mode (prompt injection instead of native template):**
```json
{"function_calling": "legacy", "max_tokens": 58579}
```
(Deprecated since v0.10.0, no new features/fixes — but useful for models that hallucinate with native FC)

## Web Search Configuration (config table)

Key config values (set via compose.yaml env OR Admin Panel; ConfigVars persist in DB):

| DB key | Meaning |
|--------|---------|
| `web.search.enable` | Enable web search |
| `web.search.engine` | `"searxng"`, `"google_pse"`, etc. |
| `web.search.searxng_query_url` | `"https://searxng.claw.graf.priv.at/search?q=<query>"` |
| `web.search.result_count` | Results to fetch (default 3) |
| `web.search.concurrent_requests` | Parallel search requests (0=unlimited) |
| `web.search.confirmation.enable` | Show "Search the web?" dialog before each search |
| `web.search.bypass_embedding_and_retrieval` | Skip embedding, use raw snippets |
| `web.search.bypass_web_loader` | Don't scrape result pages, use only snippets |
| `web.loader.engine` | Content extraction engine (empty=default, `playwright`, etc.) |
| `web.loader.ssl_verification` | SSL verify for page fetches (set `false` for self-signed) |

Quick-check via:
```python
rows = db.execute("SELECT key, value FROM config WHERE key LIKE 'web.search.%'").fetchall()
```

### ConfigVar caveat
Web search and many other settings are `ConfigVar` — once saved in the DB (Admin UI
or first startup), the DB value takes **permanent precedence** over compose.yaml env
vars on subsequent restarts. To force env vars:
1. Set `ENABLE_PERSISTENT_CONFIG: "false"` in compose.yaml temporarily
2. Or update directly in the DB (see above)
3. Or set via Admin Panel (which writes to DB)

## Tool-Call Problems — Root Causes & Fixes

### The `function_calling` parameter is the real lever (not `builtin_tools`)

Open WebUI v0.10.0+ defaults `function_calling` to **`native`**. This sends
the function-calling signal to the model via the Ollama chat template — even
when `builtin_tools: false` and no tools are registered. The model sees the
"you can call functions" instruction and hallucinates tool-call JSON like
`{"name": "write_poem", "arguments": {"content": "..."}}`.

The three modes:
- **`native`** (default since v0.10.0) — uses the model's native tool-calling
  template. Small models hallucinate tool calls even without registered tools.
- **`legacy`** — uses prompt injection instead of native template. Deprecated,
  still works, no new features/fixes.
- **`none`** — disables function calling entirely. No tool-calling signal sent.

**Setting `function_calling: "none"` in model params is the primary fix.**
This stops Open WebUI from signaling the model that it can call functions.

(Source: Open WebUI maintainer Classic298, issue #26823)

### THE Root Cause for SQL-inserted models: `base_model_id` must be NULL

**This is the #1 gotcha.** When inserting model entries into the Open WebUI
`model` table via SQL, `base_model_id` MUST be `NULL` (None), NOT `''` (empty
string).

Open WebUI's model merge logic (`utils/models.py:144-172`):

```python
if custom_model.base_model_id is None:      # ← Only None triggers override!
    model = base_model_lookup.get(custom_model.id)
    model['info'] = custom_model.model_dump()  # ← Capabilities applied HERE

elif custom_model.is_active:
    if custom_model.id in existing_ids:
        continue                              # ← SKIPPED! Base model used as-is!
```

When `base_model_id = ''` (empty string, NOT `None`):
1. First branch skipped (`'' is not None`)
2. Elif checks if model ID exists in LiteLLM catalog → it does
3. **`continue`** → custom model entry **silently ignored**
4. Base model from LiteLLM used **without any capabilities**
5. `function_calling` **defaults to `native`** → model hallucinates tool JSON

**Fix:** `UPDATE model SET base_model_id = NULL WHERE base_model_id = '';`

**How to check:** All models in the `model` table should have
`base_model_id = None` (NULL). If any have `''`, their capabilities are
being silently ignored.

### Secondary defenses (apply AFTER fixing base_model_id)

Once `base_model_id = NULL` is fixed and capabilities are properly loaded,
these settings take effect:

**In Open WebUI DB — model params:**
```python
params['function_calling'] = 'none'  # THE key fix: stop native FC signal
params['tool_choice'] = 'none'       # Belt-and-suspenders: no tools in request
```

**In Open WebUI DB — model capabilities:**
```python
meta['capabilities']['builtin_tools'] = False   # Disable builtin tools
meta['capabilities']['web_search'] = False
meta['capabilities']['code_interpreter'] = False
meta['capabilities']['terminal'] = False
meta['capabilities']['image_generation'] = False
```

**In LiteLLM DB — model_info (prevents function-calling advertisement):**
```sql
UPDATE "LiteLLM_ProxyModelTable"
SET model_info = '{"supports_function_calling": false}'
WHERE model_name IN ('qwen3:1.7b', 'qwen2.5-coder:3b', 'llama3.2:3b');
```

**In Modelfile — system prompt (prevents training artifact):**
```
SYSTEM """...Do NOT use any tools or functions. Respond only in plain text..."""
```

### Summary of required fixes per model

| Model | base_model_id | DB params | Modelfile system prompt |
|-------|---------------|-----------|------------------------|
| qwen3:1.7b | NULL ✅ | `function_calling: "none"`, `tool_choice: "none"`, `reasoning_tags: false`, `think: false` | "Do NOT use any tools or functions" |
| qwen2.5-coder:3b | NULL (fix!) | `function_calling: "none"`, `tool_choice: "none"` | "Do NOT use any tools or functions" |
| llama3.2:3b | NULL (fix!) | `function_calling: "none"`, `tool_choice: "none"` | "Do NOT use any tools or functions" |

**Two layers are critical:**
1. `base_model_id = NULL` — without this, ALL settings are silently ignored
2. `function_calling = "none"` — without this, the model gets the native FC signal and hallucinates tool calls

### Upstream feedback

Filed as issue [#26823](https://github.com/open-webui/open-webui/issues/26823).
Closed by maintainer Classic298 with the explanation that `function_calling:
native` is the intended default (not a bug). The `base_model_id` empty-string
behavior was not addressed. Issue closed — not worth reopening.

## `{}` Empty Response Bug (Qwen3 + LiteLLM + Open WebUI)

**Symptom:** Model returns empty `{}` in the chat instead of text.

**Root cause:** Pipeline bug (Mechanism 1 above) — registered builtin tools
cause dropped stream chunks. Additionally, Qwen3's `reasoning_tags` output
causes Open WebUI's handler to drop subsequent `content` chunks (Open WebUI
issue #24697).

**Fixes applied (both required):**
```python
# In model params:
params['tool_choice'] = 'none'
params['reasoning_tags'] = False
params['think'] = False

# In model capabilities:
meta['capabilities']['builtin_tools'] = False
meta['capabilities']['code_interpreter'] = False
meta['capabilities']['terminal'] = False
meta['capabilities']['web_search'] = False
```

## Web Search Does NOT Work via Automatic Injection

Open WebUI v0.10.2 (current) implements web search exclusively as a **tool call**,
not as server-side automatic injection. The model MUST:
- Have `function_calling` enabled (either `"native"` or default)
- Have `web_search: true` in capabilities
- Actually call the `web_search` function

There is no "auto-inject search results into the prompt" fallback. If the model
doesn't call the tool, no search happens.

**Qwen3 1.7B** can receive the `web_search` tool but is too small to reliably
decide when to call it. Enabling both `builtin_tools` and `web_search` triggers
the `{}` bug (model calls wrong tools). Keeping `tool_choice=none` prevents
all tool use including web_search.

**Bottom line:** On this stack (Qwen3 1.7B + LiteLLM + Open WebUI v0.10.2),
web search via SearXNG is not practically usable. A larger model or a
different web search approach (e.g., embedding-based RAG with automatic
context injection) would be needed.
