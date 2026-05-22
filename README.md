# LLM On-Premise — Spengergasse

On-premise LLM-Infrastruktur für die Spengergasse. Datenschutzkonforme
KI-Assistenten für Unterricht und Coding – betrieben auf schuleigenen
Servern im ZID-Rechenzentrum, ohne Abhängigkeit von externen Anbietern.

## Worum geht's?

Schüler und Lehrer der Spengergasse nutzen KI als Werkzeug: zum Chatten,
für Coding-Assistenz in Projekten und zur Recherche. Die gesamte
Infrastruktur läuft lokal – kontrolliert, kostengünstig, und ohne dass
Daten das Schulnetz verlassen.

Das Projekt ist offen angelegt. Beiträge und Feedback sind willkommen.

## Status

Aktuell in der Planungsphase. Hardware-Entscheidung noch offen.
→ Details in [Issue #2](https://github.com/Die-Spengergasse/llm-on-premise/issues/2),
[#5](https://github.com/Die-Spengergasse/llm-on-premise/issues/5) und
[#7](https://github.com/Die-Spengergasse/llm-on-premise/issues/7).

## Architektur (Überblick)

Eine zentrale Management-VM (LiteLLM + Open WebUI + SearXNG) ist der
einzige öffentlich erreichbare Einstiegspunkt. Die AI-Backend-Knoten
laufen in einem isolierten VLAN und sind nur über den Proxy erreichbar.

```
┌──────────────────────────────────────────────────────────┐
│ ZID Rechenzentrum                                        │
│                                                          │
│  Management VM (LiteLLM, Open WebUI, SearXNG)            │
│       │                  │              │                │
│       └──────────┬───────┴──────┬───────┘                │
│                  │ Internes VLAN │                        │
│          ┌───────┴───────┬───────┴───────┐                │
│       Backend #1     Backend #2     Backend #3            │
│       (vLLM)         (vLLM)         (vLLM)               │
│                                                          │
│  ← KEIN direkter Zugriff von außen →                     │
└──────────────────────────────────────────────────────────┘
                   │ Schulnetz / VLAN
         ┌─────────┼─────────────┐
      Schüler   Lehrer   Coding-Tools
```

## Software-Stack

| Komponente | Zweck |
|---|---|
| **LiteLLM** | API-Proxy, Routing, Rate Limiting, Logging |
| **Open WebUI** | Chat-Frontend für Schüler und Lehrer |
| **SearXNG** | Lokale Suchinstanz für RAG / Tool Use |
| **vLLM** | LLM-Serving mit Continuous Batching |

## Clients

Zugriff über **OpenAI-kompatible API** von LiteLLM:

| Client | Verwendung |
|---|---|
| **Open WebUI** | Browserbasierter Chat (Schul-SSO) |
| **OpenCode** | Terminal-Coding-Tool (API-Key) |
| **Kilo Code** | VS Code / Cursor-Erweiterung (API-Key) |
| **Beliebige OpenAI-Clients** | Weitere Tools |

## Budget

~€9.000 (3× NVIDIA DGX Spark) – Alternativen in Evaluierung.

## Nächste Schritte

- [#2](https://github.com/Die-Spengergasse/llm-on-premise/issues/2) DGX Spark mit vLLM konfigurieren
- [#3](https://github.com/Die-Spengergasse/llm-on-premise/issues/3) Management-VM aufsetzen
- [#4](https://github.com/Die-Spengergasse/llm-on-premise/issues/4) Network Hardening
- [#6](https://github.com/Die-Spengergasse/llm-on-premise/issues/6) LiteLLM Access Control
- [#7](https://github.com/Die-Spengergasse/llm-on-premise/issues/7) Gemma 4 Evaluation

## Links

- [GitHub Issues](https://github.com/Die-Spengergasse/llm-on-premise/issues)
- [Diskussionen](https://github.com/Die-Spengergasse/llm-on-premise/discussions)
