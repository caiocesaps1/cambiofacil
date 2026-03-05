import json
import time
from typing import Any

# Tenta usar Redis; se não disponível, usa cache in-memory
try:
    import redis as redis_lib
    from app.config import settings

    _redis = redis_lib.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2)
    _redis.ping()
    REDIS_AVAILABLE = True
except Exception:
    _redis = None
    REDIS_AVAILABLE = False

# Cache in-memory: {key: (value, expires_at)}
_memory_cache: dict[str, tuple[Any, float]] = {}


def get(key: str) -> Any | None:
    if REDIS_AVAILABLE:
        raw = _redis.get(key)
        return json.loads(raw) if raw else None

    entry = _memory_cache.get(key)
    if entry and time.time() < entry[1]:
        return entry[0]
    return None


def set(key: str, value: Any, ttl: int) -> None:
    if REDIS_AVAILABLE:
        _redis.setex(key, ttl, json.dumps(value))
    else:
        _memory_cache[key] = (value, time.time() + ttl)


def delete(key: str) -> None:
    if REDIS_AVAILABLE:
        _redis.delete(key)
    else:
        _memory_cache.pop(key, None)


def is_redis() -> bool:
    return REDIS_AVAILABLE
