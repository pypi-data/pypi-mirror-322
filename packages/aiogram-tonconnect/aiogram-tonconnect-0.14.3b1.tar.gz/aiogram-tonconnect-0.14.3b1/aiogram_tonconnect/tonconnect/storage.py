import asyncio
from typing import Any

from redis.asyncio import Redis
from tonutils.tonconnect import IStorage


class ATCRedisStorage(IStorage):

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def set_item(self, key: Any, value: Any) -> None:
        async with self.redis.client() as client:
            await client.set(name=key, value=value)

    async def get_item(self, key: Any, default_value: str = None) -> Any:
        async with self.redis.client() as client:
            value = await client.get(name=key)
            return value if value else default_value

    async def remove_item(self, key: Any) -> None:
        async with self.redis.client() as client:
            await client.delete(key)


class ATCMemoryStorage(IStorage):
    data = {}

    def __init__(self) -> None:
        self.lock = asyncio.Lock()

    async def set_item(self, key: Any, value: Any) -> None:
        async with self.lock:
            self.data[key] = value

    async def get_item(self, key: Any, default_value: str = None) -> Any:
        async with self.lock:
            return self.data.get(key) if key in self.data else default_value

    async def remove_item(self, key: Any) -> None:
        async with self.lock:
            self.data.pop(key, None)
