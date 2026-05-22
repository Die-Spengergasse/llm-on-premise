# Architecture

Living structural map of the system as of 2026-05-22.

## Overview

On-premise LLM-Infrastruktur für die Spengergasse. Die Management-VM
(LiteLLM, Open WebUI, SearXNG) ist der einzige Einstiegspunkt für
Clients aus dem Schulnetz. AI-Backend-Knoten (vLLM) laufen isoliert
und sind ausschließlich über die Management-VM erreichbar.

```
                    ╔══════════════════════════════════════╗
                    ║         ZID Rechenzentrum            ║
                    ║                                      ║
                    ║ ┌─────────┐ ┌─────────┐ ┌─────────┐ ║
                    ║ │vLLM #1  │ │vLLM #2  │ │vLLM #3  │ ║
                    ║ └────┬────┘ └────┬────┘ └────┬────┘ ║
                    ║      │           │           │      ║
                    ║ ═════╧═══════════╧═══════════╧═══   ║
                    ║ ← KEIN direkter Zugriff von außen   ║
                    ║ ═════╤═══════════╤═══════════╤═══   ║
                    ║      │           │           │      ║
                    ║ ┌────┴───────────┴───────────┴────┐ ║
                    ║ │         Management VM            │ ║
                    ║ │ LiteLLM + Open WebUI + SearXNG  │ ║
                    ║ └───────────────┬─────────────────┘ ║
                    ╚═════════════════╬════════════════════╝
                                      ║
                                 HTTPS (Schul-SSO / API-Key)
                                      ║
              ┌───────────────────────╬───────────────────────┐
              │                       ║                       │
              │                 Schulnetz / VLAN                │
              │                       ║                       │
         ┌────┴────┐           ┌──────┴──────┐          ┌────┴────┐
         │ Schüler │           │    Lehrer    │          │ Coding- │
         ├─────────┤           ├──────────────┤          │  Tools  │
         │ Browser │           │   Browser    │          ├─────────┤
         │Coding-T.│           │  Coding-T.   │          │API-Key  │
         └─────────┘           └──────────────┘          └─────────┘
```

## Knowledge Files (`docs/ai/`)

| File | Purpose | Update mode |
|------|---------|-------------|
| HANDOFF.md | Offene Aufgaben für nächste Sitzung | Overwrite |
| DECISIONS.md | Chronologische Aufzeichnung von Entscheidungen | Append |
| ARCHITECTURE.md | Living structural map | Overwrite |
| CONVENTIONS.md | Laufende Regeln zur Befolgung | Append |
| PITFALLS.md | Fallstricke und nicht-offensichtliche Fehler | Append |
| DOMAIN.md | Schulische/Bildungs-Domänenregeln | Append |
| STATE.md | Aktueller Projektstatus | Overwrite |

## Data Flows

- Schüler/Lehrer → Browser/IDE → Open WebUI / Direct API → LiteLLM Proxy → vLLM Backend → SearXNG (Tool Use)
- Auth: Schul-SSO → LiteLLM JWT → API-Token für Coding-Tools
- Management-VM ↔ Backend-Knoten: interner API-Call über VLAN (kein direkter Zugriff von außen)
