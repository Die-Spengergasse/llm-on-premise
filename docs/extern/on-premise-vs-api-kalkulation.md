# On-Premise vs. Cortecs-API — Kalkulation für HTL Spengergasse

Erstellt: 2026-08-13
Kontext: 2.600 Schüler, 280 Lehrer, 97 Klassen (STATE.md), Budget ~€9.000
Zugehörig: Issue #14 (Token- und Auth-Konzept)
Siehe auch: `cortecs-provider-evaluation.md` (DSGVO-Tier-Klassifikation)

## Annahmen

### Token-Volumen (mittleres Szenario, 30 % aktive Nutzer)

| Parameter | Wert | Begründung |
|-----------|------|------------|
| Schüler total | 2.600 | STATE.md |
| Aktive Nutzer (30 %) | 780 | Rollout-Phase 1–2 |
| Output-Tokens/Anfrage | 500 | Realistische Chat-Antwort |
| Anfragen/Tag/Nutzer | 20 | Unterricht + Hausübungen |
| Schultage/Jahr | 200 | Österreichisches Schuljahr |
| Output/Jahr | ~78 Mrd | 780 × 500 × 20 × 200 |
| Input/Output-Verhältnis | 1:2 | Input ~250 Tok/Anfrage |
| Input/Jahr | ~39 Mrd | |
| Output/Monat (Ø) | ~325 Mio | 78 Mrd / 240 |
| Input/Monat (Ø) | ~163 Mio | 39 Mrd / 240 |

### Token-Preise (Cortecs, geschätzt mit EU-Aufschlag)

| Modell | Input/Mio | Output/Mio | Quelle |
|--------|-----------|------------|--------|
| DeepSeek V4 Flash (direkt) | $0,14 | $0,28 | DeepSeek API |
| DeepSeek V4 Flash (Cortecs, +40 % geschätzt) | $0,20 | $0,40 | Annahme für Kalkulation |
| Claude Opus 4.8 (Cortecs) | ~$15 | ~$75 | Anthropic + Aufschlag |
| OpenRouter (Tier 3) | $0,0679 | $0,168 | openrouter.ai (nicht empfohlen) |

> Preise vor Vertrag mit Cortecs verifizieren — siehe
> `cortecs-anfrage-email-draft.md`. EU-Aufschlag realistisch +30–50 %.

## Kostenkalkulation Cortecs-API (DeepSeek V4 Flash, mittleres Szenario)

| Posten | Volumen/Monat | Preis/Mio | Kosten/Monat |
|--------|---------------|-----------|--------------|
| Output | 325 Mio | $0,40 | $130 |
| Input | 163 Mio | $0,20 | $33 |
| **Total/Monat** | | | **~$163** |
| **Total/Jahr** | | | **~$1.960** |
| **Total/3 Jahre** | | | **~$5.880 (~€5.400)** |

### Drei-Szenarien-Tabelle

| Szenario | Aktive Nutzer | Output/Monat | Kosten/Monat | Kosten/Jahr | Kosten/3J |
|----------|--------------|-------------|--------------|-------------|-----------|
| Konservativ (10 %) | 260 | 108 Mio | ~$55 | ~$660 | ~€1.820 |
| **Mittel (30 %)** | **780** | **325 Mio** | **~$163** | **~$1.960** | **~€5.400** |
| Hoch (50 %) | 1.300 | 542 Mio | ~$270 | ~$3.240 | ~€8.950 |
| Voll (100 %, unrealistisch) | 2.600 | 2.167 Mio | ~$1.083 | ~$13.000 | ~€35.900 |

## Kostenkalkulation On-Premise (Framework Desktop Strix Halo 128 GB)

### Hardware

| Posten | Preis | Quelle |
|--------|-------|--------|
| Framework Desktop (Ryzen AI Max+ 395, 128 GB unified) | ~$1.999 (~€1.850) | localaimaster.com |
| SSD 4 TB | ~€300 | |
| Rack/Halterung, Netzwerk | ~€100 | |
| **Hardware total** | **~€2.250** | |

### Betriebskosten (3 Jahre)

| Posten | Berechnung | Betrag |
|--------|------------|--------|
| Hardware (abgeschrieben über 3J) | | €2.250 |
| Strom (90 W × 12h × 220 Tage × €0,25/kWh × 3J) | 90 × 12 × 220 × 0,25 × 3 / 1000 | ~€178 |
| IT-Stundenaufwand (2h/Wo × 40 Wo × 3J × €50) | 2 × 40 × 3 × 50 | ~€12.000 |
| Wartung (Updates, Treiber, ollama/vLLM) | | ~€1.500 |
| **Total/3 Jahre** | | **~€15.930** |
| **Ø/Jahr** | | **~€5.310** |

### Was auf 128 GB unified memory läuft

| Modell | Speicherbedarf | Q3 (110 GB) | Q4 (155 GB) | Q8 lossless (162 GB) |
|--------|---------------|-------------|-------------|---------------------|
| DeepSeek V4 Flash | | ✓ | ✗ (Offload) | ✗ |
| Llama 3.3 70B Q4 | ~40 GB | ✓ | ✓ | ✓ |
| Llama 3.3 70B BF16 | ~140 GB | ✓ | ✓ | ✓ |
| Qwen 3.6 32B Q4 | ~18 GB | ✓ | ✓ | ✓ |

**Wichtig:** DeepSeek V4 Flash **lossless (Q8) ist auf 128 GB nicht möglich**
(bräuchte Mac Studio M5 Max 192 GB, ~€5.500+). Mit Q3 (~110 GB) läuft es,
aber mit messbarem Qualitätsverlust — siehe PITFALLS.md / Quantization-Tabelle
unten.

### DeepSeek V4 Flash — Quantisierungs-Übersicht (Unsloth, Aug 2026)

