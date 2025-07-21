"""Convenience functions for lists, iterables and sequences."""

from collections.abc import Iterable
from typing import TypeVar, overload

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")


### NOTE:
# In general, it is hard to create a fully generized flattening method.
# The main problem is, how do we decide what types of iterables to flatten.
# (e.g a string is an iterable, which yields strings)


# NOTE: this is a simple flattening of depth 2.
def flatten(itr: Iterable[Iterable[T] | None]) -> Iterable[T]:
    """Flatten a 2 level iterable, with 'None' filtering."""
    return (elem for subitr in itr if subitr is not None for elem in subitr)


def flattenl(itr: Iterable[Iterable[T] | None]) -> list[T]:
    """Flatten a 2 level iterable into a list, with 'None' filtering."""
    return [elem for subitr in itr if subitr is not None for elem in subitr]


### NOTE:
# Now we will define recursive flattening.
# To properly type this, we would need the following type expression:
# >>> type RIterable[T, Iter[X]: Iterable[X]] = T | Iter[RIterable[T]]
# However currently this is impossible due to Python's limitation with HKT.

type RIterable[T] = T | Iterable[RIterable[T]]


def rflatten(itr: Iterable[RIterable[T]], unpack_cls: type[Iterable] = list) -> Iterable[T]:
    """Flatten an iterable recursively.

    Since the types of iterables to unpack cannot (and should not) be guessed,
    the function is parametrized to include this.

    Currently fully correct typing is not possible, use with caution.

    :param itr: The iterable to flatten.
    :type itr: Iterable[RIterable[T]]
    :param unpack_cls: The class to unpack along, defaults to list
    :type unpack_cls: type[Iterable]
    :return: The iterable for the flattened iterable
    :rtype: Iterable[T]
    """
    for item in itr:
        if isinstance(item, unpack_cls):
            yield from rflatten(item, unpack_cls)
        else:
            yield item  # type: ignore


def first(itr: Iterable[T]) -> T:
    """Get the first element of an iterable."""
    iterator = iter(itr)
    return next(iterator)


### NOTE:
# An unzip function of an unknown size is currently not possible in a
# way that all types could be fully inferred.
# Reference: https://github.com/python/typing/issues/1383


@overload
def unzip(itr: Iterable[tuple[T1, T2]]) -> tuple[Iterable[T1], Iterable[T2]]: ...


@overload
def unzip(itr: Iterable[tuple]) -> tuple[Iterable, ...]: ...


def unzip(itr: Iterable[tuple]) -> tuple[Iterable, ...]:
    """Unzip a nonempty iterable of same-length tuples.

    The number of iterables to unzip into is determined by the first
    tuple of the input iterable. The length is not checked throughout
    the unzipping.
    """
    try:
        k = len(first(itr))
    except StopIteration:
        msg = "Iterator is empty, cannot unzip"
        raise ValueError(msg) from None

    return tuple((elem[i] for elem in itr) for i in range(k))


@overload
def safe_unzip(itr: Iterable[tuple[T1, T2]]) -> tuple[Iterable[T1], Iterable[T2]]: ...


@overload
def safe_unzip(itr: Iterable[tuple]) -> tuple[Iterable, ...]: ...


def safe_unzip(itr: Iterable[tuple]) -> tuple[Iterable, ...]:
    """Unzip a nonempty iterable of tuples.

    The number of iterables to unzip into is determined by the first
    tuple of the input iterable. If the k-th tuple in the iterator is
    shorter than i, the i-th iterator in the output will contain None
    as the k-th element.
    """
    try:
        k = len(first(itr))
    except StopIteration:
        msg = "Iterator is empty, cannot unzip"
        raise ValueError(msg) from None

    return tuple(
        (elem[i] if len(elem) > i else None for elem in itr)  # no-fmt
        for i in range(k)
    )


@overload
def unzipl(itr: Iterable[tuple[T1, T2]]) -> tuple[list[T1], list[T2]]: ...


@overload
def unzipl(itr: Iterable[tuple]) -> tuple[list, ...]: ...


def unzipl(itr: Iterable[tuple]) -> tuple[list, ...]:
    """Unzip a nonempty iterable of same-length tuples into lists.

    The number of iterables to unzip into is determined by the first
    tuple of the input iterable. The length is not checked throughout
    the unzipping.
    """
    try:
        k = len(first(itr))
    except StopIteration:
        msg = "Iterator is empty, cannot unzip"
        raise ValueError(msg) from None

    return tuple([elem[i] for elem in itr] for i in range(k))


@overload
def safe_unzipl(itr: Iterable[tuple[T1, T2] | tuple[T1] | tuple[()]]) -> tuple[list[T1 | None], list[T2 | None]]: ...


@overload
def safe_unzipl(itr: Iterable[tuple]) -> tuple[list, ...]: ...


def safe_unzipl(itr: Iterable[tuple]) -> tuple[list, ...]:
    """Unzip a nonempty iterable of tuples into lists.

    The number of iterables to unzip into is determined by the first
    tuple of the input iterable. If the k-th tuple in the iterator is
    shorter than i, the i-th iterator in the output will contain None
    as the k-th element.
    """
    try:
        k = len(first(itr))
    except StopIteration:
        msg = "Iterator is empty, cannot unzip"
        raise ValueError(msg) from None

    return tuple(
        [elem[i] if len(elem) > i else None for elem in itr]  # no-fmt
        for i in range(k)
    )
