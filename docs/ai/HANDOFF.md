# HANDOFF — llm-on-premise

Offene Aufgaben für die nächste Sitzung.

1. [ ] Shell reloaden / aktives `opencode -c` neu starten, damit `OPENCODE_MODELS_URL` (aus `~/.bash_aliases`) + reduzierte `opencode.json` (`provider.litellm = { options }`, kein models-Block) greifen. Danach echten Chat via Picker testen (Modell lädt, contention-429 bei parallelem anderen Modell verifizieren).
2. [ ] `OPENCODE_MODELS_URL=http://10.8.0.18:11436` für das Schüler-Lab austollen (Shared-Launcher oder `/etc/profile.d/opencode.sh`) — aktuell nur in georgs `~/.bash_aliases`.
3. [ ] Management-VM aufsetzen (Issue #3). Danach LiteLLM migrieren: `rsync /opt/litellm <vm>:` + `docker compose up -d`; `api_base` bleibt `10.8.0.18:11435`, nichts am Katalog ändern.
4. [ ] Network Hardening / ufw für `:11435` (Issue #4) — aktuell Bypass um LiteLLM-Auth möglich (Known Gap). Siehe PITFALLS.md (Docker+ufw): `:11434` ist Container-Port (ufw kann nicht filtern), nur `:11435`-Filterung möglich.
5. [ ] Hardware-Entscheidung (Issues #2, #5, #7), LiteLLM Access Control / Virtual-Keys für User-Groups (Issue #6), dev-rig-01 Adapter einbauen (Issue #12).