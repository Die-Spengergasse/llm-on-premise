# DOMAIN — llm-on-premise

## Schulkontext

- **Schule**: HTBLuVA Wien 5 Spengergasse, Spengergasse 20, 1050 Wien
- **Schüler**: 2.600 gesamt, ~2/3 in IT/Design-Abteilungen = ~1.700 potenzielle KI-Nutzer
- **Lehrer**: 280
- **Klassen**: 97 (laut eEducation-Daten)
- **Zielgruppe**: Schüler (Unterricht, Projekte), Lehrer (Vorbereitung, erweiterte Modelle), Administratoren (VIP-Zugriff)
- **Datenschutz**: DSGVO-kritisch – Verarbeitung personenbezogener Daten von Minderjährigen
- **Pädagogisches Ziel**: KI-Kompetenz vermitteln, KI als Werkzeug im Unterricht, Coding-Assistenz in Projekten

## Preise (Stand 2026-06-24)

### Hardware Einmalig
| Gerät | Speicher | Bandbreite | Preis |
|-------|----------|-----------|-------|
| AMD Strix Halo Mini PC | 96 GB unified | ~256 GB/s | ab $1.479 |
| Mac Mini M4 Pro | 48 GB unified | 273 GB/s | $1.799 |
| Mac Mini M4 Pro | 64 GB unified | 273 GB/s | ~$2.000 |
| Mac Studio M4 Max | 128 GB unified | 400–546 GB/s | ~€4.500 |
| Mac Studio M3 Ultra | 96 GB unified | 800 GB/s | ~€4.300 |
| Mac Studio M3 Ultra | 192 GB unified | 800 GB/s | ~€7.000 |
| AMD Strix Halo Dev Kit | 128 GB unified | ~256 GB/s | $3.999 |
| NVIDIA DGX Spark | 128 GB unified | 273 GB/s | ~€4.950 |
| 4× Mac Mini Pro (EXO) | 192 GB pooled | ~273 GB/s | ~$7.200 |

### GPU-Miete (laufend)
| Anbieter | GPU | Preis |
|----------|-----|-------|
| Hetzner GEX44 | RTX 4000 Ada 20 GB | €184/Monat |
| Hetzner GEX131 | RTX PRO 6000 96 GB | €889/Monat |
| Spheron H100 SXM spot | H100 80 GB | ab $1.03/h |
| Vast.ai | RTX 4090 | ab $0.35/h |
| Lambda | H100 | $2.49/h |

### API-Kosten pro Million Tokens
| Modell | Eingang | Ausgang |
|--------|---------|---------|
| SiliconFlow (günstigste Modelle) | $0.05 | – |
| DeepSeek V4 Flash | $0.14 | $0.28 |
| DeepSeek V4 Pro | $0.44 | $0.87 |
| Qwen 3.6-27B | $0.10 | $0.15 |
| GLM-5.2 | $1.40 | $4.40 |
| Gemini 3.1 Pro | $2.00 | $12.00 |
| Claude Opus 4.8 | $5.00 | $25.00 |
| GPT-5.5 | $5.00 | $30.00 |

### Education-Pläne
| Angebot | Kosten | Details |
|---------|--------|---------|
| ChatGPT Edu | ~$10/Sitz/Monat | OpenAI, DSGVO-Fragen offen |
| ChatGPT Go | $8/Monat | Werbefinanziert, US-only |
| ChatGPT Business | $20/Sitz/Monat | SOC 2 Type 2 |
| ChatGPT Enterprise | $60-80/Sitz/Monat | ab 150 Sitzen |
| Anthropic Claude for Education | individuell | API-Credits, Campus Ambassadors |
| OpenRouter | +5.5 % Aufschlag | 500+ Modelle, ein API-Key |

### Modelle auf Hardware (On-Premise, Stand 2026-06-24)

