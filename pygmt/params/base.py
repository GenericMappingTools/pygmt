"""
General class for PyGMT parameters.
"""

from __future__ import annotations

from typing import NamedTuple

from pygmt.helpers import is_nonstr_iter


class Alias(NamedTuple):
    """
    Alias PyGMT long-form parameter to GMT single-letter option flag.
    """

    name: str
    modifier: str
    separator: str | None = None


class BaseParams:
    """
    Base class for PyGMT parameters.

    Examples
    --------
    >>> import dataclasses
    >>> from pygmt.params.base import BaseParams
    >>>
    >>> @dataclasses.dataclass(repr=False)
    ... class Test(BaseParams):
    ...     attr1: Any = None
    ...     attr2: Any = None
    ...     attr3: Any = None
    ...
    ...     __aliases__ = [
    ...         Alias("attr1", ""),
    ...         Alias("attr2", "+a"),
    ...         Alias("attr3", "+b", "/"),
    ...     ]
    >>> var = Test(attr1="val1")
    >>> str(var)
    'val1'
    >>> repr(var)
    "Test(attr1='val1')"
    """

    def __str__(self):
        """
        String representation of the object that can be passed to GMT directly.
        """
        values = []
        for alias in self.__aliases__:
            value = getattr(self, alias.name)
            if value in (None, False):
                continue
            if value is True:
                value = ""
            elif is_nonstr_iter(value):
                value = alias.separator.join(map(str, value))
            values.append(f"{alias.modifier}{value}")
        return "".join(values)

    def __repr__(self):
        """
        String representation of the object.
        """
        string = []
        for alias in self.__aliases__:
            value = getattr(self, alias.name)
            if value is None or value is False:
                continue
            string.append(f"{alias.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(string)})"
