# Cortecs-Anfrage — E-Mail-Entwurf

Erstellt: 2026-08-13
An: enterprise@cortecs.ai
Betreff: Anfrage Bildungseinrichtung — LLM-API für HTL Spengergasse

---

Betreff: Anfrage Bildungseinrichtung — LLM-API für HTL Spengergasse

Sehr geehrtes Cortecs-Team,

die HTL Spengergasse (Wien, ~2.600 Schüler, 280 Lehrer, 97 Klassen) baut
aktuell eine hybride LLM-Infrastruktur auf (On-Premise + API) und evaluiert
EU-souverane Provider als Alternative zu direkten China-basierten APIs
(DeepSeek, SiliconFlow).

Cortecs ist aufgrund der EU-native-Cloud-Infrastruktur, ISO 27001-Zertifizierung
und DSGVO-by-default für uns ein bevorzugter Kandidat. Details zur Evaluation
finden Sie unter `docs/extern/cortecs-provider-evaluation.md` (ggf. auf Anfrage).

Wir würden gerne folgende Punkte klären:

## 1. Bildungs-/Schul-Rabatt

Gibt es ein spezielles Pricing für öffentliche Bildungseinrichtungen
(HTL, nicht kommerziell, Bundesschule)?

## 2. Modellangebot und Preise

Bitte Angebot für folgende Modelle (pro Mio Tokens, Input/Output):

- DeepSeek V4 Flash
- GLM-5.2
- Qwen 3.6
- Optional: Claude Opus 4.8, GPT-5.6

## 3. DPA und Auftragsverarbeitung

Bitte DPA-Dokument für Unterzeichnung seitens der Schule /
des Schulträgers (BM für Bildung).

## 4. Datenlöschung und Aufbewahrung

Welche Standard-Aufbewahrungsfristen gelten für API-Inputs/Outputs?
Ist Zero-Data-Retention möglich?

## 5. Volumen-Kalkulation

Grobe Schätzung (mittleres Szenario): ~325 Mio Output-Tokens/Monat
(bei 30 % aktiver Schüler). Skalierung auf 100 % aktiv (~2,2 Mrd/Monat)
im Worst-Case. Details siehe `docs/extern/on-premise-vs-api-kalkulation.md`.

## 6. Auth-Integration

Support für LiteLLM-kompatibles Routing (OpenAI-API-Format)?
Virtual-Keys / Rate-Limits pro Schülergruppe möglich?

## 7. Test-Phase

Könnten wir einen 30-tägigen Pilot-Zugang für 1–2 Klassen erhalten?

## 8. Rechnungsstellung

Mögliche Rechnungsstellung auf österreichische öffentliche Schule?
(UID-pflichtig, Rechnungsadresse: HTL Spengergasse, 1050 Wien)

Kontakt:
Georg Graf, graf@spengergasse.at
HTL Spengergasse, Spengergasse 20, 1050 Wien

Mit freundlichen Grüßen,
Georg Graf

---

## Verwendungs-Hinweis

Dieser Entwurf ist eine Vorlage. Vor Versand:
- [ ] Aktuelle Schülerzahl / Schultage verifizieren
- [ ] Konkrete Modellpreise (falls von Cortecs vorab genannt) einsetzen
- [ ] Schul-UID / Rechnungsadresse offiziell bestätigen
- [ ] Mit Direktion / IT-Leitung abstimmen
