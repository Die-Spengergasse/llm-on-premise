#!/usr/bin/env python3
"""Merging models.dev catalog proxy for opencode.

Serves GET /api.json = upstream https://models.dev/api.json with a `litellm`
provider injected, whose models are fetched from LiteLLM's GET /v1/models.

opencode is pointed at this proxy via OPENCODE_MODELS_URL; it fetches
`${OPENCODE_MODELS_URL}/api.json` and refreshes every ~60 min, so adding a
model on the LiteLLM side (any host) appears in the opencode picker with
zero per-client `models` config and without any sync script.

Resilience: upstream + litellm fetches are cached to disk (last-good) and
served on failure, so a transient outage never yields an empty catalog
(which would wipe opencode's built-in providers).
"""
import json
import os
import re
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = os.environ.get("MODELS_DEV_URL", "https://models.dev")
UA = os.environ.get("UPSTREAM_USER_AGENT", "opencode-models-proxy/1.0 (+https://opencode.ai)")
LITELLM_INTERNAL = os.environ.get("LITELLM_INTERNAL_URL", "http://litellm:11434")
LITELLM_KEY = os.environ.get("LITELLM_PROXY_KEY", "")
# Public baseURL opencode clients will actually call for inference:
LITELLM_PUBLIC = os.environ.get("LITELLM_PUBLIC_URL", "http://10.8.0.18:11434/v1")
CACHE_DIR = os.environ.get("CACHE_DIR", "/app/cache")
TTL = int(os.environ.get("UPSTREAM_TTL", "600"))  # 10 min
HOST_LABEL = os.environ.get("HOST_LABEL", "gregor")

FORCE_UPPER = {"it", "qat", "mlx", "ecc", "mxfp", "nvfp", "mtp"}


def _fmt(tok):
    tl = tok.lower()
    if tl in FORCE_UPPER:
        return tok.upper()
    m = re.match(r"^([A-Za-z]*)(\d+)([A-Za-z]*)$", tok)
    if m:
        p, d, s = m.groups()
        return p.upper() + d + s.upper()
    if tok.isdigit():
        return tok
    if len(tok) <= 5:
        return tok.upper()
    return tok.capitalize()


def display_name(model_id):
    """'gemma4:12b-it-qat' -> 'Gemma 4 12B IT QAT (gregor)'."""
    base, _, tag = model_id.partition(":")
    base = re.sub(r"(?<=[A-Za-z])(\d+)", r" \1", base)
    base = base[0].upper() + base[1:] if base else base
    toks = [_fmt(t) for t in re.split(r"[-_]", tag) if t]
    name = base + (" " + " ".join(toks) if toks else "")
    return f"{name} ({HOST_LABEL})"


def _get(url, headers=None, timeout=10):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _read_disk(name):
    p = os.path.join(CACHE_DIR, name)
    try:
        with open(p, "rb") as f:
            return f.read()
    except Exception:
        return None


def _write_disk(name, data):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        p = os.path.join(CACHE_DIR, name)
        tmp = f"{p}.{os.getpid()}.{int(time.time())}.tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, p)
    except Exception as e:
        print(f"[warn] write {name}: {e}", file=sys.stderr)


def fetch_upstream():
    raw = _read_disk("upstream.json")
    if raw:
        try:
            d = json.loads(raw)
            mtime = os.path.getmtime(os.path.join(CACHE_DIR, "upstream.json"))
            if time.time() - mtime < TTL:
                return d
        except Exception:
            pass
    try:
        raw = _get(f"{UPSTREAM}/api.json", timeout=12)
        d = json.loads(raw)
        _write_disk("upstream.json", raw)
        return d
    except Exception as e:
        print(f"[warn] upstream fetch: {e}", file=sys.stderr)
        if raw:
            return json.loads(raw)
        return None


def fetch_litellm_models():
    try:
        raw = _get(
            f"{LITELLM_INTERNAL}/v1/models",
            headers={"Authorization": f"Bearer {LITELLM_KEY}"} if LITELLM_KEY else {},
            timeout=8,
        )
        d = json.loads(raw)
        return [m["id"] for m in d.get("data", [])]
    except Exception as e:
        print(f"[warn] litellm fetch: {e}", file=sys.stderr)
        # fall back to last-known model list
        raw = _read_disk("litellm_models.json")
        if raw:
            return json.loads(raw)
        return None


def build_provider(model_ids):
    models = {}
    for mid in model_ids or []:
        models[mid] = {
            "id": mid,
            "name": display_name(mid),
            "release_date": "",
            "attachment": False,
            "reasoning": True,
            "temperature": True,
            "tool_call": True,
            "limit": {"context": 131072, "output": 8192},
        }
    return {
        "id": "litellm",
        "name": f"LiteLLM ({HOST_LABEL})",
        "env": ["LITELLM_API_KEY"],
        "npm": "@ai-sdk/openai-compatible",
        "api": LITELLM_PUBLIC,
        "models": models,
    }


def build_catalog():
    upstream = fetch_upstream()
    model_ids = fetch_litellm_models()

    # last-merged disk cache for the both-fail case
    if upstream is None and model_ids is None:
        raw = _read_disk("merged.json")
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                pass

    catalog = dict(upstream) if isinstance(upstream, dict) else {}
    if model_ids is not None:
        catalog["litellm"] = build_provider(model_ids)
        _write_disk("litellm_models.json", json.dumps(model_ids).encode())
    else:
        # litellm failed: keep prior injected entry from last-merged if present
        prev = _read_disk("merged.json")
        if prev:
            try:
                pc = json.loads(prev)
                if "litellm" in pc:
                    catalog["litellm"] = pc["litellm"]
            except Exception:
                pass

    out = json.dumps(catalog).encode()
    _write_disk("merged.json", out)
    return catalog


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "public, max-age=300")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/api.json", "/"):
            try:
                body = json.dumps(build_catalog()).encode()
                self._send(200, body)
            except Exception as e:
                print(f"[err] /api.json: {e}", file=sys.stderr)
                self._send(500, b'{"error":"internal"}')
        elif self.path == "/healthz":
            self._send(200, b'{"status":"ok"}')
        else:
            self._send(404, b'{"error":"not found"}')

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", file=sys.stderr)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"models-proxy listening on :{port} (upstream={UPSTREAM} litellm={LITELLM_INTERNAL})", file=sys.stderr)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()