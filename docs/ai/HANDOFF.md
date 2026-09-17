No pending tasks. Last cleared: 2026-09-17.

## Key New File
- `docs/ai/TIPS.md` — Open WebUI DB operations (model params, capabilities, web search config, `{}` bug fix, SearXNG integration status, models-proxy-Kette/Cache-TTL/10.8.0.18-Pitfall). Read before any future Open WebUI or LiteLLM configuration work.

## Issue #17 — Implemented (2026-09-17, commit pending)
Qwen3:8B lokal für OpenCode verfügbar gemacht. Implementiert + verifiziert, Commit steht noch aus.
Repo-Änderungen:
- `ollama/Modelfile.qwen3-8b` (neu, Parameter wie 1.7b)
- `docs/ai/PITFALLS.md` → Qwen3-Thinking-Budget-Eintrag
- `docs/ai/STATE.md` → 7-Modell-Fokus + Completed-Eintrag

Live-Änderungen (nicht git-tracked):
- ollama: `qwen3:8b` (5,2 GB) gepullt + Tag-Override via Modelfile
- LiteLLM-DB: INSERT qwen3:8b (jetzt 7 Zeilen)
- Container `litellm` restartet, opencode-Cache gelöscht

## Issue #16 — Completed (2026-09-17, committed 7a5fcb5, closed)
Repo-Änderungen (Phase 1/4):
- `litellm/.env.example` → LITELLM_PUBLIC_URL auf 10.8.0.16 + Sync-Header
- `litellm/opencode.json.example` → baseURL 10.8.0.16
- `litellm/opencode-env.sh` → OPENCODE_MODELS_URL 10.8.0.16
- `litellm/models_proxy.py` → default-Fallback 10.8.0.16
- `litellm/README.md` → SQL-Beispiel api_base 10.8.0.16
- `docs/ai/CONVENTIONS.md` → IP-Sync-Regel, Modell-Kette
- `docs/ai/TIPS.md` → Models-Proxy-Kette, Stale-Debugging, 10.8.0.18
- `docs/ai/PITFALLS.md` → 4 neue Einträge (10.8.0.18, host.docker.internal, stale-cache, stale-models-dual-layer)
- `docs/ai/DECISIONS.md` → Entscheidung 2026-09-17 (10.8.0.16 als canonical URL-Basis)
- `docs/ai/STATE.md` → Current Focus aktualisiert (5/6 Modelle), Cortecs-Eintrag + Issue-16-Eintrag in Completed

Live-Änderungen (Phase 2, nicht git-tracked):
- `/opt/litellm/.env`: LITELLM_PUBLIC_URL → 10.8.0.16
- LiteLLM-DB: 6 Modelle (UPDATE api_base 2×, INSERT 3×, DELETE 1×) — Dump vorher unter `/tmp/opencode/litellm_table_before_20260917_*.txt`
- `litellm/models_proxy.py`: default synchronisiert (copy aus repo)
- Container `litellm` + `models-proxy` force-recreated

## Open (2026-08-13)

1. [ ] Cortecs-Vertrag anfragen: E-Mail-Entwurf in `docs/extern/cortecs-anfrage-email-draft.md` an `enterprise@cortecs.ai` senden. Bildungs-Rabatt, DPA, Modellpreise, Zero-Data-Retention, 30-Tage-Pilot klären.
2. [ ] Hardware-Entscheidung (Issues #2, #5, #7) aktualisieren: Framework Desktop Strix Halo 128 GB (~€1.850) als On-Prem-Backend für DSGVO-kritische Last + Q3-Modelle bestellen. Kalkulation in `docs/extern/on-premise-vs-api-kalkulation.md`. Mac Studio M5 Max 192 GB als spätere Ergänzung (Phase 2) für Q8-lossless DeepSeek V4 Flash vorgemerkt.
3. [ ] Issue #14 (Token- und Auth-Konzept) ergänzen: Cortecs-Volumen (mittleres Szenario ~325 Mio Tok/Monat, ~€1.800/Jahr) + Virtual-Keys mit Cap (z. B. $5/Schüler/Monat) berücksichtigen. Drei-Säulen-Modell (On-Prem DSGVO-kritisch + Cortecs Massenlast + Phasen-Strategie) als Grundlage.
