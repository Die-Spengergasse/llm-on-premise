# llm-on-premise — Spengergasse

<!--
  Template for new opencode projects.
  How to use:
    1. Copy this file as AGENTS.md into your project root
    2. Fill in placeholders (<PROJECT_NAME>, <OWNER>, etc.)
    3. Symlink or copy opencode-helpers skills & commands:
       ln -s /path/to/opencode-helpers/skills skills
       ln -s /path/to/opencode-helpers/commands commands
       ln -s /path/to/opencode-helpers/docs/ai docs/ai
    4. In opencode, run: /init
    5. The agent reads this file and sets up the rest.

  A full opencode-helpers checkout is at:
  https://github.com/georgernstgraf/opencode-helpers
-->

## Project Identity

On-premise LLM-Infrastruktur für die Spengergasse – datenschutzkonforme
KI-Assistenten für Unterricht und Coding mit LiteLLM, Open WebUI,
SearXNG und vLLM auf schuleigenen Servern.

## Knowledge Bootstrap

Before starting any task, read the following files in order:

1. `docs/ai/HANDOFF.md` ← **read first, act on it**
2. `docs/ai/CONVENTIONS.md`
3. `docs/ai/DECISIONS.md`
4. `docs/ai/ARCHITECTURE.md`
5. `docs/ai/PITFALLS.md`
6. `docs/ai/STATE.md`
7. `docs/ai/DOMAIN.md` (if task involves business logic)

If the user says "continue", "resume", or "finish where we left off":
read and act on HANDOFF.md immediately without asking clarifying questions.
If HANDOFF.md contains open tasks, complete them before starting any new
work unless the user explicitly says otherwise.

## Skill Triggers

The following skills have NO slash commands. Invoke them by natural language:

**Knowledge Persistence** — when the user says:
  "remember", "merke dir", "don't forget", "behalte das im Kopf",
  "merk dir das", "save context", "persist knowledge"
  → load and execute the `knowledge-persistence` skill

**Issue Workflow** — when the user says:
  - start: "issue start", "start issue", "begin issue", "neues issue",
           "ich arbeite an"
  - commit: "issue commit", "commit issue", "speichere issue", "checkpoint"
  - finish: "issue commit and push", "finish issue", "issue done",
            "issue fertig", "schließe issue"
  → parse intent (start/commit/finish) and load the `issue-workflow` skill
    with the corresponding mode.

## Tech Stack

- LiteLLM (API-Proxy, Routing, Rate Limiting)
- Open WebUI (Chat-Frontend)
- SearXNG (Lokale Suchinstanz für RAG / Tool Use)
- vLLM (LLM-Serving mit Continuous Batching)
- Docker Compose (Management-VM)
- NVIDIA DGX Spark / AMD Strix Halo (Backend-Hardware, in Evaluierung)

## Repository

- GitHub: Die-Spengergasse/llm-on-premise
- Issue tracker: GitHub Issues

## Key Contacts

- Owner: Georg Graf <grafg@spengergasse.at>

## Development Environment

- Management-VM Docker Compose (LiteLLM + Open WebUI + SearXNG)
- vLLM auf Backend-Knoten
- GitHub Issues für Task-Tracking
- opencode issue-workflow für issue-gebundene Commits
