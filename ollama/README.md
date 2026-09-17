# Ollama — LLM Inference Backend

Ollama läuft als Host-Service (systemd) auf gregor und dient als
LLM-Inference-Backend für den gesamten Stack.

## Service

| Eigenschaft | Wert |
|-------------|------|
| Port | `:11435` (`OLLAMA_HOST=0.0.0.0:11435`) |
| systemd unit | `/etc/systemd/system/ollama.service` (Backup: `ollama.service`) |
| Env-Variablen | `MAX_LOADED_MODELS=1`, `KEEP_ALIVE=-1`, `FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, `OLLAMA_CONTEXT_LENGTH=32768` (Fallback für Tags ohne `num_ctx`; Modelfile-Werte gewinnen) |
| Auth | **Keine** — direkt erreichbar (Known Gap, Issue #4) |
| GPU | RTX 2070 SUPER, 8 GB VRAM (shared mit whisper, siehe SingleGpuGuard) |

## Modelle (Live, Stand 2026-09-17 — alle auf nativem Max, Issue #20)

| Tag | Basis | Größe | Kontext (`num_ctx` = Arch-Max) | Zweck |
|-----|-------|-------|-------------------------------|-------|
| `qwen3:8b` | qwen3:8b | 5.2 GB | **40960** (Achtung: 8,8 GB Footprint → 22 % CPU-Offload) | Default für OpenCode |
| `qwen3.5:9b` | qwen3.5 | 6.6 GB | **262144** | Großer Kontext, schmalere Aktivierung später |
| `qwen3.5:4b` | qwen3.5 | 3.4 GB | **262144** | Großer Kontext, schmalere Aktivierung später |
| `qwen2.5:3b` | qwen2.5:3b | 1.9 GB | **32768** | Coding |
| `qwen3:1.7b` | qwen3:1.7b | 1.4 GB | **40960** | General Chat (zu klein für Tools) |
| `llama3.2:3b` | llama3.2:3b | 2.0 GB | **131072** | General Chat (Alternative) |

Arch-Maxima per `ollama show` (gguf-Metadaten; `num_ctx` darüber wird gecappt).
Alle Modelle nutzen Q8 KV-Cache (`OLLAMA_KV_CACHE_TYPE=q8_0`) für halben
KV-Speicher vs. fp16. Alle Tags sind getunt (temp 0.5, "Do NOT use tools") —
Stock-Tags liefen zuvor auf temperature 1.0 + 4K-VRAM-Default.

## Modelfiles

Jedes Modell hat einen tuned Modelfile im `/ollama/` Verzeichnis:

| Datei | Modell | Besonderheiten |
|-------|--------|----------------|
| `Modelfile.qwen3-8b` | qwen3:8b | `num_ctx 40960` (Arch-Max), "Do NOT use tools" |
| `Modelfile.qwen3.5-9b` | qwen3.5:9b | `num_ctx 262144` (Arch-Max), "Do NOT use tools" |
| `Modelfile.qwen3.5-4b` | qwen3.5:4b | `num_ctx 262144` (Arch-Max), "Do NOT use tools" |
| `Modelfile.qwen3-1.7b` | qwen3:1.7b | `reasoning_tags=false`, `think=false`, "Do NOT use tools" |
| `Modelfile.qwen2.5-coder-3b` | qwen2.5-coder:3b | "Do NOT use tools" |
| `Modelfile.llama3.2-3b` | llama3.2:3b | "Do NOT use tools", stripped template |
| `Modelfile.qwen2.5-3b` | qwen2.5:3b | Deprecated (durch llama3.2:3b ersetzt) |
| `Modelfile.qwen3` | qwen3:1.7b | Alias von qwen3-1.7b |

### Modelfile anwenden

```bash
ollama create <tag> -f /ollama/Modelfile.<name>
```

Beispiel:
```bash
ollama create qwen3:1.7b -f /ollama/Modelfile.qwen3-1.7b
```

### System Prompt (alle Modelle)

```
You are a precise, helpful assistant. Answer concisely and accurately in the
language of the user's question. Do NOT use any tools or functions. Respond
only in plain text. When unsure, state your uncertainty.
```

"Do NOT use tools" ist kritisch — ohne diesen Prompt generieren kleine
Modelle (1.7B-3B) Tool-Call-JSON aus ihrem Training. Siehe `docs/ai/TIPS.md`.

## VRAM-Budget

```
RTX 2070 SUPER: 8 GB VRAM (Whisper deaktiviert, Stand 2026-09-17)
├── qwen3:8b @40K:     ~8,8 GB Footprint → 22 % CPU-Offload (größtes Fenster > volle GPU)
├── qwen3.5:9b @262K:  deutlich > VRAM → mehrheitlich CPU (Aktivierung später)
├── kleine Modelle:     1,4–3,4 GB Weights + Q8-KV → mehr Headroom für große Fenster
├── CUDA overhead:     ~0,5 GB
└── Faustregel:        Fenster am Arch-Max = max. Kontext, nicht max. Speed
```

SingleGpuGuard (in LiteLLM) stellt sicher, dass nur ein Modell gleichzeitig
geladen ist. Bei Modellwechsel: ~50s Evict+Load.

## Nützliche Kommandos

```bash
ollama list                           # Geladene Modelle
ollama ps                             # Aktuell im VRAM
ollama show <tag>                     # Modell-Details
ollama show <tag> --modelfile         | Vollständiger Modelfile (mit Template)
ollama rm <tag>                       # Modell löschen
ollama pull <tag>                     # Modell pullen
ollama create <tag> -f Modelfile      # Modell aus Modelfile erstellen
nvidia-smi                            # VRAM-Nutzung
```

## Geplant

- **7B Modell** (qwen3:7b): möglich wenn whisper zu Groq-Cloud wandert
  (3.9 GB VRAM frei). 7B ist groß genug für zuverlässiges Function Calling.
- **Modelle aus Blob-Inventory restoren** bei >8 GB Hardware:
  siehe `/opt/litellm/blob-inventory/README.md`
