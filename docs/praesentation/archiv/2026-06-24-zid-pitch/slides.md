---
marp: true
size: 16:9
paginate: true
---

<style>
  section {
    background: white;
    color: #1a1a1a;
    font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
    padding: 30px;
  }
  h1 {
    color: #2563eb;
    font-size: 2em;
    margin: 0 0 10px 0;
  }
  h2 {
    color: #1a1a1a;
    font-size: 1.3em;
    margin: 0 0 10px 0;
  }
  table {
    font-size: 0.6em;
    border-collapse: collapse;
    width: 100%;
    margin: 5px 0;
  }
  th {
    background: #f3f4f6;
    font-weight: 600;
    padding: 4px 8px;
    border: 1px solid #d1d5db;
  }
  td {
    padding: 4px 8px;
    border: 1px solid #d1d5db;
  }
  .dim {
    color: #6b7280;
    font-size: 0.65em;
    margin-top: 8px;
  }
  .big {
    color: #2563eb;
    font-weight: 700;
    font-size: 2em;
  }
  ul {
    font-size: 0.85em;
    line-height: 1.4;
    margin: 5px 0;
    padding-left: 1.2em;
  }
  blockquote {
    color: #6b7280;
    font-style: italic;
    font-size: 0.85em;
    border-left: 3px solid #2563eb;
    padding-left: 10px;
    margin: 8px 0;
  }
</style>

<!-- 1 -->
# KI-Infrastruktur Spengergasse

Drei Wege – Daten, Preise, Entscheidungen

Georg Graf · 2026-06-24

---

<!-- 2 -->
## Kontext

**2.600 Schüler · 280 Lehrer · 97 Klassen**

Davon ~1.700 in IT/Design (potenzielle KI-Nutzer).
Aktive tägliche Nutzung: ~680 (40 %).

DSGVO als Grundanforderung.

Open-Source-LLMs haben den Abstand zu Closed Source von 17 auf 2–3 Prozentpunkte geschlossen (2023 → 2026).

---

<!-- 3 -->
## Open Source hat aufgeholt

| Benchmark | Open Source | Closed Source |
|-----------|-------------|---------------|
| SWE-bench Pro | **GLM-5.2** 62.1 (MIT) | GPT-5.5 58.6 |
| SWE-bench Verified | **DeepSeek V4 Pro** 80.6 | Claude Opus 4.8 88.6 |
| LiveCodeBench | **DeepSeek V4 Pro** 93.5 | GPT-5.3 Codex 85.0 |
| Terminal-Bench 2.1 | **GLM-5.2** 81.0 | Claude Opus 4.8 85.0 |
| GPQA Diamond | **Qwen 3.5** 88.4 | Claude Opus 4.6 ~85 |
| AIME 2026 | **GLM-5.2** 99.2 | – |

<div class="dim">LiveCodeBench: Open Source führt. Terminal-Bench: 4 Punkte Rückstand. Stand Juni 2026.</div>

---

<!-- 4 -->
## Preise & Lizenzen pro Million Tokens

| Modell | Eingang | Ausgang | Lizenz |
|--------|---------|---------|--------|
| GLM-5.2 | $1.40 | $4.40 | MIT |
| DeepSeek V4 Flash | $0.14 | $0.28 | MIT |
| DeepSeek V4 Pro | $0.44 | $0.87 | MIT |
| Qwen 3.6-27B | $0.10 | $0.15 | Apache 2.0 |
| SiliconFlow (günstigste) | $0.05 | – | offen |
| GPT-5.5 | $5.00 | $30.00 | – |
| Claude Opus 4.8 | $5.00 | $25.00 | – |

<div class="dim">Faktor 35–100x zwischen Open und Closed. Keine Lizenzkosten, keine MAU-Limits. Preise Stand 2026-06-24.</div>

---

<!-- 5 -->
## Vendor Lock-In ist real

<div class="big">12. Juni 2026</div>

US-Exportkontrolle sperrt Claude Fable 5 (SWE-bench 95.0 %) für alle Nicht-US-Nutzer. Über Nacht. Kein Ersatz.

