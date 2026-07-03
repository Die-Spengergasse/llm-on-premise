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
| 2026-07-02 | RTX 2070-Host (dev-rig-01) als Dev/Test-Rig, nicht als vLLM-Backend (8 GB VRAM zu klein für Zielmodelle GLM-5.2/DeepSeek V4/Qwen 3.6) | Beschlossen |
| 2026-07-02 | Power-Fix dev-rig-01: 6→8 Pin PCIe-Adapter am zweiten VX550-Strang; kein Y-Splitter (Überlastungsgefahr) | Beschlossen |
| 2026-07-02 | Präsentation vom 2026-06-24 (ZID-Pitch, detailliert/technisch) archiviert unter docs/praesentation/archiv/2026-06-24-zid-pitch/ – Vorschläge sehr positiv aufgenommen | Erledigt |
| 2026-07-02 | Neue Eröffnungskonferenz-Präsentation (4 Folien, High-Level/Bird's-Eye): Zweck = Chancengleichheit + Schul-Autonomie; Ansatz = Hybridmodell (eigene HW + Token-Kontingente + gemietete Rechenleistung CPU/GPU/LPU/NPU). Keine fertigen Entscheidungen, Details offen | In Arbeit |

## In Evaluierung

- Hardware-Optionen (AMD Strix Halo, Mac Mini Pro, DGX Spark) — siehe Issues #2, #5, #7
- Modell-Routing-Strategie (LiteLLM Access Groups) — siehe Issue #6
- Gemma 4 Family als VIP-Modell — siehe Issue #7
- Netzwerk-Isolation der Backend-Knoten — siehe Issue #4
- ROCm vs. CUDA für AMD-Hardware – Strix Halo erfordert ROCm-Kompatibilität mit vLLM
- Externes KI-Kursangebot (pup-consulting.at) – fachliche Klärung offen — siehe docs/extern/externes-ki-kursangebot.md
