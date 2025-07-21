"""Executing tasks in the background."""

import asyncio
from collections.abc import Coroutine

BACKGROUND_TASKS: set[asyncio.Task] = set()


def execute_in_background(coro: Coroutine) -> None:
    """Execute a coroutine in the background, output is not retained.

    Must be called in a running asyncio loop.
    """
    task = asyncio.create_task(coro)
    BACKGROUND_TASKS.add(task)
    task.add_done_callback(BACKGROUND_TASKS.discard)
