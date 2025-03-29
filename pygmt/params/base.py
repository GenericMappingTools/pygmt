"""
Base class for PyGMT common parameters.
"""


class BaseParam:
    """
    Base class for PyGMT common parameters.

    Examples
    --------
    >>> from typing import Any
    >>> import dataclasses
    >>> from pygmt.params.base import BaseParam
    >>> from pygmt.alias import Alias
    >>>
    >>> @dataclasses.dataclass(repr=False)
    ... class Test(BaseParam):
    ...     par1: Any = None
    ...     par2: Any = None
    ...     par3: Any = None
    ...
    ...     _aliases = [
    ...         Alias("par1"),
    ...         Alias("par2", prefix="+a"),
    ...         Alias("par3", prefix="+b", separator="/"),
    ...     ]
    >>> var = Test(par1="val1")
    >>> str(var)
    'val1'
    >>> repr(var)
    "Test(par1='val1')"
    """

    def __str__(self):
        """
        String representation of the object that can be passed to GMT directly.
        """
        for alias in self._aliases:
            alias.value = getattr(self, alias.name)
        return "".join(
            [alias.value for alias in self._aliases if alias.value is not None]
        )

    def __repr__(self):
        """
        String representation of the object.
        """
        string = []
        for alias in self._aliases:
            value = getattr(self, alias.name)
            if value is None or value is False:
                continue
            string.append(f"{alias.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(string)})"
