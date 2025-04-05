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
    ...     @property
    ...     def _aliases(self):
    ...         return [
    ...             Alias(self.par1),
    ...             Alias(self.par2, prefix="+a"),
    ...             Alias(self.par3, prefix="+b", separator="/"),
    ...         ]
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
        return "".join(
            [alias._value for alias in self._aliases if alias._value is not None]
        )

    def __repr__(self):
        """
        String representation of the object.
        """
        params = ", ".join(f"{k}={v!r}" for k, v in vars(self).items() if v is not None)
        return f"{self.__class__.__name__}({params})"
