# STATE — llm-on-premise

## Current Focus
Dev/Test-Host (RTX 2070, dev-rig-01) inventarisiert; Power-Fix (6→8 Pin PCIe-Adapter) entschieden und in Issue #12 dokumentiert.

## Completed (this cycle)
- [x] Web-Recherche: Aktuelle GPU-Mietpreise, API-Preise, Education-Pläne (Stand Juni 2026)
- [x] Web-Recherche: Open Source vs. Closed Source Benchmarks (GLM-5.2, DeepSeek V4, Qwen 3.6 vs. GPT-5.5, Claude Opus 4.8)
- [x] Web-Recherche: Apple Mac Mini M4 Pro Preise für LLM-Inference
- [x] Web-Recherche: AMD Strix Halo Preis und Verfügbarkeit
- [x] Web-Recherche: Schülernachweis Spengergasse (2.600 Schüler, 280 Lehrer, 97 Klassen)
- [x] Präsentation in docs/praesentation/slides.md erstellt (HTML + PDF)
- [x] Phasen-Strategie definiert: API 2026 → HW-Nachkauf 2027/28 → autark 2028+
- [x] Dev/Test-Host inventarisiert (infra/hosts/inventory.md) – RTX 2070/8 GB, Rolle: Experiment-Rig (kein vLLM-Backend)
- [x] Power-Fix für Dual-8-Pin RTX 2070 entschieden: 6→8 Pin PCIe-Adapter am zweiten VX550-Strang (Issue #12)

## Pending
- [ ] Hardware-Entscheidung (Issues #2, #5, #7)
- [ ] Management-VM aufsetzen (Issue #3)
- [ ] Network Hardening (Issue #4)
- [ ] LiteLLM Access Control (Issue #6)
- [ ] dev-rig-01: Adapter einbauen, PCIe-Stränge physisch prüfen, Specs nachtragen (Issue #12)

## Blockers
- Hardware-Entscheidung
- ZID-Koordination (Netzwerk, VLAN, SSO)

## Next Session Suggestion
dev-rig-01: Adapter physisch einbauen, Stränge verifizieren, fehlende Specs (CPU/RAM/Hostname/Storage) in inventory.md nachtragen.
