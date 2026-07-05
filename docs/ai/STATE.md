# STATE — llm-on-premise

## Current Focus
gregor-Stack live: LiteLLM + Postgres + SingleGpuGuard + models.dev-Proxy in Docker; opencode entdeckt Modelle dynamisch (kein Sync-Skript mehr). Katalog jetzt wirklich 2 Modelle (e2b/e4b-128k) — nach Fix des Virtual-Key-`models`-Pinning (2026-07-05 Session 2; siehe Completed). SingleGpuGuard 2026-07-05 um Staleness-Self-Heal + ollama-`/api/ps`-Reconcile erweitert (behebt den 429-Forever-Bug durch geleakte in_flight-Counter + Out-of-band-Load-Divergenz).

## Completed (this cycle)
- [x] Web-Recherche: Aktuelle GPU-Mietpreise, API-Preise, Education-Pläne (Stand Juni 2026)
- [x] Web-Recherche: Open Source vs. Closed Source Benchmarks (GLM-5.2, DeepSeek V4, Qwen 3.6 vs. GPT-5.5, Claude Opus 4.8)
- [x] Web-Recherche: Apple Mac Mini M4 Pro Preise für LLM-Inference
- [x] Web-Recherche: AMD Strix Halo Preis und Verfügbarkeit
- [x] Web-Recherche: Schülernachweis Spengergasse (2.600 Schüler, 280 Lehrer, 97 Klassen)
- [x] Präsentation in docs/praesentation/slides.md erstellt (HTML + PDF)
- [x] Phasen-Strategie definiert: API 2026 → HW-Nachkauf 2027/28 → autark 2028+
- [x] Dev/Test-Host inventarisiert (infra/hosts/gregor.md) – RTX 2070 SUPER/8 GB; inzwischen Host gregor (interim inference+gateway, s. 2026-07-05)
- [x] Power-Fix für Dual-8-Pin RTX 2070 entschieden: 6→8 Pin PCIe-Adapter am zweiten VX550-Strang (Issue #12)
- [x] ZID-Präsentation (2026-06-24) archiviert nach docs/praesentation/archiv/2026-06-24-zid-pitch/
- [x] Eröffnungskonferenz-Präsentation erstellt: docs/praesentation/slides.md (4 Folien, Bird's-Eye, HTML + PDF)
- [x] GitHub Pages aktiviert (source=Actions) + Workflow .github/workflows/deploy-pages.yml
- [x] gregor: ollama_backend auf :11435 (OLLAMA_HOST=0.0.0.0:11435, MAX_LOADED_MODELS=1, KEEP_ALIVE=-1, FLASH_ATTENTION=1)
- [x] LiteLLM-Stack unter /opt/litellm/ (Docker: litellm + Postgres 16 + models-proxy); LiteLLM auf :11434
- [x] SingleGpuGuard-Plugin (/opt/litellm/single_gpu_guard.py): Single-GPU-Residency-Regel (busy→429, idle→Swap) via litellm_call_id-Matching; e2e getestet
- [x] Passwortloses sudo für georg via /etc/sudoers.d/georg eingerichtet
- [x] e4b-Varianten gepullt (e4b-it-qat 6,1 GB, e4b q4_K_M 9,6 GB); e4b-128k-Tag erstellt (e4b-it-qat @128K); OOM-Test bestanden (6,35 GB VRAM)
- [x] LiteLLM Virtual Keys erzeugt: opencode-gregor + catalog-proxy
- [x] models.dev-Merging-Proxy (/opt/litellm/models_proxy.py) injiziert litellm-Provider; User-Agent-Fix (403 von Cloudflare) — 152 Provider, Built-Ins überleben
- [x] opencode.json auf `provider.litellm = { options }` reduziert (kein models/npm/name); opencode.jsonc gelöscht
- [x] OPENCODE_MODELS_URL in ~/.bash_aliases gesetzt; A/B-Beweis: mit env 7 litellm-Modelle, ohne 0
- [x] opencode-ollama-sync archiviert (git mv → scripts/archive/) in opencode-helpers-Repo, committed & gepusht
- [x] SingleGpuGuard 429-Forever-Bug gefixt (2026-07-05): Wurzel = geleakter `in_flight`-Counter (abgebrochene Streaming-Requests feuern kein `async_log_failure_event` → Counter klebt bei >0 → jedes andere Modell bekommt ewig 429). Fix: (a) Staleness-Self-Heal (`_Domain.last_busy_at` + `_STALE_AFTER=660s`, Reset+Swap statt 429 bei stale), (b) ollama-`/api/ps`-Reconcile (pollt ollamas real geladenes Modell, adoptiert es bei `in_flight==0`; korrigiert Out-of-band-Loads via `ollama run`/`:11435`-Bypass), (c) `_domain()` löst `api_base` via `config.yaml`-Map (pre_call hat `litellm_params` noch leer), (d) Traces `ACCEPT/SAME/SWAP/STALE-RESET/RECONCILE` für Observability. E2e verifiziert: idle-swap ✓, busy→429 ✓, stale-self-heal ✓ (Abort reproduziert Leak, `STALE-RESET`+`SWAP` nach <660s), reconcile bei out-of-band-Load ✓.
- [x] LiteLLM-Katalog auf Max-Context-only reduziert (2026-07-05): `config.yaml` `model_list` → nur `gemma4:e2b-128k` + `gemma4:e4b-128k` (beide 128K = e2b/e4b-Max). 5 4K-Default-Varianten entfernt. 12B/12b-it-qat nicht auf 256K gesetzt (6,36 GB Weights + ~4–8 GB KV >> 1,64 GB freie VRAM auf 8 GB gregor → OOM/Offload). *Korrektur:* die ursprüngliche Behauptung „`/v1/models`=2 verifiziert" stimmte NICHT — `/v1/models` lieferte weiterhin 7, weil die Virtual Keys (`opencode-gregor` + `catalog-proxy`) hartcodierte 7-Modelle-Listen hatten (siehe PITFALLS.md, „`/v1/models` ist key-scoped"). Echt behoben in der Folgesession (nächster Punkt).
- [x] **Echte Katalog-Bereinigung + Blob-Inventory (2026-07-05, Session 2):** Wurzel für „opencode sieht keine/stale Modelle" gefunden — LiteLLM `/v1/models` ist **key-scoped** (`get_available_models_for_user`), liefert die `models`-Allowance des API-Keys, NICHT den Router-Katalog. Beide Virtual Keys hatten die 7-Modelle-Liste hartcodiert → `/v1/models`=7 egal was `config.yaml`/ollama taten. Fix: (a) `models`-Restriction beider Keys auf `{}` gesetzt (erben live den Proxy-Katalog), (b) 5 ungewollte Tags (`e2b`, `e4b`, `e4b-it-qat`, `12b`, `12b-it-qat`) via `ollama rm` entfernt — aber ZUERST ihre 11 unique Blobs (22,6 GiB; shared Blobs bleiben via `-128k`-Tags) + 5 Manifeste nach `/opt/litellm/blob-inventory/` (nicht git) kopiert + sha256-verifiziert, Restore-README geschrieben, (c) LiteLLM restartet (flusht Key-Cache). E2e verifiziert: ollama `/api/tags`=2 → LiteLLM `/model/info`=2 → `/v1/models`=2 → models-proxy `litellm`=2. Detail & Restore im PITFALLS.md + DECISIONS.md + `infra/hosts/gregor.md`.

## Pending
- [x] opencode `OPENCODE_MODELS_URL`-Problem gelöst (2026-07-05): daemonized `opencode serve` erbt nun die Env-Var; Picker zeigt die 2 LiteLLM-Modelle.
- [ ] Katalog-Änderungen in Zukunft: `models`-Restriction der Virtual Keys bleibt leer (`{}`) — sie erben den Proxy-Katalog automatisch. Beim Hinzufügen eines Modells: ollama-Tag pullen → `config.yaml` `model_list`-Eintrag → `docker compose restart litellm` (Config wird nur am Startup gelesen). Kein Key-Edit nötig solange `models={}`.
- [ ] OPENCODE_MODELS_URL für Schüler-Lab austollen (Shared-Launcher / /etc/profile.d) — aktuell nur georgs Shell
- [ ] Management-VM aufsetzen (Issue #3) — LiteLLM migriert dann dorthin (rsync /opt/litellm + compose up, api_base bleibt <WG_IP_GREGOR>; IP siehe `infra/hosts/secrets.local.md`)
- [ ] Network Hardening / ufw für :11435 (Issue #4) — aktuell Bypass möglich (Known Gap)
- [ ] Hardware-Entscheidung (Issues #2, #5, #7)
- [ ] LiteLLM Access Control / Virtual-Keys für User-Groups (Issue #6)
- [ ] dev-rig-01: Adapter einbauen, PCIe-Stränge prüfen, Specs nachtragen (Issue #12)

## Blockers
- Hardware-Entscheidung
- ZID-Koordination (Netzwerk, VLAN, SSO)

## Next Session Suggestion
Echten Chat via opencode-Picker mit gesetztem OPENCODE_MODELS_URL testen (Modell laden, Contention-429 bei并行 anderen Modells verifizieren). Dann OPENCODE_MODELS_URL für die Schüler austollen.