| Quant | Größe | Speicherbedarf | Verlust |
|-------|-------|----------------|---------|
| Q8 (UD-Q8_K_XL) — lossless | 162 GB | ~169 GB | ~0 (verlustfrei) |
| Q4 (UD-Q4_K_XL) — near lossless | 155 GB | ~162 GB | praktisch verlustfrei (KLD 0.010) |
| Q3 (IQ3_XXS) | 103 GB | ~110 GB | gering–mittel |
| Q2 (IQ2_XXS) | ~87 GB | ~92–102 GB | deutlich (KLD ~0.41) |

→ Auf 128 GB Strix Halo läuft DeepSeek V4 Flash nur als **Q3** (110 GB) —
   Qualität leicht reduziert, aber für Coding/Chat brauchbar.
   Lossless (Q8) erst ab Mac Studio M5 Max 192 GB (~€5.500+).

### Durchsatz (Strix Halo, 70B Q4, 32 tok/s)

- Bei 32 tok/s: 1.920 tok/min → ~4 Schüler parallel bei 500-Tok-Antworten
- Bei mehreren parallelen Schülern bricht throughput ein (256 GB/s Bandbreite
  limitiert Batching vs. discrete GPU ~1.000 GB/s)
- **Für Vollbetrieb einer Klasse (25 Schüler parallel) nicht geeignet**

## Vergleichstabelle On-Prem vs. Cortecs (mittleres Szenario, 3 Jahre)

| Aspekt | On-Prem (Strix Halo) | Cortecs API |
|--------|---------------------|-------------|
| Hardware-Investition | €2.250 | €0 |
| Betriebskosten 3J | €13.680 | €5.400 |
| **Total 3 Jahre** | **~€15.930** | **~€5.400** |
| Ø/Jahr | ~€5.310 | ~€1.800 |
| Modellqualität | Mittel (70B Q4, Flash Q3) | Hoch (Flash lossless, Claude) |
| DSGVO/EU-Residency | ✓ (lokal, bestmöglich) | ✓ (Cortecs garantiert) |
| Skalierung bei Klassen | ❌ (32 tok/s limit) | ✓ (beliebig) |
| Frontier-Modelle (Claude/GPT-5) | ❌ nicht verfügbar | ✓ |
| Ausfall/Wartung | IT-Mitarbeiter belastet | Provider-SLA |
| Upgrade auf neues Modell | Neuinvestition | sofort verfügbar |
| Internet-Unabhängigkeit | ✓ (voll autark) | ✗ |

## Empfehlung: Drei-Säulen-Modell

### Säule 1: On-Prem für DSGVO-kritische Daten

- **Framework Desktop Strix Halo 128 GB (~€2.250)**
- Läuft: DeepSeek V4 Flash Q3, Llama 3.3 70B, Qwen 3.6
- Einsatz: Klausuren, schülerbezogene Daten, DSGVO-kritische Verarbeitung
- Backup für Internet-Ausfälle (volle Autarkie)

### Säule 2: Cortecs-Vertrag für Massenlast + Frontier-Modelle

- DeepSeek V4 Flash lossless (Q8), Claude Opus, GLM-5.2 etc.
- Budget: ~€1.800/Jahr (mittleres Szenario)
- Einsatz: regulärer Unterricht, Projekte, Coding-Assistenz
- Kein Hardware-Risiko, kein Personalbedarf

### Säule 3: Phasen-Strategie (DECISIONS.md 2026-06-24, beibehalten)

- Phase 1 (2026/27): API-lastig (Cortecs) + Dev-Rig gregor
- Phase 2 (2027/28): Strix Halo als On-Prem-Backend; bei fallenden Preisen
  Mac Studio M5 Max 192 GB ergänzen (für Q8-lossless DeepSeek V4 Flash)
- Phase 3 (2028+): autark mit breiterer Hardware-Basis

## Aktualisierte Hardware-Empfehlung

**Stärkung der bestehenden DECISIONS.md-Entscheidung** (2026-06-24):
Hardware-Favorit „Apple Mac Mini Pro + AMD Strix Halo":

- **Framework Desktop Strix Halo 128 GB (~€1.850)** bestätigt als günstigste
  realistische On-Prem-Option. Läuft DeepSeek V4 Flash Q3 (110 GB) und
  Llama 3.3 70B Q4 (40 GB) — letzteres als BF16 sogar lossless.
- **Mac Mini M5 Pro (24–48 GB unified)** — verworfen für DeepSeek V4 Flash:
  zu wenig VRAM (Flash Q3 braucht 110 GB). Nur für kleine Modelle brauchbar.
- **Mac Studio M5 Max 192 GB (~€5.500+)** wäre Alternative für Q8-lossless
  DeepSeek V4 Flash — außerhalb 9K-Budget für erstes Setup, aber in Phase 2
  als Ergänzung vorgemerkt.
- **DGX Spark (€4.950)** — bestätigt zu teuer für Einstieg (bereits
  DECISIONS.md 2026-06-24 so festgelegt).

## Quellen

- localaimaster.com/blog/strix-halo-ai-max-395-guide (Preis, Benchmarks, 128 GB unified)
- maccompute.com/blog/articles/2026-mac-mini-m5-release-date-price-full-specs.html
- pricepertoken.com/pricing-page/model/deepseek-deepseek-v4-flash (API-Preise)
- openrouter.ai/deepseek/deepseek-v4-flash (OpenRouter-Preis)
- unsloth.ai/docs/models/deepseek-v4 (Quantisierungs-Tabelle)
- cortecs.ai/aboutUs (EU-souveran, ISO 27001, DPA, No-Training)
- Siehe `cortecs-provider-evaluation.md` für vollständige Provider-Klassifikation
