import redis
from functools import wraps
from fastapi import Request
from ..exception import RequestException


def convert_seconds(seconds):
    time_units = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("week", 60 * 60 * 24 * 7),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1)
    ]
    result = {}
    for unit_name, unit_value in time_units:
        if seconds >= unit_value:
            result[unit_name], seconds = divmod(seconds, unit_value)

    result_str = ', '.join([f"{value} {key}{'s' if value > 1 else ''}" for key, value in result.items()])
    return result_str


def rate_limiter(limit: int = 5, period: int = 10, increase_factor: int = 2, development_mode: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis_client: redis.Redis = kwargs.get('redis')

            if not development_mode or not redis_client:
                request: Request = kwargs.get('request')
                if not request:
                    raise ValueError("Request object must be provided as a keyword argument.")

                path = request.url.path
                ip = request.headers.get('x-real-ip', 'localhost')

                block_key = f"rate-limit-block-list:{ip}"
                count_key = f"rate-limit:{ip}:{path}"

                is_blocked = redis_client.get(block_key)
                if is_blocked:
                    retry_after = redis_client.ttl(block_key)
                    block_time = int(retry_after * increase_factor)
                    redis_client.setex(block_key, block_time, path)
                    raise RequestException(
                        status_code=429,
                        message=f'Your system has been blocked because of sending lots of requests. You can try again in {convert_seconds(block_time)}.',
                        controller=f'rate_limiter',
                    )

                current_count = redis_client.get(count_key) or 0
                if int(current_count) >= limit:
                    redis_client.setex(block_key, period, path)
                    redis_client.delete(count_key)
                    raise RequestException(
                        status_code=429,
                        message=f'Your system has been blocked because of sending lots of requests. You can try again in {convert_seconds(period)}.',
                        controller=f'rate_limiter',
                    )
                else:
                    with redis_client.pipeline() as pipe:
                        try:
                            pipe.incr(count_key, 1)
                            pipe.expire(count_key, period)
                            pipe.execute()
                        except redis.exceptions.RedisError:
                            raise RequestException(
                                status_code=503,
                                message='Service temporarily unavailable.',
                                controller=f'rate_limiter',
                            )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
