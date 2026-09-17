No pending tasks. Last cleared: 2026-09-17.

## Key New File
- `docs/ai/TIPS.md` — Open WebUI DB operations (model params, capabilities, web search config, `{}` bug fix, SearXNG integration status, models-proxy-Kette/Cache-TTL/10.8.0.18-Pitfall). Read before any future Open WebUI or LiteLLM configuration work.

## Issue #18 — Evaluated (2026-09-17, committed 921c4a6 + Folge-Commit pending, open)
Streaming-Tool-Calls via LiteLLM defekt — Upgrade 1.91.0 → 1.101.0 evaluiert, Bug bleibt (Root-Cause: LiteLLM demotiert native ollama-tool_calls-Frames zu Content-Text). Behalten + Digest gepinnt (keine Regression).
Workaround VERIFIZIERT: Direkt-Provider `ollama-direct` in `~/.config/opencode/opencode.json` (alle 6 Tags, Default `ollama-direct/qwen3:8b`) — e2e-Agent-Run mit Write-Tool erfolgreich. Nicht git-tracked (Heimverzeichnis).
Folge-Änderungen für nächsten Commit (#18): CONVENTIONS (Direkt-Provider-Regel), STATE (Direkt-Fokus), HANDOFF (dieser Eintrag).

## Issue #17 — Implemented (2026-09-17, committed dbb21e2 + 60178ce + Folge-Commit pending, open)
Qwen3:8B lokal für OpenCode + Whisper gestoppt (100 % GPU, 58 tok/s) + Whisper-Deaktivierung (`restart: no`, DB-Eintrag gelöscht, STT künftig via GROQ).
Folge-Änderungen für nächsten Commit (#17): `litellm/compose.yaml` (restart-no), PITFALLS (Restore-Anleitung), STATE (Dauerhaft-Fokus), HANDOFF (dieser Eintrag).
Live-Zustand: whisper-Container `exited` + Autostart aus; Katalog = 6 Modelle ohne whisper-1.

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
