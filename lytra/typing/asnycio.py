"""Utilities to help with asyncio type detenction."""

import inspect
from collections.abc import Awaitable, Coroutine
from typing import Any, Callable, ParamSpec, TypeVar

from typing_extensions import TypeIs

T = TypeVar("T")
P = ParamSpec("P")
type AsyncCallable[**P, T] = Callable[P, Coroutine[Any, Any, T]]


def is_awaitable(obj: Any) -> TypeIs[Awaitable]:  # noqa: ANN401
    """Check whether an object is awaitable."""
    return inspect.isawaitable(obj)


def is_async_callable(c: Callable) -> TypeIs[AsyncCallable]:
    """Check whether a callable is async."""
    return inspect.iscoroutinefunction(c)
