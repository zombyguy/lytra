"""Convert between sync and async callables."""

import asyncio
from typing import Callable, ParamSpec, TypeVar

from ..typing.asnycio import (
    AsyncCallable,
    is_async_callable,
)
from .control_flow import get_running_loop

T = TypeVar("T")
P = ParamSpec("P")


def sync_to_asnyc(c: Callable[P, T]) -> AsyncCallable[P, T]:
    """Turn a synchronous callable into an asynchronous one."""

    async def async_c(*args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.to_thread(c, *args, **kwargs)

    return async_c


def to_async(c: Callable[P, T] | AsyncCallable[P, T]) -> AsyncCallable[P, T]:
    """Turn any callable into an asynchronous one."""
    if is_async_callable(c):
        return c

    return sync_to_asnyc(c)


def asnyc_to_sync(c: AsyncCallable[P, T], loop: asyncio.AbstractEventLoop | None = None) -> Callable[P, T]:
    """Turn an asynchronous callable into a synchronous one."""
    if loop is None:
        loop = get_running_loop()
    if loop is None:

        def sync_c(*args: P.args, **kwargs: P.kwargs) -> T:
            return asyncio.run(c(*args, **kwargs))

    else:

        def sync_c(*args: P.args, **kwargs: P.kwargs) -> T:
            future = asyncio.run_coroutine_threadsafe(c(*args, **kwargs), loop)
            return future.result()

    return sync_c


def to_sync(c: Callable[P, T] | AsyncCallable[P, T]) -> Callable[P, T]:
    """Turn any callable into an synchronous one."""
    if not is_async_callable(c):
        return c

    return asnyc_to_sync(c)
