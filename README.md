# LLM On-Premise — Spengergasse

On-premise LLM-Infrastruktur für die Spengergasse. Drei NVIDIA DGX Spark Knoten mit 128 GB Unified Memory, gemanagt über eine zentrale VM mit LiteLLM, Open WebUI und SearXNG.

## Status: Planning

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
│     │ Qwen3   │ │ Devstral │ │ Qwen3   │            │
│     │ 30B      │ │ 24B      │ │ 14B      │            │
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

| Komponente | Spezifikation |
|---|---|
| **DGX Spark #1** | NVIDIA DGX Spark, 128 GB Unified Memory, ~273 GB/s |
| **DGX Spark #2** | NVIDIA DGX Spark, 128 GB Unified Memory, ~273 GB/s |
| **DGX Spark #3** | NVIDIA DGX Spark, 128 GB Unified Memory, ~273 GB/s |
| **Management VM** | ZID-Infrastruktur, ~4 vCPU, 8 GB RAM, 50 GB Disk |

## Software-Stack

| Komponente | Zweck |
|---|---|
| **LiteLLM** | API-Proxy, Routing, Rate Limiting, Token-Management, Logging |
| **Open WebUI** | Chat-Frontend für Schüler (browserbasiert) |
| **SearXNG** | Lokale Suchinstanz für RAG / Tool Use |
| **vLLM** | LLM-Serving auf allen DGX Sparks mit Continuous Batching |

## Modell-Belegung

| Knoten | Modell | Task | RAM-Bedarf (Q4) |
|---|---|---|---|
| DGX Spark #1 | Qwen3 30B | General + Coding (stark) | ~18 GB |
| DGX Spark #2 | Devstral 24B | Coding-Fokus | ~14 GB |
| DGX Spark #3 | Qwen3 14B | Schnelle Antworten, viele parallele Nutzer | ~8 GB |

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
| 3x NVIDIA DGX Spark 128 GB | ~€9.000 |
| Management VM | ZID-Infrastruktur (keine Extrakosten) |
| **Gesamt** | **~€9.000** |
