# LLM On-Premise — Spengergasse

On-premise LLM-Infrastruktur für die Spengergasse. Gemanagt über eine zentrale VM im ZID-Rechenzentrum mit LiteLLM, Open WebUI und SearXNG.

## Status: Planning

Die konkrete Hardware-Architektur ist noch offen. Zur Diskussion stehen u.a. NVIDIA DGX Spark, AMD Strix Halo, Multi-GPU-Workstation und weitere Optionen. Siehe [Architecture Decision Log](#architecture-decision-log) unten.

## Architektur

```
┌─────────────────────────────────────────────────────────┐
│  ZID Rechenzentrum                                      │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Management VM (einzige öffentlich erreichbare  │    │
│  │                   Komponente)                    │    │
│  │                                                 │    │
│  │  ┌───────────┐  ┌────────────┐  ┌───────────┐  │    │
│  │  │ LiteLLM   │  │ Open WebUI │  │ SearXNG   │  │    │
│  │  │ (Router / │  │ (Chat UI)  │  │ (Suche    │  │    │
│  │  │  Proxy)   │  │            │  │  für RAG) │  │    │
│  │  └─────┬─────┘  └──────┬─────┘  └─────┬─────┘  │    │
│  │        │               │              │         │    │
│  │  ┌─────┴───────────────┴──────────────┴──────┐  │    │
│  │  │  Auth (SSO / OAuth2 / Schul-IdM)          │  │    │
│  │  │  Token-Management für Schüler              │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └────────────────────┬────────────────────────────┘    │
│                       │ Internes VLAN ONLY              │
│          ┌────────────┼────────────┐                    │
│          │            │            │                    │
│     ┌────┴─────┐ ┌────┴─────┐ ┌───┴──────┐            │
│     │DGX Spark │ │DGX Spark │ │DGX Spark │            │
│     │  #1      │ │  #2      │ │  #3      │            │
│     │ 128 GB   │ │ 128 GB   │ │ 128 GB   │            │
│     └──────────┘ └──────────┘ └──────────┘            │
│                                                         │
│     ← KEIN direkter Zugriff von außen →                │
└─────────────────────────────────────────────────────────┘
                      │ Schulnetz / VLAN
          ┌───────────┼───────────┐
          │           │           │
       Schüler 1   Schüler 2   Schüler N
       (Browser)   (Browser)   (Browser)
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
| **LiteLLM** | API-Proxy, Routing, Rate Limiting, Token-Management, Logging |
| **Open WebUI** | Chat-Frontend für Schüler (browserbasiert) |
| **SearXNG** | Lokale Suchinstanz für RAG / Tool Use |
| **vLLM** | LLM-Serving auf allen DGX Sparks mit Continuous Batching |

## Modell-Belegung (exemplarisch)

Die Modellwahl hängt von der finalen Hardware ab. Aktueller Plan:

| Knoten | Modell | Task | RAM-Bedarf (Q4) |
|---|---|---|---|
| Backend #1 | Qwen3 30B | General + Coding (stark) | ~18 GB |
| Backend #2 | Devstral 24B | Coding-Fokus | ~14 GB |
| Backend #3 | Qwen3 14B | Schnelle Antworten, viele parallele Nutzer | ~8 GB |

## Request-Flow

```
Schüler (Browser)
    │ HTTPS (via Schul-SSO)
    ▼
Open WebUI          ← Chat-Oberfläche, Login
    │ API-Call (OpenAI-kompatibel)
    ▼
LiteLLM Proxy       ← Token-Auth, Rate Limiting, Routing, Logging
    │ Interner API-Call
    ▼
vLLM auf DGX Spark  ← Modell-Inferenz + Tool Use (SearXNG)
```

## Netzwerk

- DGX Sparks und Management VM stehen im ZID-Rechenzentrum (19"-Rack, Kühlung vorhanden)
- DGX Sparks sind **nicht öffentlich erreichbar** — nur die Management VM ist per Schul-URL zugänglich
- Interne Kommunikation über VLAN
- Auth über bestehende Schul-Infrastruktur (SSO / IdM)

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
| 2026-05-15 | Favorit: 3x NVIDIA DGX Spark | Under evaluation |
