# PITFALLS — llm-on-premise

## Bekannte Fallstricke

- **Hardware-Entscheidung blockiert Setup**: Ohne finale Hardware kann vLLM-Konfiguration nicht abgeschlossen werden
- **ROCm vs. CUDA**: AMD-Optionen sind günstiger, aber ROCm-Ökosystem ist weniger ausgereift als CUDA
- **Gemma 4 Lizenz**: Apache 2.0, aber SuperGemma 4 Uncensored ist ein Community-Derivat – Policy für Schulumgebung klären
- **SSO-Integration**: Auth hängt an Schul-IdM – Koordination mit ZID nötig
- **Tool Calling Zuverlässigkeit**: Nicht alle Modelle liefern konsistentes Function Calling für SearXNG – evaluieren vor Deployment
- **Preise veralten schnell**: Hardware- und API-Preise ändern sich monatlich. Alle Preisangaben mit Datum versehen (DOMAIN.md). Stand 2026-06-24 als Referenz notiert.
- **China-Datenschutz**: DeepSeek, SiliconFlow, Kimi, GLM sind chinesische Anbieter. DSGVO-konformer Betrieb ungeklärt. On-Premise oder EU-Anbieter (Hetzner, OVHcloud, Gcore, Mistral) sind der sichere Weg.
- **ChatGPT Edu-Preis unsicher**: Quellen widersprechen sich ($10/Schüler/Jahr vs. $10/Schüler/Monat). Letzteres angenommen für Berechnungen. Vor Vertrag klären.
- **GPU-DRAM-Preisschock**: LPDDR5x-Knappheit hat DGX-Spark- und Hetzner-Preise 2025/26 steigen lassen. Temporär, aber aktuell real.

## Strom / PCIe-Anschlüsse

- **6+2-Pin ist ein 8-Pin**: Die 2-Pin-Sektion wird auf den 6-Pin aufgesteckt – das ist der bestimmte, sichere 8-Pin-PCIe-Anschluss. Kein Adapter nötig, kein „Hack".
- **Keine Y-Splitter von einem PSU-Anschluss auf zwei Kartensockel**: Überlastet die einzelne Leitung → Schmelz-/Brandgefahr. Lieber beide separaten PCIe-Stränge des Netzteils nutzen (je einen pro Sockel).
- **PCIe- vs. EPS/CPU-6→8-Adapter**: Pinout unterschiedlich. EPS-Adapter in eine GPU gesteckt = Karte zerstört. Nur PCIe-Adapter verwenden.
- **Netzteil-Alterung**: VX550W (CMPSU-550VX, ~2008) – Kondensatoralterung, fehlende moderne Schutzschaltungen. Für unattended-Betrieb langfristig austauschen.
