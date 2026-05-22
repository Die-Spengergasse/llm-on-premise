# Architecture

Living structural map of the system as of 2026-05-22.

## Overview

On-premise LLM-Infrastruktur für die Spengergasse. Eine Management-VM
(LiteLLM, Open WebUI, SearXNG) im ZID-Rechenzentrum dient als einziger
öffentlicher Einstiegspunkt. AI-Backend-Knoten (vLLM) laufen in einem
isolierten VLAN. Schüler und Lehrer greifen über Browser oder Coding-Tools
zu, authentifiziert über Schul-SSO.

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
