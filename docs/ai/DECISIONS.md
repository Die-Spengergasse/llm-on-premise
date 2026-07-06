# DECISIONS — llm-on-premise

## Beschlossen

| Datum | Entscheidung | Status |
|---|---|---|
| 2026-05-15 | Management-VM mit LiteLLM + Open WebUI + SearXNG als feste Architektur | Beschlossen |
| 2026-05-15 | AI-Backend nicht öffentlich erreichbar, nur via Proxy | Beschlossen |
| 2026-05-15 | Auth durch Schul-Infrastruktur (SSO/IdM), keine eigene Auth-Lösung | Beschlossen |
| 2026-05-15 | Zugriff neben Browser auch via Coding-Tools (OpenCode, Kilo Code) über OpenAI-kompatible API | Beschlossen |
| 2026-06-24 | Open-Source-Modelle als primäre Modellbasis (GLM-5.2, DeepSeek V4, Qwen 3.6) – MIT/Apache 2.0-Lizenzen | Beschlossen |
| 2026-06-24 | Phasen-Strategie: Phase 1 (2026/27) API-lastig, Phase 2 (2027/28) HW-Nachkauf bei fallenden Preisen, Phase 3 (2028+) autark | Beschlossen |
| 2026-06-24 | Hardware-Favoriten: Apple Mac Mini Pro + AMD Strix Halo (DGX Spark durch Preiserhöhung €4.950 zu teuer für den Einstieg) | Beschlossen |
| 2026-06-24 | Hybrid-Ansatz: On-Premise für DSGVO-kritische Daten, API (DeepSeek/SiliconFlow) für Massenlast | Beschlossen |
| 2026-07-02 | RTX 2070-Host (dev-rig-01) als Dev/Test-Rig, nicht als vLLM-Backend (8 GB VRAM zu klein für Zielmodelle GLM-5.2/DeepSeek V4/Qwen 3.6) — 2026-07-05 zu **gregor** umbenannt + interim inference+gateway (ollama+LiteLLM); weiterhin kein vLLM-Backend | Beschlossen |
| 2026-07-02 | Power-Fix dev-rig-01: 6→8 Pin PCIe-Adapter am zweiten VX550-Strang; kein Y-Splitter (Überlastungsgefahr) | Beschlossen |
| 2026-07-02 | Präsentation vom 2026-06-24 (ZID-Pitch, detailliert/technisch) archiviert unter docs/praesentation/archiv/2026-06-24-zid-pitch/ – Vorschläge sehr positiv aufgenommen | Erledigt |
| 2026-07-02 | Neue Eröffnungskonferenz-Präsentation (4 Folien, High-Level/Bird's-Eye): Zweck = Chancengleichheit + Schul-Autonomie; Ansatz = Hybridmodell (eigene HW + Token-Kontingente + gemietete Rechenleistung CPU/GPU/LPU/NPU). Keine fertigen Entscheidungen, Details offen | In Arbeit |
| 2026-07-05 | LiteLLM (Docker, bundled Postgres 16, `api_base`=gregors WireGuard-IP `<WG_IP_GREGOR>`, siehe `infra/hosts/secrets.local.md`; temporär/DHCP) als zentraler Gateway statt Custom-FastAPI-Proxy — wegen Virtual-Keys/Budgets/Rate-Limits und Skalierung auf hunderte User. `:main-stable` akzeptiert kein SQLite mehr (PITFALLS). | Beschlossen |
| 2026-07-05 | SingleGpuGuard-Plugin (`/opt/litellm/single_gpu_guard.py`) implementiert Single-GPU-Residency-Regel (busy→HTTP 429, same model OK, idle→atomic swap) per `litellm_call_id`-Matching; ein residentes Modell auf der 8-GB-GPU. Konfig ist per-backend (api_base) keyed → korrekt nach Migration auf mehrere Knoten. | Beschlossen |
| 2026-07-05 | opencode-Modell-Discovery über models.dev-Merging-Proxy (`:11436`, `OPENCODE_MODELS_URL`) statt Fork-Patch/PR (upstream opencode #6231) — behält npm-binary, macht Sync-Skript obsolet. Provider-Id in opencode = `litellm` (nicht `ollama`), opencode.json enthält nur `{ options }`. | Beschlossen |
| 2026-07-05 | `gemma4:e4b-128k` (e4b-it-qat @128K) als Sweet-Spot für die 8-GB-Mappe; die ~1,4 GB VRAM-Headroom bleiben bewusst als KV-Cache-Puffer für lange Sessions, nicht "verschenkt". 192K/256K abgelehnt — e4b hat 128K nativ (12B/26B/31B haben 256K). | Beschlossen |
| 2026-07-05 | Firewall-Regeln (ufw) bewusst NICHT umgesetzt — `:11435` (ollama) bleibt direkt erreichbar (Known Gap, Bypass um LiteLLM-Auth möglich); auf Issue #4 verschoben. `:11434` ist Container-Port → ufw kann ihn ohnehin nicht filtern. | Verschoben |
| 2026-07-05 | LiteLLM-Katalog auf Max-Context-only reduziert: nur `gemma4:e2b-128k` + `gemma4:e4b-128k` (beide 128K = architektonisches Max der e2b/e4b-Varianten). 4K-Default-Varianten (`e2b`, `e4b`, `e4b-it-qat`, `12b`, `12b-it-qat`) aus `config.yaml` `model_list` entfernt — ein Modell mit nur 4K Kontext ist pädagogisch wertlos. 12B/12b-it-qat NICHT auf 256K (sein Max) gesetzt, weil 6,36 GBWeights + ~4–8 GB KV-Cache @256K >> 1,64 GB freie VRAM auf der 8 GB gregor-GPU (OOM oder CPU-KV-Offload = unbrauchbar langsam). | Beschlossen |
| 2026-07-05 | **5 ungewollte Tags aus ollama entfernt + Blobs inventarisiert** (Session 2; revidiert den „Blob bleibt in ollama"-Teil des ursprünglichen Plans): `ollama rm gemma4:{e2b,e4b,e4b-it-qat,12b,12b-it-qat}`, aber ZUERST die 11 zu den Tags uniqueen Blobs (~22,6 GiB; shared Weight-Blobs überleben via der behaltenen `-128k`-Tags) + 5 Manifeste nach `/opt/litellm/blob-inventory/` (NICHT git; README + tag-digest-map.json mit Restore-Anleitung) kopiert und sha256-verifiziert. Grund: die Tags mussten aus ollama raus, sonst tauchen sie (falls ein Key sie erlaubt) weiter im Picker auf. Restore bei >8 GB-HW (Issues #2/#5/#7): Blobs+Manifeste zurückkopieren + `systemctl restart ollama`. | Beschlossen |
| 2026-07-05 | **Virtual Keys ohne `models`-Restriction** (`models = '{}'`): beide gregor-Keys ... | Beschlossen |
| 2026-07-05 | **qwen3:4b als sole LLM** (Session 3 — SUPERSEDED by Session 4, see HISTORY.md): alle bisherigen Modelle (gemma4:e2b/e4b-128k, qwen3:8b) aus ollama entfernt und Blobs inventarisiert (→ `/opt/litellm/blob-inventory/`, Stand: 24 Blobs / 40 GiB). `qwen3:4b` (2,5 GB, 256K native Context) läuft auf ollama. `config.yaml` enthält nur `qwen3:4b` + `whisper-1`. Grund: 256K Context + kleines Weight-Footprint (~3 GB VRAM) erlauben Koexistenz mit whisper (~3,9 GB) auf 8 GB GPU. | Superseded |
| 2026-07-05 | **Open WebUI mit LDAP (Session 3):** Open WebUI als user-facing Chat-Frontend deployt (`ghcr.io/open-webui/open-webui:main`), authentifiziert gegen Schul-AD via LDAPS (`ldap.spengergasse.at:636`). LiteLLM bleibt der Backend-Aggregator (`:11434`), Open WebUI verwendet den shared `opencode-gregor`-Key. STT-Engine auf `openai` gestellt, sendet Audio an lokales whisper via LiteLLM. HTTPS/Caddy für Mic-Zugriff ist offen (Issue #14). | Beschlossen |
| 2026-07-05 | **Modell-Swap: qwen3:4b (4B, 2,5 GB) → qwen3:1.7b (1,7B, 1,4 GB) via Modelfile-Tag-Override** (Session 4): Realer 4B-Modell lief zu langsam (~59 s, 87% GPU, BW-bound). Stattdessen qwen3:1.7b gepullt, mit `ollama create qwen3:4b -f Modelfile.qwen3` als selber Tag überschrieben — LiteLLM-Config (`config.yaml`) bleibt unverändert. Ergebnis: ~140 tok/s, 100% GPU, ~3 s Antwortzeit. Modelfile in `infra/litellm/Modelfile.qwen3`. | Beschlossen |
| 2026-07-05 | **24K Kontext mit Q8-KV-Cache** (Session 4): Binary Search ergab 24K als maximum, das 100% GPU-Layer hält (whisper ~3,9 GB + LLM ~2,8 GB = 6,7 GB von 8 GB). 256K native Context → CPU-Offload (zu langsam). `OLLAMA_KV_CACHE_TYPE=q8_0` halbiert KV-Cache-Speicher vs. fp16. `num_ctx 24576` im Modelfile. | Beschlossen |
| 2026-07-05 | **Generation-Parameter** (Modelfile, Session 4): temperature=0.5, top_p=0.85, top_k=40, min_p=0.05, repeat_penalty=1.08. Konservative Werte halten das 1,7B-Modell fokussiert. | Beschlossen |
| 2026-07-05 | **Builtin-Tools deaktiviert + tool_choice=none** (Session 4–5): Qwen3 1.7B ruft builtin-Tools (write_note, list_knowledge_bases, calculate_timestamp, explain_options_trading) auf → LiteLLM/Ollama-Streaming liefert Tool-Call-Deltas → Open WebUI's Stream-Handler produziert leeres `{}`. Fix: `capabilities.builtin_tools=false`, `code_interpreter=false`, `terminal=false`, `image_generation=false` in der Open-WebUI-DB; `params.tool_choice="none"`. Web-Search (via SearXNG) ist in Open WebUI v0.10.2 ausschließlich als Tool-Call implementiert, daher nicht nutzbar mit `tool_choice=none`. Ein größeres Modell mit stabilem Function-Calling wäre nötig. Detail in `docs/ai/TIPS.md`. | Beschlossen |

## In Evaluierung

- Hardware-Optionen (AMD Strix Halo, Mac Mini Pro, DGX Spark) — siehe Issues #2, #5, #7
- Modell-Routing-Strategie (LiteLLM Access Groups) — siehe Issue #6
- Gemma 4 Family als VIP-Modell — siehe Issue #7
- Netzwerk-Isolation der Backend-Knoten — siehe Issue #4
- ROCm vs. CUDA für AMD-Hardware – Strix Halo erfordert ROCm-Kompatibilität mit vLLM
- Externes KI-Kursangebot (pup-consulting.at) – fachliche Klärung offen — siehe docs/extern/externes-ki-kursangebot.md
