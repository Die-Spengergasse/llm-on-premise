# HANDOFF — llm-on-premise

Offene Aufgaben für die nächste Sitzung.

1. [x] Shell reloaden / aktives `opencode -c` neu starten, damit `OPENCODE_MODELS_URL` ... E2e verifiziert: ollama=`/v1/models`=models-proxy=2. opencode-Picker zeigt 2 (ggf. Picker-reload wg. Client-Cache `max-age=300`).
2. [ ] **Open WebUI ist deployt** (`:3000`, LDAP auth gegen Schul-AD). **Offen:** HTTPS für Mic-Zugriff (Caddy/nginx vorm Open WebUI). Siehe Issue #14.
3. [ ] `OPENCODE_MODELS_URL=http://<WG_IP_GREGOR>:11436` (IP aus `infra/hosts/secrets.local.md`) für das Schüler-Lab austollen (Shared-Launcher oder `/etc/profile.d/opencode.sh`) — aktuell nur in georgs `~/.bash_aliases`. Achtung: ein daemonized `opencode serve` (PPID=1) erbt die Var nur, wenn der Startprozess sie geladen hat; robust via systemd-User-Unit mit `Environment=` + `loginctl enable-linger`.
4. [ ] Management-VM aufsetzen (Issue #3). Danach LiteLLM migrieren: `rsync -a /opt/litellm <vm>:` + `docker compose up -d`; `api_base` bleibt `<WG_IP_GREGOR>:11435`, nichts am Katalog ändern. Das Blob-Inventory `/opt/litellm/blob-inventory/` ggf.同步 mit-rsyncen, falls >8 GB-HW ansteht.
5. [ ] Network Hardening / ufw für `:11435` (Issue #4) — aktuell Bypass um LiteLLM-Auth möglich (Known Gap). Siehe PITFALLS.md (Docker+ufw): `:11434` ist Container-Port (ufw kann nicht filtern), nur `:11435`-Filterung möglich.
6. [ ] Hardware-Entscheidung (Issues #2, #5, #7), LiteLLM Access Control / Virtual-Keys für User-Groups (Issue #6), dev-rig-01 Adapter einbauen (Issue #12). Bei >8 GB-HW: 12b-Blobs aus `/opt/litellm/blob-inventory/` per Restore-Anleitung (README.md dort) reaktivieren.