"""Basic control flow handling functions."""

import asyncio
from collections.abc import Generator
from types import coroutine


@coroutine
def ayield() -> Generator[None, None, None]:
    """Yield control to the async loop for a cycle."""
    yield


async def ayields(k: int) -> None:
    """Yield contorl to the async loop multiple times."""
    for _ in range(k - 1):
        await ayield()


def get_running_loop() -> asyncio.AbstractEventLoop | None:
    """Return the running event loop, or None if there is none."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None
