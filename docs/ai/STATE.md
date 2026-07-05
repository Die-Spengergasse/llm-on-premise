# STATE — llm-on-premise

## Current Focus
gregor-Stack live: LiteLLM + Postgres + SingleGpuGuard + models.dev-Proxy in Docker; opencode entdeckt Modelle dynamisch (kein Sync-Skript mehr).

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

## Pending
- [ ] Shell reloaden / opencode neu starten, damit OPENCODE_MODELS_URL + reduzierte Config greifen (läuft noch mit altem Cache)
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