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

## Migration zu Groq Cloud mit Token-Rotation (Issue #21, Stand 2026-09-17)

GROQ bietet `whisper-large-v3` kostenlos (Free-Tier). Schüler generieren
einzeln ihre GROQ-API-Keys; der LiteLLM-Router rotiert/last-balanciert über
alle Keys (Cooldown bei 429). Open WebUI sieht nur EINEN Key (den
LiteLLM-Key) — Rotation ist für den Client unsichtbar.

### Setup (sobald die ersten Keys von Schülern da sind)

1. **LiteLLM-DB: ein Deployment pro Key** (`/opt/litellm`-Postgres, Tabelle
   `LiteLLM_ProxyModelTable`; via LiteLLM-UI oder SQL):

   ```sql
   INSERT INTO "LiteLLM_ProxyModelTable"
     (model_id, model_name, litellm_params, model_info, created_at, updated_at)
   VALUES
     ('groq-stt-<schueler-n>', 'groq-whisper',
      '{"model": "groq/whisper-large-v3", "api_key": "<GROQ_KEY_SCHUELER_N>"}',
      '{}', EXTRACT(EPOCH FROM now()) * 1000, EXTRACT(EPOCH FROM now()) * 1000);
   ```

   Der Router load-balanced automatisch über alle Deployments mit demselben
   `model_name` und Cooldown'ed Keys mit 429s.

2. **Open WebUI umstellen** (Admin Panel → Settings → Audio oder direkt
   config-DB, ConfigVar-Präzedenz beachten):
   - `audio.stt.engine` = `openai` (bleibt)
   - `audio.stt.openai.api_base_url` = `http://litellm:11434/v1` (bleibt)
   - `audio.stt.model` = `groq-whisper`
   - Key: bestehender `LITELLM_PROXY_KEY` (bleibt)

3. **Verifikation**: Mikrofon-Button in Open WebUI → Sprachnachricht →
   Transkript; LiteLLM-Logs zeigen das rotierende Deployment.

### Rollout / Rückbau

- Keys nachliefern: nur Schritt 1 wiederholen (Neue Deployment-Rows), kein
  Open-WebUI-Eingriff, kein Restart nötig.
- Key-Tausch (Schüler widerruft): Deployment-Row löschen.
- **Rückweg zu lokalem Whisper** (DSGVO-Fallback): `docker compose up -d
  whisper` + DB-INSERT laut PITFALLS.md (Whisper-Restore-Anleitung) +
  `audio.stt.model` = `whisper-1`.

### DSGVO

Schüler-Stimmdaten gehen über GROQ in die USA (Free-Tier, Zero-Retention
klären). Bewusste Entscheidung (Issue #21): STT ist freiwilliges Feature;
lokales Whisper bleibt Restore-Option. Für DSGVO-kritische Last bleibt
On-Prem das Ziel (Issue #2/#5/#7).