**OpenAI:** 33 Modelle in einem Monat retired (Januar 2025).
**Anthropic:** Drittanbieter-Agents auf Pro/Max verboten (April 2026).
**Preise:** GPT-5.5 doppelt so teuer wie GPT-5.4. Keine Ankündigung.

> Geschlossene APIs: morgen teurer, morgen weg, morgen anders.

---

<!-- 6 -->
## Option A: On-Premise

Management-VM (LiteLLM + Open WebUI + SearXNG) + GPU-Knoten (vLLM)

| Hardware | Speicher | Preis |
|----------|----------|-------|
| AMD Strix Halo Mini PC | 96 GB unified | ab $1.479 |
| Mac Mini M4 Pro | 48 GB unified | $1.799 |
| Mac Mini M4 Pro | 64 GB unified | ~$2.000 |
| Mac Studio M4 Max | 128 GB unified | ~€4.500 |
| Mac Studio M3 Ultra | 96 GB unified | ~€4.300 |
| Mac Studio M3 Ultra | 192 GB unified | ~€7.000 |
| AMD Strix Halo Dev Kit | 128 GB unified | $3.999 |
| NVIDIA DGX Spark | 128 GB unified | ~€4.950 |
| 4× Mac Mini Pro (EXO) | 192 GB pooled | ~$7.200 |

<div class="dim">Strom: 40–300W pro Gerät. Alle mit vLLM, Ollama oder llama.cpp. Preise Stand 2026-06-24.</div>

---

<!-- 7 -->
## Open Source Modelle & Hardware

| Hardware | Läuft z.B. | Kern-Benchmarks |
|----------|------------|-----------------|
| Mac Mini Pro 48 GB / Strix Halo 96 GB | Qwen 3.6-27B, MiniMax M3, Gemma 4 31B | SWE-bench V 77–80, TB 59, LiveCode 80 |
| Mac Studio M4 Max 128 GB | GLM-5.2 (Q4), DeepSeek V4 Flash, Qwen 3.5 397B | SWE-bench Pr 62, GPQA 88, LiveCode 94 |
| Mac Studio M3 Ultra 192 GB | GLM-5.2, DeepSeek V4 Pro, DeepSeek V4 Flash | SWE-bench V 81, LiveCode 94, AIME 99 |

**Zum Vergleich (Closed Source):**
- Claude Opus 4.8: SWE-bench V 88.6, TB 85.0
- GPT-5.5: SWE-bench Pr 58.6
- Claude Opus 4.6: SWE-bench V 80.8

<div class="dim">Auf LiveCodeBench führt DeepSeek V4 Pro alle geschlossenen Modelle an (93.5).</div>

---

<!-- 8 -->
## Option A: Kosten

| Szenario | Jahr 1 | Jahr 2 | Jahr 3 |
|----------|--------|--------|--------|
| 1 Knoten + Management-VM | ~€4.000 | ~€500 | ~€500 |
| 3 Knoten (erweitert) | ~€12.000 | ~€1.500 | ~€1.500 |
| Vergleich: ChatGPT Edu (1.700 Sitz) | ~€204.000 | ~€204.000 | ~€204.000 |

<div class="dim">Break-even nach 2–3 Jahren. Danach nur noch Strom + Wartung.</div>

---

<!-- 9 -->
## Option B: GPU mieten

**EU-souverän – kein CLOUD Act:**

| Anbieter | GPU | Preis | Läuft z.B. |
|----------|-----|-------|------------|
| Hetzner GEX44 | RTX 4000 Ada 20 GB | €184/Monat | Qwen 3.6-27B, Gemma 4 31B |
| Hetzner GEX131 | RTX PRO 6000 96 GB | €889/Monat | DeepSeek V4 Flash, GLM-5.2 (Q4) |
| OVHcloud | H100 | ~$3.20/h | DeepSeek V4 Pro, GLM-5.2 |
| Gcore | H100 | ~$3.10/h | DeepSeek V4 Pro, GLM-5.2 |

**Neo-Clouds (günstiger, global):**

