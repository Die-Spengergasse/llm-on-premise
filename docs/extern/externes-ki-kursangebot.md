# Externes KI-Kursangebot (pup-consulting.at)

## Hintergrund

Externes Angebot der **pup-consulting.at** für ein praxisorientiertes KI-Kursmodul
an der Spengergasse, eingebracht in der Planungsrunde am 2026-07-01. Kernforderung:
KI in der technischen Ausbildung nicht nur als Anwendungs- und Prompting-Thema zu
begreifen, sondern bis zur domänenspezifischen Anpassung eigener Modelle zu führen.

## Fachliche Einordnung

Das Angebot übersetzt sich in vier fachliche Felder:

| Feld | Bedeutung |
|---|---|
| Model-Based Systems Engineering (MBSE) | Systeme werden über fachspezifische Modellsprachen (SysML v2, UML) beschrieben und in Programme überführt; KI beschleunigt Modellierung & Code-Generierung. |
| Domänenspezifische KI-Anpassung | Anpassung offener Basismodelle an eine Fachdomäne, typischerweise via Fine-Tuning (LoRA/QLoRA) oder RAG. |
| ML/DL-Tiefe | Verständnis der Algorithmen statt reiner Anwendung („mehr als Prompting"). |
| Souveränität / Unabhängigkeit | Verringerung der Abhängigkeit von US-/chinesischen Anbietern durch Open-Source-Modelle und On-Premise-Betrieb. |

## Vergleichbare bestehende Angebote

| Anbieter | Kurs | Dauer | Preis | Zielgruppe |
|---|---|---|---|---|
| Caltech CTME | AI-Assisted MBSE (Generative AI-Driven Models) | 24 h | ~1.950 $ | erfahrene Systems Engineers |
| oose (Hamburg) | Introduction to AI Assisted MBSE with SysML v2 | 2 Tage | 1.650 € | Einsteiger |
| NobleProg | AI Assisted MBSE with SysML | 3 Tage (21 h) | ~5.500 $ (Online) / ~7.300 $ (Classroom) | Systems/Software Engineers |

Gemeinsamer Kern: SysML-v2-Modellierung + ChatGPT/Cameo, KI-gestützte
Requirements-/Architektur-/Code-Generierung (Embedded C, DB, UI).

## Bezug zum llm-on-premise-Projekt

Der Aspekt **Souveränität/Unabhängigkeit** wird durch das llm-on-premise-Projekt
bereits abgedeckt (Open-Source-Modelle GLM-5.2/DeepSeek V4/Qwen 3.6,
DSGVO-konformer On-Premise-Betrieb, hybrider Ansatz). Ein potenzieller Mehrwert
eines externen Moduls läge daher primär in den Feldern **MBSE** und
**domänenspezifische Fine-Tuning/RAG**.

## Offene Fragen (zu klären)

1. **Werkzeug & Beispielsystem** – Modellierungstool (Cameo, Papyrus, Eigenentwicklung)? Konkretes Beispielsystem + funktionierendes Pilot-Beispiel?
2. **Tiefe der KI-Anpassung** – Fine-Tuning (LoRA/QLoRA) oder RAG? Welches offene Basismodell?
3. **Know-how & Daten** – Lösung des Konflikts „Firma muss Know-how freigeben": synthetische Trainingsdaten, RAG ohne Persistenz, On-Premise-Fine-Tuning?
4. **Zielgruppe & Vorwissen** – Ab welchem Jahrgang/Vorwissen realistisch? Stundenumfang?
5. **Partner & Infrastruktur** – Konkrete Partnerfirma/Forschung? Hardware- bzw. Cloud-Bedarf an der Schule?
6. **Modulskizze** – Schriftliche Skizze (Lernziele, Ablauf, Bewertung)?
