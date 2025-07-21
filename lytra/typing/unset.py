"""The UNSET sentinel."""

from typing import Any

from typing_extensions import TypeIs

__all__ = [
    "UNSET",
    "Unset",
    "is_unset",
]


### NOTE:
# UNSET provides an alternative to None.
# It may be useful in cases where None is a usable default, but we also wanto to
# introduce a benhaviour which is unspecifiable by the user.


class Unset:
    """Class of the 'UNSET' sentinel."""

    __slots__ = []


UNSET = Unset()


def is_unset(obj: Any) -> TypeIs[Unset]:  # noqa: ANN401
    """Check whether an object is UNSET."""
    return obj is Unset
