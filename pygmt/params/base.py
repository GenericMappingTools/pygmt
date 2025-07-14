"""
Base class for common parameters shared in PyGMT.
"""


class BaseParam:
    """
    Base class for parameters in PyGMT.

    To define a new parameter class, inherit from this class and define the attributes
    that correspond to the parameters you want to include. The class should also
    implement the ``_aliases`` property, which returns a list of ``Alias`` objects. Each
    ``Alias`` object represents a parameter and its value, and the ``__str__`` method
    will concatenate these values into a single string that can be passed to GMT.

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

    >>> var = Test(par1="val1", par2="val2", par3=("val3a", "val3b"))
    >>> str(var)
    'val1+aval2+bval3a/val3b'
    >>> repr(var)
    "Test(par1='val1', par2='val2', par3=('val3a', 'val3b'))"
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
