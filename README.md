# LLM On-Premise — Spengergasse

On-premise LLM-Infrastruktur für die Spengergasse. Gemanagt über eine zentrale VM im ZID-Rechenzentrum mit LiteLLM, Open WebUI und SearXNG.

## Status: Planning

Die konkrete Hardware-Architektur ist noch offen. Zur Diskussion stehen u.a. NVIDIA DGX Spark, AMD Strix Halo, Multi-GPU-Workstation und weitere Optionen. Siehe [Architecture Decision Log](#architecture-decision-log) unten.

## Architektur

```
┌─────────────────────────────────────────────────────────┐
│ ZID Rechenzentrum                                       │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Management VM (einzige öffentlich erreichbare)      │ │
│ │                  Komponente                         │ │
│ │                                                     │ │
│ │ ┌──────────┐  ┌────────────┐  ┌──────────┐          │ │
│ │ │ LiteLLM  │  │ Open WebUI │  │ SearXNG  │          │ │
│ │ │ (Router) │  │ (Chat UI)  │  │ (RAG)    │          │ │
│ │ └────┬─────┘  └─────┬──────┘  └────┬─────┘          │ │
│ │      │              │              │                │ │
│ │ ┌───────────────────────────────────────────────┐   │ │
│ │ │ Auth: bereitgestellt durch Schul-Infra        │   │ │
│ │ │ (SSO / IdM / OAuth2)                          │   │ │
│ │ └───────────────────────────────────────────────┘   │ │
│ └───────────────────┬──────────────────────────────┘    │
│                    │ Internes VLAN ONLY                 │
│       ┌────────────┼────────────┐                       │
│       │            │            │                       │
│  ┌────┴────┐  ┌────┴────┐  ┌───┴─────┐                  │
│  │ Backend │  │ Backend │  │ Backend │                  │
│  │  #1     │  │  #2     │  │  #3     │                  │
│  └─────────┘  └─────────┘  └─────────┘                  │
│                                                         │
│  ← KEIN direkter Zugriff von außen →                    │
└─────────────────────────────────────────────────────────┘
                     │ Schulnetz / VLAN
         ┌───────────┼───────────┐
         │           │           │
      Schüler 1   Schüler 2   Schüler N
   (Browser/IDE) (Browser/IDE) (Browser/IDE)
```

## Hardware

**Noch nicht final entschieden.** Folgende Optionen werden evaluiert:

| Option | Spezifikation | Geschätzter Preis | Vor-/Nachteile |
|---|---|---|---|
| **NVIDIA DGX Spark** | 128 GB Unified Memory, ~273 GB/s, volles CUDA | ~€3.000/Stk. | + CUDA-Ökosystem, + einheitlicher Stack, − geringere Bandbreite |
| **AMD Strix Halo (Ryzen AI Max+ 395)** | 128 GB LPDDR5X, ~112 GB GPU-zuweisbar | ~€1.700–2.500/Stk. | + günstiger, − ROCm hinkt CUDA hinterher |
| **Multi-GPU (RTX 4090/5090)** | 2x 24–32 GB VRAM, hohe Bandbreite | ~€5.000–6.000 | + schnellste Inferenz, − wenig Gesamtspeicher |
| **Mac Studio (M4 Max/Ultra)** | 128–256 GB Unified Memory | ~€3.500–9.500 | + viel Speicher, + leise, − kein CUDA, − macOS-only |

**Aktueller Favorit:** 3x NVIDIA DGX Spark (~€9.000) — aber offen für Alternativen.

Die folgenden Diagramme zeigen die Architektur exemplarisch mit DGX Spark als Backend. Die Management-VM-Architektur bleibt unabhängig von der Hardware-Entscheidung gleich.

## Software-Stack

| Komponente | Zweck |
|---|---|
| **LiteLLM** | API-Proxy, Routing, Rate Limiting, Logging |
| **Open WebUI** | Chat-Frontend für Schüler (browserbasiert) |
| **SearXNG** | Lokale Suchinstanz für RAG / Tool Use |
| **vLLM** | LLM-Serving auf den Backend-Knoten mit Continuous Batching |

## Client-Zugriff

Die Schüler greifen über verschiedene Clients auf die Infrastruktur zu, alle über die **OpenAI-kompatible API** von LiteLLM:

| Client | Verwendung |
|---|---|
| **Open WebUI** | Browserbasierter Chat (über Schul-SSO authentifiziert) |
| **OpenCode** | Terminal-basiertes Coding-Tool (API-Key) |
| **Kilo Code** | VS Code / Cursor-Erweiterung für Coding (API-Key) |
| **Beliebige OpenAI-kompatible Clients** | Weitere Tools die OpenAI-API sprechen |

Auth wird vollständig von der Schul-Infrastruktur bereitgestellt (SSO / IdM). Schüler können sich API-Tokens generieren, um Coding-Tools anzubinden.

## Modell-Belegung (exemplarisch)

Die Modellwahl hängt von der finalen Hardware ab. Aktueller Plan:

| Knoten | Modell | Task | RAM-Bedarf (Q4) |
|---|---|---|---|
| Backend #1 | Qwen3 30B | General + Coding (stark) | ~18 GB |
| Backend #2 | Devstral 24B | Coding-Fokus | ~14 GB |
| Backend #3 | Qwen3 14B | Schnelle Antworten, viele parallele Nutzer | ~8 GB |

## Request-Flow

```
Schüler
    │
    ├── Browser ──── Open WebUI ─────────┐
    ├── OpenCode ──── Direct API-Call ───┤
    ├── Kilo Code ─── Direct API-Call ───┤
    └── Other ──────── Direct API-Call ──┘
                                         │
                            HTTPS + Auth (Schul-SSO / API-Key)
                                         │
                                         ▼
                                  LiteLLM Proxy  ← Routing, Rate Limiting, Logging
                                         │
                            Interner API-Call (VLAN)
                                         │
                                         ▼
                              vLLM Backend  ← Modell-Inferenz + Tool Use (SearXNG)
```

## Netzwerk

- DGX Sparks und Management VM stehen im ZID-Rechenzentrum (19"-Rack, Kühlung vorhanden)
- DGX Sparks sind **nicht öffentlich erreichbar** — nur die Management VM ist per Schul-URL zugänglich
- Interne Kommunikation über VLAN
- Auth wird von der Schul-Infrastruktur bereitgestellt (SSO / IdM), kein separates Auth-System nötig
- API-Tokens für Coding-Clients (OpenCode, Kilo Code) über Schul-Infra generiert

## Budget

| Komponente | Geschätzter Preis |
|---|---|
| 3x NVIDIA DGX Spark 128 GB (alternativ) | ~€9.000 |
| Management VM | ZID-Infrastruktur (keine Extrakosten) |
| **Gesamt (DGX Spark Szenario)** | **~€9.000** |

Andere Hardware-Optionen siehe [Hardware-Tabelle](#hardware).

## Architecture Decision Log

| Datum | Entscheidung | Status |
|---|---|---|
| 2026-05-15 | Projektinitialisierung, Evaluierung der Hardware-Optionen | Offen |
| 2026-05-15 | Management-VM mit LiteLLM + Open WebUI + SearXNG als feste Architektur | Beschlossen |
| 2026-05-15 | AI-Backend nicht öffentlich erreichbar, nur via Proxy | Beschlossen |
| 2026-05-15 | Auth durch Schul-Infrastruktur (SSO/IdM), keine eigene Auth-Lösung | Beschlossen |
| 2026-05-15 | Zugriff neben Browser auch via Coding-Tools (OpenCode, Kilo Code) über OpenAI-kompatible API | Beschlossen |

## Issues

| # | Titel | Labels |
|---|---|---|
| [#1](https://github.com/Die-Spengergasse/llm-on-premise/issues/1) | Docs: create detailed architecture documentation | documentation |
| [#2](https://github.com/Die-Spengergasse/llm-on-premise/issues/2) | Infra: configure DGX Spark nodes with vLLM | infrastructure |
| [#3](https://github.com/Die-Spengergasse/llm-on-premise/issues/3) | Infra: set up management VM (LiteLLM + Open WebUI + SearXNG) | infrastructure |
| [#4](https://github.com/Die-Spengergasse/llm-on-premise/issues/4) | Infra: network hardening — AI servers not publicly reachable | infrastructure, security |
| [#5](https://github.com/Die-Spengergasse/llm-on-premise/issues/5) | Eval: Gemma 4 as VIP model for advanced users | enhancement |
| [#6](https://github.com/Die-Spengergasse/llm-on-premise/issues/6) | Feat: LiteLLM user groups, access control, and model routing | enhancement |
| [#7](https://github.com/Die-Spengergasse/llm-on-premise/issues/7) | Eval: Super Gemma 4 26B Uncensored — VIP model with tool-calling fixes | enhancement |
