import asyncio
import json
import os
import time
import traceback
import urllib.request
from typing import Optional

import yaml
from fastapi import HTTPException
from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import DualCache, UserAPIKeyAuth

_TRACE = "/app/data/guard.log"
_CONFIG_PATH = os.environ.get("LITELLM_CONFIG_PATH", "/app/config.yaml")

# If a backend's in_flight counter stays > 0 for longer than this without a
# matching success/failure event, the counter is considered leaked (lost
# callback: streaming disconnect, worker crash, dropped event, etc.). The next
# different-model request forces a reset and falls through to the swap path
# instead of 429-ing forever. Sized to LiteLLM request_timeout (600s) + grace.
_STALE_AFTER = 660.0

# Ollama /api/ps is polled per gated request to reconcile the guard's view of
# the resident model with ollama's real state (out-of-band loads via
# `ollama run` on the host or the :11435 direct-access bypass, Issue #4).
# Cached per api_base so a burst of requests costs one HTTP call per TTL window.
_OLLAMA_PS_TTL = 2.0
_OLLAMA_PS_TIMEOUT = 1.5
_PS_CACHE: dict[str, tuple[float, Optional[str]]] = {}

# model_name -> api_base, parsed from config.yaml at startup. At pre_call time
# LiteLLM has NOT yet populated metadata.litellm_params.api_base (the router
# selects the deployment only later), so _domain() cannot see the api_base from
# the request data. We resolve it from the config map instead. Log-event kwargs
# DO carry litellm_params.api_base, so both paths converge on the same key.
_MODEL_API_BASE: dict[str, str] = {}