| Hardware | Läuft z.B. (Open Source) | Kern-Benchmarks |
|----------|--------------------------|-----------------|
| Mac Mini Pro 48 GB / Strix Halo 96 GB | Qwen 3.6-27B, MiniMax M3, Gemma 4 31B | SWE-bench V 77–80, TB 59, LiveCodeBench 80 |
| Mac Studio M4 Max 128 GB | GLM-5.2 (Q4), DeepSeek V4 Flash, Qwen 3.5 397B | SWE-bench Pro 62, GPQA 88, LiveCodeBench 94 |
| Mac Studio M3 Ultra 192 GB | GLM-5.2, DeepSeek V4 Pro, DeepSeek V4 Flash | SWE-bench V 81, LiveCodeBench 94, AIME 99 |
| GPU-Miete: H100 (80-96GB) | DeepSeek V4 Pro, GLM-5.2, Qwen 3.5 397B | SWE-bench V 81, SWE-bench Pro 62, GPQA 88 |
| GPU-Miete: RTX 4090 (24GB) | Qwen 3.6-27B (Q4), DeepSeek V4 Flash | SWE-bench V 77, TB 59 |

### OpenAI Codex (Coding-Agent)
| Plan | Kosten | Details |
|------|--------|---------|
| Codex (ChatGPT Business) | im Business-Seat enthalten | 2026-04-02 |
| Codex Pro | $20/Monat | 500 Codex-Agent-Aktionen |
| Codex Max | $60/Monat | 2.500 Aktionen |
| Codex API | $1.75/$14.00 MTok | GPT-5.3 Codex |

## Benchmarks (Stand Juni 2026)

### Coding
- **SWE-bench Pro** (Scale AI, echte Software-Bugs):
  - Claude Opus 4.8 (vendor): 69.2 %
  - GLM-5.2: 62.1 % (MIT-Lizenz, open weight)
  - GPT-5.5: 58.6 %
  - GPT-5.4: 59.1 %
- **SWE-bench Verified**:
  - Claude Fable 5: 95.0 % (gesperrt seit 2026-06-12)
  - Claude Opus 4.8: 88.6 %
  - GPT-5.3 Codex: 85.0 %
  - DeepSeek V4 Pro: 80.6 % (MIT-Lizenz)
  - MiniMax M3: 80.5 %
- **LiveCodeBench** (Competitive Programming):
  - DeepSeek V4 Pro: 93.5 % (#1 aller Modelle)
  - Kimi K2.6: 89.6 %
- **Terminal-Bench 2.1** (Shell-Agent):
  - Claude Opus 4.8: 85.0
  - GLM-5.2: 81.0 (open weight)
  - Gemini 3.1 Pro: unter 81.0

### Reasoning
- **GPQA Diamond** (Graduate-Level Science):
  - Qwen 3.5 397B: 88.4 (Apache 2.0)
- **AIME 2026** (Mathe-Olympiade):
  - GLM-5.2: 99.2 (MIT-Lizenz, closed source not disclosed)

### Gesamt-Scores
- **Artificial Analysis Intelligence Index**:
  - Top Closed: 57 (Anthropic, Google, OpenAI)
  - Kimi K2.6: 54 (#4 overall, best open)
  - MiMo-V2.5-Pro: 54 (tied #4)
  - DeepSeek V4 Pro: 52
- **BenchLM.ai Gesamt**:
  - GLM-5.2: 91/100 (#4 von 124 Modellen)
  - Design Arena: #1 weltweit

## Nutzungsmodell

- Schüler (Standard): Qwen 3.6-27B, Gemma 4, DeepSeek V4 Flash
- Lehrer/VIPs: GLM-5.2, DeepSeek V4 Pro
- Realistische Token-Nutzung: ~5.000 Tokens/Tag pro aktivem Nutzer
- ~680 aktive Nutzer (40 % von 1.700 IT-Schülern)
- 190 Schultage → ~646 Millionen Tokens/Jahr
- Auth: Schul-SSO + API-Tokens für Coding-Tools
