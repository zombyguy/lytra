"""Utilities to help with types and type hinting."""

from .asnycio import (
    is_async_callable,
    is_awaitable,
)
from .unset import (
    UNSET,
    Unset,
    is_unset,
)

__all__ = [
    "UNSET",
    "Unset",
    "is_async_callable",
    "is_awaitable",
    "is_unset",
]

### NOTE:
# The higher-kindled-types concept is sadly missing from python at the moment.
# References:
# - https://sobolevn.me/2020/10/higher-kindled-types-in-python
# - https://gist.github.com/sobolevn/7f8ffd885aec70e55dd47928a1fb3e61
# - https://github.com/python/typing/issues/548
# - https://returns.readthedocs.io/en/latest/pages/hkt.html
