# Cortecs — Provider-Evaluation für HTL Spengergasse

Erstellt: 2026-08-13
Kontext: DSGVO-konforme Alternative zu direkten China-basierten LLM-APIs
(DeepSeek, SiliconFlow, Kimi, GLM) — siehe PITFALLS.md „China-Datenschutz".

## Zusammenfassung

Cortecs (Cortecs GmbH, Wien) ist ein EU-souveräner LLM-Router, der als
**Tier-1-DSGVO-Anbieter** die China-Datenschutz-Problematik von DeepSeek/GLM/Kimi
löst. Empfohlen als API-Partner für Massenlast und Frontier-Modelle, ergänzend
zur On-Premise-Infrastruktur (Drei-Säulen-Modell, siehe
`on-premise-vs-api-kalkulation.md`).

## DSGVO-Klassifikation: Tier 1 (EU-souverän)

| Kriterium | Ausprägung |
|-----------|-----------|
| Hosting | EU-native Clouds (Scaleway, OVH, IONOS, Infercom, Nebius, StackIt) |
| Datenlokalität | Daten verlassen nie Europa |
| EU-Residency | Garantiert, auch bei proprietären Modellen (die nicht auf EU-native Clouds gehostet sind) |
| DPA (Auftragsverarbeitung) | Verfügbar (cortecs.ai/dpa) |
| ISO 27001 | Zertifiziert (cortecs.ai/docs/ISO_27001_Certificate.pdf) |
| Training auf Kundendaten | Nein (per Policy, über Filter optional sicherstellbar) |
| GDPR-by-default | Ja |
| Standort | Althanstraße 4, 1090 Wien, Österreich |
| Ansprechpartner | enterprise@cortecs.ai (Schul-/Bildungs-Anfragen), support@cortecs.ai |

## Modellangebot (Beispiele, Stand Aug 2026)

Cortecs routet zu vielen Modellen — inkl. EU-gehosteter Varianten von Modellen,
deren Hersteller ursprünglich in China ansässig sind (DeepSeek, GLM, Kimi).
Konkrete Modellliste via `cortecs.ai/serverlessModels` bzw. `docs.cortecs.ai`.

- DeepSeek V4 Flash (EU-gehostet statt China-Direct-API)
- DeepSeek V4 Pro
- GLM-5.2
- Qwen 3.6
- Claude / GPT / Gemini (proprietär, aber EU-Residency garantiert)
- Mistral

## Preisrichtwerte

Siehe `on-premise-vs-api-kalkulation.md` für die vollständige Volumenrechnung.
Richtwerte pro Mio Tokens (geschätzt, inkl. EU-Aufschlag von +30–50 %):

| Modell | Input/Mio | Output/Mio | Quelle |
|--------|-----------|------------|--------|
| DeepSeek V4 Flash (Direkt-API) | $0,14 | $0,28 | api-docs.deepseek.com |
| DeepSeek V4 Flash (Cortecs, geschätzt +40 %) | ~$0,20 | ~$0,40 | Annahme für Kalkulation |
| DeepSeek V4 Flash (OpenRouter) | $0,0679 | $0,168 | openrouter.ai (Tier 3, nicht empfohlen) |

> Preise vor Vertrag mit Cortecs verifizieren — siehe
> `cortecs-anfrage-email-draft.md`.

## DSGVO-Tier-Vergleich (vollständige Klassifikation, Stand Aug 2026)

### Tier 1 — EU-souverän (Beste Wahl)

- **Cortecs** ★★★★★ — EU-native Clouds, ISO 27001, DPA, No-Training, Wien
- **Azure OpenAI** ★★★★★ — EU-Regionen (Schweden/Frankreich), 72h-Breach-SLA,
  Microsoft-DPA von EU-Aufsichtsbehörden anerkannt, kein Training auf API-Daten

### Tier 2 — DPA mit SCCs, aber US-Hosting

- **Anthropic (Claude API)** ★★★ — GDPR-DPA, kein Training auf API-Daten, SCCs
  für EU→US, 30 Tage Retention. Aber: keine EU-Residency (US-Verarbeitung), nur
  „prompt notice" bei Breach (nicht 72 h).
