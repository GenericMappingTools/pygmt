"""
General class for PyGMT parameters.
"""

from pygmt.alias import value_to_string


class BaseParams:
    """
    Base class for PyGMT parameters.

    Examples
    --------
    >>> from typing import Any
    >>> import dataclasses
    >>> from pygmt.params.base import BaseParams
    >>> from pygmt.alias import Alias
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
        for alias in self.__aliases__:
            value = getattr(self, alias.name)
            alias.value = value_to_string(value, alias.prefix, alias.separator)

        return "".join(
            alias.value for alias in self.__aliases__ if alias.value is not None
        )

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
