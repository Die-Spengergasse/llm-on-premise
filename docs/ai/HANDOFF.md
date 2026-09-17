Issue #21 — Implemented (2026-09-17, commit follow-up pending). Working copy synchron mit Trunk.

## Done (Issue #21)
- Open WebUI: direkte Ollama-Connection (10.8.0.16:11435) aktiviert; stale 10.8.0.18 in openai.api_base_urls + rag.ollama korrigiert.
- Web-Search-Experiment `qwen3:8b-search` (Tag + Modelfile im Repo): FC=native, builtin_tools=true, `meta.builtinTools`-Gating (nur web_search), System-Prompt nennt search_web/fetch_url. e2e verifiziert (JWT + Socket.io): tool_calls → SearXNG gregor:80 → 2. Turn → Antwort. 6 Produktionsmodelle bleiben Lockdown.
- `OLLAMA_MAX_LOADED_MODELS=1` verifiziert (2. Modell evicted residentes).
- GROQ-Token-Rotation: Setup-Anleitung + SQL-Template in whisper/README.md.
- Docs: TIPS (Native Tool-Call Mechanics + Admin-Workflow + searxng-URL-Fix), PITFALLS (3 neue), DECISIONS, STATE.

## Open (Issue #21 / nächste Session)
1. [ ] GROQ-Keys von Schülern einsammeln → LiteLLM-Deployment-Rows anlegen (SQL-Template whisper/README.md) → Open WebUI `audio.stt.model=groq-whisper` → Mic-e2e-Test.
2. [ ] **UI-Verifikation Open WebUI Web Search durch Georg selbst machen** (qwen3:8b-search, Globe-Icon): API-e2e lief, echter UI-Durchlauf (Chat speichern, Zitaten-UI) noch nicht getestet — Session 2026-09-17 endete hier (Georg hatte keine Zeit mehr); Open WebUI URL: `http://10.8.0.16:3000`.
3. [ ] `search_chats`/`view_chat` leakt durch `builtinTools`-Gating — ggf. Upstream-Check, ob Kategorie-Gate fehlt.
4. [ ] Beim nächsten eigenen UI-Test prüfen, ob der `{}`-Bug (Stream-Drop mit builtin_tools=true) bei qwen3:8b-search im UI-Streaming auftritt (reasoning_tags/think=false sind gesetzt — sollte OK sein).
5. [ ] Admin-Promotion: Sobald neue Admins sich 1× per LDAP einloggen, im Admin Panel promoten (TIPS.md „Admin accounts").

## Offene Todos (älter)
1. [ ] Cortecs-Vertrag anfragen: E-Mail-Entwurf in `docs/extern/cortecs-anfrage-email-draft.md` an `enterprise@cortecs.ai` senden.
2. [ ] Hardware-Entscheidung (Issues #2, #5, #7) aktualisieren: Framework Desktop Strix Halo 128 GB (~€1.850) bestellen (Kalkulation in `docs/extern/on-premise-vs-api-kalkulation.md`).
3. [ ] Issue #14 (Token- und Auth-Konzept) ergänzen: Cortecs-Volumen + Virtual-Keys mit Cap + Drei-Säulen-Modell.
