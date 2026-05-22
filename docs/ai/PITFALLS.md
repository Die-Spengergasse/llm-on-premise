# PITFALLS — llm-on-premise

## Bekannte Fallstricke

- **Hardware-Entscheidung blockiert Setup**: Ohne finale Hardware kann vLLM-Konfiguration nicht abgeschlossen werden
- **ROCm vs. CUDA**: AMD-Optionen sind günstiger, aber ROCm-Ökosystem ist weniger ausgereift als CUDA
- **Gemma 4 Lizenz**: Apache 2.0, aber SuperGemma 4 Uncensored ist ein Community-Derivat – Policy für Schulumgebung klären
- **SSO-Integration**: Auth hängt an Schul-IdM – Koordination mit ZID nötig
- **Tool Calling Zuverlässigkeit**: Nicht alle Modelle liefern konsistentes Function Calling für SearXNG – evaluieren vor Deployment
