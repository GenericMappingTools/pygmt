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
    ...             Alias(self.par3, prefix="+b", sep="/"),
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

    def __post_init__(self):
        """
        Post-initialization method to _validate the _aliases property.
        """
        self._validate()

    def _validate(self):
        """
        Validate the parameters of the object.

        This method should be overridden in subclasses to perform any necessary
        validation on the parameters.
        """

    @property
    def _aliases(self):
        """
        List of Alias objects representing the parameters of this class.

        This property must be implemented in subclasses to define the parameters
        and their aliases.
        """
        msg = "The _aliases property must be implemented in subclasses."
        raise NotImplementedError(msg)

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
