from typing import AsyncGenerator, Awaitable

from redis.asyncio import Redis


class RedisList:

    def __init__(self, client: Redis):
        self._client = client

    async def lpush(self, key: str, *value: str) -> int:
        return await self._client.lpush(key, *value) #type: ignore

    async def lindex(self, key: str, index: int) -> str | None:
        return await self._client.lindex(key, index) # type: ignore

    async def linsert(self, name: str, where: str, refvalue: str, value: str) -> int:
        return await self._client.linsert(name, where, refvalue, value) # type: ignore

    async def llen(self, key: str) -> int:
        return await self._client.llen(key) # type: ignore

    async def lpop(self, key: str, count: int | None = None) -> str | list[str] | None:
        return await self._client.lpop(key, count) # type: ignore

    async def lset(self, key: str, index: int, value: str) -> str:
        return await self._client.lset(key, index, value) # type: ignore

    async def rpush(self, key: str, *value: str) -> int:
        return await self._client.rpush(key, *value) # type: ignore

    async def rpop(self, key: str, count: int | None = None) -> str | list[str]:
        return await self._client.rpop(key, count) # type: ignore

    async def lrange(self, key: str, start: int, stop: int) -> list[str]:
        return await self._client.lrange(key, start, stop) # type: ignore

    async def ltrim(self, key: str, start: int, stop: int) -> str:
        return await self._client.ltrim(key, start, stop) # type: ignore

    async def lrem(self, key: str, count: int, value: str) -> int:
        return await self._client.lrem(key, count, value) # type: ignore

    async def list_iterator(self, key: str) -> AsyncGenerator[str, None]:
        length = await self._client.llen(key) # type: ignore
        for i in range(length):
            value = await self._client.lindex(key, i) # type: ignore
            yield value # type: ignore

