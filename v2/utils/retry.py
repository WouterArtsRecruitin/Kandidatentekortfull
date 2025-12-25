"""
Retry decorator with exponential backoff.
"""

import time
import functools
from typing import Callable, Type, Tuple
from .logging_config import get_logger

logger = get_logger("retry")


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable = None
):
    """
    Decorator that retries a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiply delay by this factor after each attempt
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Optional callback called before each retry with (attempt, exception)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(f"[RETRY] {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise

                    logger.warning(f"[RETRY] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}")

                    if on_retry:
                        on_retry(attempt, e)

                    time.sleep(delay)
                    delay *= backoff_factor

            raise last_exception

        return wrapper
    return decorator


def retry_async_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Async version of retry decorator."""
    import asyncio

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(f"[RETRY] {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise

                    logger.warning(f"[RETRY] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}")
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

            raise last_exception

        return wrapper
    return decorator
