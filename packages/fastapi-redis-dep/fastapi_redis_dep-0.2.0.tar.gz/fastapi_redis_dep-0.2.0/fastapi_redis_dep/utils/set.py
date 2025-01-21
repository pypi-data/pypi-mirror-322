from typing import Sequence

from redis.asyncio import Redis

SetType = str | bytes | int | float

class RedisSet:
    def __init__(self, client: Redis):
        self._client = client

    async def add(self, key: str, *members: SetType) -> int:
        return await self._client.sadd(key, *members) # type: ignore

    async def remove(self, key: str, *members: SetType) -> int:
        return await self._client.srem(key, *members) # type: ignore

    async def exists(self, key: str, member:SetType) -> int:
        return await self._client.sismember(key, member) > 0 # type: ignore

    async def get_all(self, key: str) -> set[SetType]:
        members = await self._client.smembers(key) # type: ignore
        return set(members)

    async def length(self, key: str) -> int:
        return await self._client.scard(key) # type: ignore

    async def intersection(self, keys: Sequence[str]) -> set[SetType]:
        return set(await self._client.sinter(*keys)) # type: ignore

    async def union(self, keys: Sequence[str]) -> set[SetType]:
        return set(await self._client.sunion(*keys)) # type: ignore

    async def difference(self, keys: Sequence[str]) -> set[SetType]:
        return set(await self._client.sdiff(*keys)) # type: ignore