def _trace(msg: str) -> None:
    try:
        with open(_TRACE, "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def _load_config_map() -> None:
    """Populate _MODEL_API_BASE from config.yaml (model_name -> api_base)."""
    try:
        with open(_CONFIG_PATH) as f:
            cfg = yaml.safe_load(f) or {}
        m: dict[str, str] = {}
        for entry in cfg.get("model_list", []) or []:
            name = entry.get("model_name")
            ab = (entry.get("litellm_params") or {}).get("api_base")
            if name and ab and name not in m:
                m[name] = ab
        _MODEL_API_BASE.clear()
        _MODEL_API_BASE.update(m)
        _trace(f"config map loaded: {len(m)} models from {_CONFIG_PATH}")
    except Exception as e:
        _trace(f"config map load failed: {e!r}")


def _domain(data_or_kwargs: dict) -> str:
    """Backend contention domain, keyed by the deployment's api_base.

    Two resolution paths, both yielding the same key for one deployment:
      - log-event kwargs: metadata.litellm_params.api_base is populated by
        LiteLLM after routing -> used directly.
      - pre_call data: litellm_params is NOT yet populated (router runs
        later) -> fall back to the config map (model_name -> api_base).
    Falls back to "__default__" only if neither resolves (e.g. a model not
    in config.yaml); reconcile is skipped for that key.
    """
    try:
        meta = (data_or_kwargs or {}).get("metadata") or {}
        lp = meta.get("litellm_params") or {}
        if hasattr(lp, "api_base") and getattr(lp, "api_base", None):
            return lp.api_base
        if isinstance(lp, dict) and lp.get("api_base"):
            return lp["api_base"]
        model = (data_or_kwargs or {}).get("model")
        if model and model in _MODEL_API_BASE:
            return _MODEL_API_BASE[model]
    except Exception:
        pass
    return "__default__"


def _ollama_loaded_model_sync(api_base: str) -> Optional[str]:
    """Blocking GET {api_base}/api/ps -> first loaded model name, or None."""
    url = api_base.rstrip("/") + "/api/ps"
    with urllib.request.urlopen(url, timeout=_OLLAMA_PS_TIMEOUT) as resp:
        if resp.status != 200:
            return None
        payload = json.loads(resp.read().decode("utf-8", "replace"))
    models = payload.get("models") or []
    if not models:
        return None
    return models[0].get("model") or models[0].get("name")


async def _ollama_loaded_model(
    api_base: str,
) -> "tuple[bool, Optional[str]]":
    """Return (fetched, loaded_model).

    - (True, "name")  -> ollama reports this model resident.
    - (True, None)    -> ollama reports nothing loaded.
    - (False, None)   -> fetch skipped (no api_base / fallback domain) or
                         failed AND no prior cache; caller must NOT reconcile.

    On fetch failure with a stale cache, the cached value is returned as
    (True, cached) for resilience (ollama briefly unreachable -> keep last
    known truth rather than dropping the guard's model).
    """
    if not api_base or api_base == "__default__":
        return (False, None)
    now = time.monotonic()
    cached = _PS_CACHE.get(api_base)
    if cached and now - cached[0] < _OLLAMA_PS_TTL:
        return (True, cached[1])
    try:
        name = await asyncio.to_thread(_ollama_loaded_model_sync, api_base)
    except Exception:
        if cached:
            return (True, cached[1])
        return (False, None)
    _PS_CACHE[api_base] = (now, name)
    return (True, name)


class _Domain:
    __slots__ = ("active_model", "in_flight", "last_busy_at", "lock")

    def __init__(self) -> None:
        self.active_model: Optional[str] = None
        self.in_flight: int = 0
        self.last_busy_at: float = 0.0
        self.lock = asyncio.Lock()


class SingleGpuGuard(CustomLogger):
    """Single-GPU residency policy for a shared Ollama backend.

    - A different model requested while the resident model is BUSY
      (in_flight > 0, and not stale) -> HTTP 429; the busy model stays.
    - A different model requested while the backend is IDLE -> atomic swap.
    - The same model requested again -> allowed (serialised by the backend).

    Two self-healing mechanisms guard against state divergence:

    1. Staleness: if in_flight > 0 but no success/failure event has arrived
       for _STALE_AFTER seconds, the counter is treated as leaked and reset
       on the next different-model request (lost callback recovery).
    2. Ollama reconcile: before deciding, the guard polls ollama /api/ps and,
       when idle, adopts ollama's actually-loaded model as truth. This
       corrects out-of-band loads (`ollama run` on the host, the :11435
       direct-access bypass, Issue #4) that the guard never observed.

    Counters are matched per request via ``litellm_call_id``: a request that
    was REJECTED in pre_call is never registered, so the failure log event
    LiteLLM emits for the rejection cannot touch the counters. State is per
    backend (api_base), so the guard stays correct after the planned move to
    a management VM fronting several Ollama nodes.
    """

    _GATED = {
        "completion", "acompletion",
        "text_completion", "atext_completion",
        "embeddings", "aembedding",
    }
    _SANITY_CEILING = 64

    def __init__(self) -> None:
        super().__init__()
        self._domains: dict[str, _Domain] = {}
        self._counted: set[str] = set()
        _load_config_map()
        _trace("init SingleGpuGuard")

    def _dom(self, key: str) -> _Domain:
        d = self._domains.get(key)
        if d is None:
            d = _Domain()
            self._domains[key] = d
        return d

    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: str,
    ):
        if call_type not in self._GATED:
            return data
        try:
            model = data.get("model")
            if not model:
                return data
            call_id = data.get("litellm_call_id")
            dom_key = _domain(data)
            dom = self._dom(dom_key)

            # Poll ollama BEFORE the lock so a slow /api/ps (1.5s timeout)
            # never blocks the event loop under the domain lock.
            fetched, loaded = await _ollama_loaded_model(dom_key)

            async with dom.lock:
                now = time.monotonic()

                if dom.in_flight >= self._SANITY_CEILING:
                    _trace(
                        f"SANITY-RESET dom={dom_key} "
                        f"in_flight={dom.in_flight}"
                    )
                    dom.in_flight = 0
                    dom.active_model = None

                # Reconcile with ollama's real resident model, but only when
                # idle: in_flight > 0 is owned by in-flight tracking +
                # staleness (ollama is truth for *loaded*, the guard is truth
                # for *in-flight*).
                if fetched and dom.in_flight == 0:
                    if loaded != dom.active_model:
                        if loaded is None:
                            _trace(
                                f"RECONCILE-EMPTY dom={dom_key} "
                                f"had={dom.active_model}"
                            )
                        else:
                            _trace(
                                f"RECONCILE dom={dom_key} "
                                f"had={dom.active_model} ollama={loaded}"
                            )
                        dom.active_model = loaded

                # Resolve the request against the (possibly reconciled) state.
                if dom.active_model is None:
                    dom.active_model = model
                    dom.in_flight = 1
                    dom.last_busy_at = now
                    _trace(f"ACCEPT dom={dom_key} model={model}")
                elif model == dom.active_model:
                    dom.in_flight += 1
                    dom.last_busy_at = now
                    _trace(
                        f"SAME dom={dom_key} model={model} "
                        f"in_flight={dom.in_flight}"
                    )
                else:
                    busy = dom.in_flight > 0
                    stale = busy and (now - dom.last_busy_at) > _STALE_AFTER
                    if busy and not stale:
                        _trace(
                            f"REJECT 429 active={dom.active_model} "
                            f"wanted={model} in_flight={dom.in_flight}"
                        )
                        # call_id is NOT registered -> the rejection's own
                        # failure log event will be a no-op in _adjust().
                        raise HTTPException(
                            status_code=429,
                            detail={
                                "error": {
                                    "message": (
                                        f"GPU backend busy with "
                                        f"'{dom.active_model}'; rejecting "
                                        f"'{model}'. Retry shortly."
                                    ),
                                    "type": "gpu_busy",
                                    "code": 429,
                                }
                            },
                            headers={"Retry-After": "5"},
                        )
                    if stale:
                        _trace(
                            f"STALE-RESET dom={dom_key} "
                            f"active={dom.active_model} "
                            f"in_flight={dom.in_flight} "
                            f"age={int(now - dom.last_busy_at)}s"
                        )
                    dom.active_model = model
                    dom.in_flight = 1
                    dom.last_busy_at = now
                    _trace(
                        f"SWAP dom={dom_key} -> {model} "
                        f"(was_busy={busy})"
                    )

                if call_id:
                    self._counted.add(call_id)
        except HTTPException:
            raise
        except Exception:
            traceback.print_exc()
        return data

    async def _adjust(self, data_or_kwargs: dict, on_failure: bool) -> None:
        try:
            kw = data_or_kwargs or {}
            call_id = kw.get("litellm_call_id")
            if not call_id or call_id not in self._counted:
                return  # rejected in pre_call (never counted) -> ignore
            self._counted.discard(call_id)
            dom = self._domains.get(_domain(kw))
            if dom is None:
                return
            async with dom.lock:
                if dom.in_flight > 0:
                    dom.in_flight -= 1
                if dom.in_flight == 0 and on_failure:
                    dom.active_model = None
        except Exception:
            traceback.print_exc()

    async def async_log_success_event(
        self, kwargs, response_obj, start_time, end_time
    ) -> None:
        await self._adjust(kwargs, on_failure=False)

    async def async_log_failure_event(
        self, kwargs, response_obj, start_time, end_time
    ) -> None:
        await self._adjust(kwargs, on_failure=True)


_load_config_map()
guard = SingleGpuGuard()
