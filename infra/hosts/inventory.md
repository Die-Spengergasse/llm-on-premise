# Host Inventory

Concrete hosts integrated into (or being evaluated for) the
llm-on-premise stack. Hardware specs are non-sensitive and tracked.
Secrets (IP/MAC/credentials) live in `secrets.local.md` (git-ignored).

---

## Host: dev-rig-01

> Status: **planning** — power fix pending physical install (see below).

| Field | Value |
|---|---|
| Role | Dev / test / experiment rig (**not** a vLLM backend) |
| Hostname | TODO |
| CPU | TODO |
| RAM | TODO |
| GPU | NVIDIA RTX 2070, 8 GB GDDR6 (Turing, 2018) |
| GPU power sockets | 2x 8-pin |
| Motherboard | Gigabyte GR-X150-PRO ECC *(model unverified — TODO confirm)* |
| PSU | Corsair VX550W / CMPSU-550VX — 550 W, +12 V @ 41 A (~492 W) |
| PSU PCIe connectors | 1x (6+2)-pin + 1x 6-pin |
| Storage | TODO |
| Network | TODO |
| Added | 2026-07-02 |

### Power-connector situation

The card has two 8-pin sockets; the PSU provides one usable 8-pin
(the 6+2 lead) and one 6-pin — a shortfall of one 8-pin. Wattage is
ample (~310 W load vs. ~492 W on the 12 V rail); this is purely a
connector-shape mismatch.

**Fix (decided 2026-07-02):** 6-pin to 8-pin PCIe adapter on the PSU's
6-pin lead. Card socket 1 <- 6+2 lead; card socket 2 <- 6-pin + adapter;
each fed from its own cable.

**Adapter spec:** 1-to-1 PCIe 6-pin (female, PSU) to 8-pin (male, GPU),
18 AWG. Example: Cable Matters 2-pack (ASIN B01DV1Z32Y).

**Avoid:** any Y-splitter that fans a single PSU connector to both card
sockets (overload/fire risk). Avoid EPS/CPU 6-to-8 adapters (wrong
pinout — damages GPU).

**Open precheck:** physically confirm the two PSU PCIe leads are
separate cables, not a single daisy-chain, before final install.

### Role rationale

8 GB VRAM cannot run the project's target models (GLM-5.2, DeepSeek V4,
Qwen 3.6) at usable precision/context. The box is scoped to vLLM
bring-up with tiny quantized models and tooling tests — not production
inference. See `docs/ai/DECISIONS.md`.
