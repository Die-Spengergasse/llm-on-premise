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

## In Evaluierung

- Hardware-Optionen (AMD Strix Halo, Mac Mini Pro, DGX Spark) — siehe Issues #2, #5, #7
- Modell-Routing-Strategie (LiteLLM Access Groups) — siehe Issue #6
- Gemma 4 Family als VIP-Modell — siehe Issue #7
- Netzwerk-Isolation der Backend-Knoten — siehe Issue #4
- ROCm vs. CUDA für AMD-Hardware – Strix Halo erfordert ROCm-Kompatibilität mit vLLM
