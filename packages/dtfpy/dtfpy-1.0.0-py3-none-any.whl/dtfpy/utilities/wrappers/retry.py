import time
import asyncio
from fastapi.encoders import jsonable_encoder
from functools import wraps
from ..exception import exception_to_dict
from ..logging import leave_a_footprint


def retry(retries=3, delay=15, backoff=2, exceptions=(Exception,)):
    """
    A decorator that retries a function or method until it succeeds or a maximum number of attempts is reached.
    Supports both synchronous and asynchronous functions.

    Parameters:
    retries (int): The maximum number of attempts. Default is 3.
    delay (int): The initial delay between attempts in seconds. Default is 1.
    backoff (int): The multiplier applied to the delay after each attempt. Default is 2.
    exceptions (tuple): A tuple of exceptions to catch. Default is (Exception,).

    Returns:
    function: The wrapped function that will be retried on failure.
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    error_dict = exception_to_dict(e)
                    error_dict['kwargs'] = jsonable_encoder(kwargs)
                    error_dict['args'] = jsonable_encoder(args)
                    leave_a_footprint(
                        log_type='warning',
                        controller=func.__name__,
                        subject=f'Warning at retrying {func.__name__}',
                        message=f"An error happened while we retry to run {func.__name__} at the {attempts} attempt{'s' if attempts > 1 else ''}.",
                        payload=error_dict,
                    )
                    if attempts == retries:
                        leave_a_footprint(
                            log_type='error',
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            message=f"We could not finish the current job in the function {func.__name__}.",
                            payload=error_dict,
                        )
                        raise e
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    error_dict = exception_to_dict(e)
                    error_dict['kwargs'] = jsonable_encoder(kwargs)
                    error_dict['args'] = jsonable_encoder(args)
                    leave_a_footprint(
                        log_type='warning',
                        controller=func.__name__,
                        subject=f'Warning at retrying {func.__name__}',
                        message=f"An error happened while we retry to run {func.__name__} at the {attempts} attempt{'s' if attempts > 1 else ''}.",
                        payload=error_dict,
                    )
                    if attempts == retries:
                        leave_a_footprint(
                            log_type='error',
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            message=f"We could not finish the current job in the function {func.__name__}.",
                            payload=error_dict,
                        )
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
