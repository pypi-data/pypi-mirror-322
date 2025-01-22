import asyncio
import json
import urllib.parse
import zlib
import redis
from contextlib import asynccontextmanager
from redis.asyncio import Redis as AsyncRedis
from typing import AsyncGenerator, Optional, Any
from fastapi.encoders import jsonable_encoder


class RedisUtility:

    def __init__(self, settings):
        self.settings = settings

    def get_redis_url(self) -> str:
        """
        Constructs the Redis connection URL based on the current settings,
        including username and password if provided.

        Returns:
            str: The Redis connection URL.

        Raises:
            ValueError: If any required Redis setting is missing.
        """
        required_settings = ['redis_host', 'redis_port', 'redis_db']
        for setting in required_settings:
            if not getattr(self.settings, setting, None):
                raise ValueError(f"Missing required Redis setting: {setting}")

        username = urllib.parse.quote(self.settings.redis_username) if hasattr(self.settings, 'redis_username') and self.settings.redis_username else ''
        password = urllib.parse.quote(self.settings.redis_password) if hasattr(self.settings, 'redis_password') and self.settings.redis_password else ''

        if username and password:
            auth_part = f"{username}:{password}@"
        elif password:
            auth_part = f":{password}@"
        elif username:
            auth_part = f"{username}@"
        else:
            auth_part = ''

        if hasattr(self.settings, 'redis_ssl') and self.settings.redis_ssl:
            protocol = 'rediss'
        else:
            protocol = 'redis'

        return f"{protocol}://{auth_part}{self.settings.redis_host}:{self.settings.redis_port}/{self.settings.redis_db}"

    def get_redis_client(self) -> redis.Redis:
        return redis.Redis.from_url(self.get_redis_url())

    def get_redis(self) -> redis.Redis:
        redis_client = self.get_redis_client()
        yield redis_client

    async def get_async_redis_client(self) -> AsyncRedis:
        return AsyncRedis.from_url(self.get_redis_url())

    @asynccontextmanager
    async def get_async_redis(self) -> AsyncGenerator[AsyncRedis, None]:
        async_redis_client = await self.get_async_redis_client()
        try:
            yield async_redis_client
        finally:
            await async_redis_client.close()

    @staticmethod
    async def read_data_in_chunks(redis_client: AsyncRedis, key: str, compression: bool = True) -> Optional[Any]:
        chunk_count = await redis_client.get(f"{key}:chunk_count")
        if not chunk_count:
            return None

        chunk_count = int(chunk_count)

        async def get_chunk(index):
            return await redis_client.get(f"{key}:chunks:{index}")

        # Fetch all chunks concurrently
        chunks = await asyncio.gather(*(get_chunk(index) for index in range(chunk_count)))

        # Join all chunks into a single byte string
        data = b"".join(chunks)

        # Decompress if necessary
        if compression:
            data = zlib.decompress(data).decode('utf-8')

        # Return the loaded JSON data
        return json.loads(data)

    @staticmethod
    async def write_data_in_chunks(redis_client: AsyncRedis, key: str, data: Any, chunk_size: int = 1024, compression: bool = True) -> None:
        data = json.dumps(jsonable_encoder(data)).encode('utf-8')
        if compression:
            data = zlib.compress(data, level=1)

        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        async def set_chunk(index, chunk):
            await redis_client.set(f"{key}:chunks:{index}", chunk)

        await redis_client.set(f"{key}:chunk_count", len(chunks))
        await asyncio.gather(*(set_chunk(index, chunk) for index, chunk in enumerate(chunks)))
