from typing import Sequence

from redis.asyncio import Redis




class RedisZset:
    def __init__(self, client: Redis):
        self._client = client

    async def add(self, key: str, members_with_scores: dict[str, str | bytes | int | float]) -> int:

        return await self._client.zadd(key, members_with_scores)

    async def remove(self, key: str, *members: str | bytes | int | float) -> int:
        return await self._client.zrem(key, *members)

    async def score(self, key: str, member: str | bytes | int | float) -> float | None:
        return await self._client.zscore(key, member)

    async def get_all(self, key: str, start: int = 0, stop: int = -1, withscores: bool = False) -> list[
        tuple[str, float] | str]:
        members = await self._client.zrange(key, start, stop, withscores=withscores)
        if withscores:
            return [(member, score) for member, score in members]
        else:
            return members

    async def length(self, key: str) -> int:
        return await self._client.zcard(key)

    async def range_by_score(self, key: str, min_: float, max_: float, start: int = 0, num: int = 5,
                             withscores: bool = False) -> list[tuple[str, float]]:

        members = await self._client.zrangebyscore(key, min_, max_, start=start, num=num,
                                                   withscores=withscores)

        if withscores:
            return [(member, score) for member, score in members]
        else:
            return members

    async def rank(self, key: str, member: str | bytes | int | float, reverse: bool = False) -> int:
        if reverse:
            return await self._client.zrevrank(key, member)
        else:
            return await self._client.zrank(key, member)