- **OpenAI (direkte API)** ★★★ — GDPR-DPA, kein Training, SCCs, Zero-Data-
  Retention-Option (ZDR). Aber: US-Verarbeitung, „prompt notice" Breach.
- **Together AI** ★★★★ — Bietet EU-Region-VPC-Deployments für GDPR-Kunden; DPA
  verfügbar. Standard-Default ist US — EU muss aktiv konfiguriert werden.
- **Fireworks AI** ★★★ — DPA mit SCCs (referenziert EU-GDPR + Schweizer FADP),
  US-basiert mit Transfer-Mechanismus. Keine direkte EU-Residency-Garantie.

### Tier 3 — Intermediär / Weiterleitung

- **OpenRouter** ★★★ — Router, der an viele Downstream-Modelle weiterleitet.
  Hat GDPR-Bewusstsein, aber die DSGVO-Konformität hängt am jeweiligen
  Downstream-Provider (möglicherweise US- oder China-Hoster, die trainieren).
  DPA pro Model-Provider prüfen!

### Tier 4 — Nicht DSGVO-konform / hohes Risiko

- **DeepSeek API (direkt)** ★ — China-basiert, speichert EU-Nutzerdaten auf
  chinesischen Servern, kein EU-Controller/Zwischenhändler, chinesische Entität
  ist alleiniger Verantwortlicher. Schwerer GDPR-Transfer-Risiko (Art. 44–49);
  italienische Aufsicht (Garante) hat DeepSeek gesperrt.
  Für EU-Personenbezogene Daten nicht empfehlbar.
- SiliconFlow, Kimi, direkte GLM-API — analog: chinesische Anbieter, Tier 4.

## Kontrast zu Direct-DeepSeek-API

Direkt-APIs von DeepSeek/SiliconFlow/Kimi/GLM sind Tier 4 (nicht DSGVO-konform):

- Daten werden auf chinesischen Servern gespeichert
- Kein EU-Controller/Zwischenhändler; chinesische Entität ist alleiniger
  Verantwortlicher ab Erfassung
- GDPR-Transfer-Risiko (Art. 44–49): kein Angemessenheitsbeschluss für China
- Italienische Aufsichtsbehörde (Garante) hat DeepSeek gesperrt
- Keine SCCs, keine EU-Aufsicht durchsetzbar

**Lösung via Cortecs:** Derselbe Modell-Typ (DeepSeek V4 Flash) wird von Cortecs
auf EU-native Clouds gehostet → DSGVO-Controller ist Cortecs GmbH (Wien) → DPA
schließbar → EU-Aufsicht durchsetzbar → Daten verlassen nie Europa.

## Integration in LiteLLM

Cortecs ist OpenAI-API-kompatplementär → direkter LiteLLM `model_list`-Eintrag.
Beispiel-Config (schematisch):

```yaml
model_list:
  - model_name: cortecs/deepseek-v4-flash
    litellm_params:
      model: openai/deepseek-v4-flash
      api_base: https://api.cortecs.ai/v1
      api_key: os.environ/CORTECS_API_KEY
```

Virtual-Keys (Issue #6, #14) können pro Schülergruppe Caps setzen
(z. B. $5/Schüler/Monat) — siehe `on-premise-vs-api-kalkulation.md`.

## Kontakte

- enterprise@cortecs.ai — Bildungs-/Schul-Anfragen, DPA, Rabatt-Verhandlung
- support@cortecs.ai — Support
- status.cortecs.ai — Status-Page
- cortecs.ai/aboutUs — Unternehmens-Self-Service

## Quellen

- cortecs.ai/aboutUs (EU-Sovereign, GDPR, ISO 27001, No-Training, Multi-Cloud)
- euro-stack.com/solutions/cortecs (EU sovereign cloud deployment)
- aipolicydesk.com/blog/anthropic-vs-openai-gdpr-compliance-2026 (Tier-Klassifikation)
- complydog.com/blog/is-deepseek-gdpr-compliant (DeepSeek Tier 4)
- docs.cortecs.ai (API-Dokumentation)
