"""Utility for throttling asynchronous operations."""

import asyncio
from collections.abc import Awaitable, Generator, Iterable
from typing import Any, Protocol, TypeVar

from .awaitable_context import AwaitableAsContext
from .background_tasks import execute_in_background

__all__ = [
    "EnsembleRateLimiter",
    "IRateLimiter",
    "SimpleRateLimiter",
    "apply_semaphore",
    "delayed",
]

T = TypeVar("T")


### Simple delay


async def delayed(a: Awaitable[T], t: float) -> T:
    """Add a delay before an async task.

    :param a: The awaitable to delay
    :type a: Awaitable[T]
    :param t: Delay amount (in seconds)
    :type t: float
    :return: The delayed task
    :rtype: T
    """
    await asyncio.sleep(t)
    return await a


### Semaphore


async def apply_semaphore(a: Awaitable[T], sem: asyncio.Semaphore) -> T:
    """Bind an async task to a semaphore.

    :param a: The awaitable to bind
    :type a: Awaitable[T]
    :param sem: The semaphore
    :type sem: asyncio.Semaphore
    :return: The bound awaitable
    :rtype: T
    """
    async with sem:
        return await a


### Rate limiting


class IRateLimiter(Protocol):
    """Async throttler/rate-limiter interface."""

    def __await__(self) -> Generator[Any, None, None]:
        """Await rate limiter to be available."""
        return self._acquire_and_schedule_release().__await__()

    async def _acquire_and_schedule_release(self) -> None:
        await self.acquire()
        self.schedule_release()

    async def acquire(self) -> None:
        """Await premission to progress in accordance with the rate limiting."""

    def schedule_release(self) -> None:
        """Schedule a release of the rate limiting resource.

        Called on the actual starot of the throttled process.
        (A process may acquire the lock before starting.)
        """


class SimpleRateLimiter(IRateLimiter, AwaitableAsContext):
    """Simple async throttler/rate-limiter class."""

    def __init__(self, max_tasks: int, period: float = 1) -> None:
        """Initialize the async throttler.

        :param max_tasks: Number of max tasks within a given period of time
        :type max_tasks: int
        :param period: The given period of time, in seconds, defaults to 1
        :type period: float
        """
        self.semaphore = asyncio.Semaphore(max_tasks)
        self.period = period

    async def acquire(self) -> None:  # noqa: D102
        await self.semaphore.acquire()

    def schedule_release(self) -> None:  # noqa: D102
        execute_in_background(self._delayed_release())

    async def _delayed_release(self) -> None:
        """Release the internal semaphore in 'period' seconds."""
        await asyncio.sleep(self.period)
        self.semaphore.release()


class EnsembleRateLimiter(IRateLimiter, AwaitableAsContext):
    """Throttle according to multiple rate-limiters."""

    def __init__(self, limiters: Iterable[IRateLimiter]) -> None:
        """Initialize the ensemble throttler.

        Rate-limit with multiple limiters.
        There is a "hierarchy" assumed, meaning the first limiter limits
        nased on the larges period, for the most concurrent tasks.

        :param limiters: The rate-limiters, in order
        :type limiters: Iterable[IRateLimiter]
        """
        self.limiters = limiters

    async def acquire(self) -> None:  # noqa: D102
        for limiter in self.limiters:
            await limiter.acquire()

    def schedule_release(self) -> None:  # noqa: D102
        for limiter in self.limiters:
            limiter.schedule_release()
