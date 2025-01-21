from __future__ import annotations

from typing import Self, cast

import redis

from .uid_cache import UidCache


class RedisCache(UidCache):
    """Implementation of UidCache using a Redis backend."""

    def __init__(self: Self, redis_host: str, redis_port: int) -> None:
        """Initialise a RedisCache.

        @param redis_host: Host for the Redis cache
        @param redis_port: Port for the Redis cache
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.cache_: redis.Redis[str] | None = None

    @property
    def cache(self: Self) -> redis.Redis[str]:
        """Lazy-load the cache on request."""
        if not self.cache_:
            self.cache_ = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True,
            )
        return self.cache_

    def get(self: Self, identifier: str) -> int | None:
        value = self.cache.get(identifier)
        return None if value is None else int(value)

    def keys(self: Self) -> list[str]:
        return [str(k) for k in self.cache.keys()]  # noqa: SIM118

    def set(self: Self, identifier: str, uid_value: int) -> None:
        self.cache.set(identifier, uid_value)

    def values(self: Self, keys: list[str]) -> list[int]:
        return [int(cast(str, v)) for v in self.cache.mget(keys)]
