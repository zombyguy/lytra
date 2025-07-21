"""Turn any awaitable into a context which runs it on entering."""

from collections.abc import Awaitable
from types import TracebackType


class AwaitableAsContext(Awaitable):
    """Mixin to turn an awaitable into a context which awaits it on entering."""

    async def __aenter__(self) -> None:
        """Enter the context."""
        await self

    async def __aexit__(  # noqa: ANN204
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        """Exit the context."""
        return
