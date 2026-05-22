# DECISIONS — llm-on-premise

## Beschlossen

| Datum | Entscheidung | Status |
|---|---|---|
| 2026-05-15 | Management-VM mit LiteLLM + Open WebUI + SearXNG als feste Architektur | Beschlossen |
| 2026-05-15 | AI-Backend nicht öffentlich erreichbar, nur via Proxy | Beschlossen |
| 2026-05-15 | Auth durch Schul-Infrastruktur (SSO/IdM), keine eigene Auth-Lösung | Beschlossen |
| 2026-05-15 | Zugriff neben Browser auch via Coding-Tools (OpenCode, Kilo Code) über OpenAI-kompatible API | Beschlossen |

## In Evaluierung

- Hardware-Optionen (DGX Spark, AMD Strix Halo, Multi-GPU, Mac Studio) — siehe Issues #2, #5, #7
- Modell-Routing-Strategie (LiteLLM Access Groups) — siehe Issue #6
- Gemma 4 Family als VIP-Modell — siehe Issue #7
- Netzwerk-Isolation der Backend-Knoten — siehe Issue #4