| Anbieter | GPU | Preis | Läuft z.B. |
|----------|-----|-------|------------|
| Spheron | H100 spot | ab $1.03/h | DeepSeek V4 Pro |
| Vast.ai | RTX 4090 | ab $0.35/h | Qwen 3.6-27B, DeepSeek V4 Flash |
| Lambda | H100 | $2.49/h | DeepSeek V4 Pro, GLM-5.2 |

<div class="dim">Hyperscaler (AWS, Azure, GCP): H100 ~$12–14/h. Preise Stand 2026-06-24.</div>

---

<!-- 10 -->
## Option C: API-Abos

**Realistisches Szenario:** 680 aktive Nutzer, 5.000 Tokens/Tag, 190 Schultage
→ **~646 Millionen Tokens/Jahr**

| Anbieter | Kosten/MTok | Kosten/Jahr |
|----------|-------------|-------------|
| SiliconFlow (günstigste) | $0.05 | **~€30** |
| DeepSeek V4 Flash | $0.14 / $0.28 | **~€270** |
| DeepSeek V4 Pro | $0.44 / $0.87 | **~€400** |
| GLM-5.2 (API) | $1.40 / $4.40 | **~€1.700** |
| ChatGPT Edu (1.700 Sitz) | ~$10/Sitz/Monat | **~€170.000** |

<div class="dim">Bei API-Kosten unter €500/Jahr stellt sich die On-Premise-Frage nicht mehr finanziell, sondern datenschutzrechtlich.</div>

---

<!-- 11 -->
## Vergleich

| Kriterium | On-Premise | GPU mieten | API-Abos |
|-----------|-----------|------------|----------|
| Kosten Jahr 1 | €4.000–12.000 | ~€2.000–7.000 | €30–204.000 |
| Kosten Jahr 3 | ~€500–1.500 | ~€2.000–7.000 | €30–204.000 |
| Datenschutz | vollständig | anbieterabhängig | extern |
| Modellauswahl | alle Open | alle | API-abhängig |
| Vendor Lock-In | keiner | gering | hoch |
| Wartung | selbst | gering | keine |

<div class="dim">API (Open-Source-Dienste): extrem günstig, aber Daten verlassen das Schulnetz.</div>

---

<!-- 12 -->
## Hardware-Trend

Preis pro Token fällt exponentiell. DRAM-Schock 2025/26 ist temporär.

<div class="big">2023 → 2026: GPU-Preis/Token<br>um Faktor 5–10 gefallen.</div>

**2027/28 zu erwarten:**
- Rubin-Generation drückt H100-Preise
- AMD MI400 + Intel Gaudi 3: mehr Wettbewerb
- DRAM-Kapazitäten hochgefahren
- MoE-Modelle effizienter (GLM-5.2: 5 % aktiv)

> Wer heute sparsam startet, kauft morgen günstiger ein.

---

<!-- 13 -->
## Ein möglicher Weg

**Phase 1 (2026/27):**
1 On-Premise-Knoten (Strix Halo / Mac Mini) + Management-VM
+ API für Massenlast (DeepSeek V4 Flash, ~€270/Jahr).
~€4.000 einmalig, ~€800/Jahr laufend.

**Phase 2 (2027/28):**
Hardware nachkaufen, wenn Preise fallen.
API-Anteil sinkt. ~€3.000–5.000 zusätzlich.

**Phase 3 (2028+):**
~90 % On-Premise. API nur für Spitzenlast.
Modelle von 2028 auf Hardware von 2026.

<div class="dim">Die API-Kosten in Phase 1 sind vernachlässigbar. Der Rest ist DSGVO und Souveränität.</div>

---

<!-- 14 -->
## Nächste Schritte

- Pilotklasse Q3 2026 – 1 Knoten + API
- Evaluierung nach einem Semester
- Hardware-Entscheidung auf Basis echter Daten
- Open-Source-Modelle evaluieren: GLM-5.2, DeepSeek V4, Qwen 3.6

---

<!-- 15 -->
## Danke

Georg Graf · grafg@spengergasse.at

github.com/Die-Spengergasse/llm-on-premise
