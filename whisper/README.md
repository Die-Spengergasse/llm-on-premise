# Whisper — Speech-to-Text (STT)

Whisper läuft als Docker-Container auf gregor und transkribiert
Sprachnachrichten für Open WebUI.

## Service

| Eigenschaft | Wert |
|-------------|------|
| Container | `whisper` (Docker, `hwdsl2/whisper-server:cuda`) |
| Port | `:11437` (→ Container `:9000`) |
| Model | `large-v3` |
| Device | CUDA (GPU) |
| Compute Type | `float16` |
| Language | `de` (Deutsch als Default) |
| VRAM | ~3.9 GB |

## Konfiguration (compose.yaml)

```yaml
whisper:
  image: hwdsl2/whisper-server:cuda
  environment:
    WHISPER_MODEL: large-v3
    WHISPER_DEVICE: cuda
    WHISPER_COMPUTE_TYPE: float16
    WHISPER_LANGUAGE: de
    WHISPER_BEAM: 5
    WHISPER_API_KEY: ${WHISPER_API_KEY}
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

## VRAM-Impact

Whisper belegt **~3.9 GB** der 8 GB GPU. Das limitiert die Größe des
parallel laufbaren LLM-Modells deutlich:

```
8 GB GPU
├── whisper:  3.9 GB
├── LLM:      ~2.8 GB (max 1.7-3B Modell mit 24K Kontext)
├── Overhead: 0.5 GB
└── Frei:     ~0.8 GB
```

SingleGpuGuard in LiteLLM stellt sicher, dass whisper und LLM nicht
gleichzeitig geladen werden (OOM-Schutz).

## Migration zu Groq Cloud (geplant)

**Vorteil:** Groq bietet `whisper-large-v3` kostenlos über ihre API.
Das würde 3.9 GB VRAM freigeben für ein lokales 7B-Modell.

**Migration:**
1. Groq API Key besorgen (console.groq.com, free tier)
2. Open WebUI → Admin Panel → Settings → Audio:
   - STT Engine: `openai`
   - API Base URL: `https://api.groq.com/openai/v1`
   - API Key: `<groq-key>`
   - Model: `whisper-large-v3`
3. `sudo docker compose stop whisper`
4. `nvidia-smi` — 3.9 GB freigegeben

**Risiko:** Schüler-Stimmdaten gehen in die USA (DSGVO).
Für Produktion: lokales whisper als Fallback behalten oder Opt-In für Cloud-STT.
