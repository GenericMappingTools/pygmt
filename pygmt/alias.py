"""
Alias system that converts PyGMT long-form parameters to GMT short-form options.
"""

import dataclasses
import inspect
from collections import defaultdict
from typing import Any

from pygmt.helpers.utils import is_nonstr_iter


def value_to_string(value, prefix="", separator=""):
    """
    Convert any value to a string.

    Examples
    --------
    >>> value_to_string("text")
    'text'
    >>> value_to_string((12, 34), "", "/")
    '12/34'
    >>> value_to_string(("12p", "34p"), "", ",")
    '12p,34p'
    >>> value_to_string(("12p", "34p"), "+o", "/")
    '+o12p/34p'
    >>> value_to_string(True)
    ''
    >>> value_to_string(False)
    >>> value_to_string(None)
    >>> value_to_string(["xaf", "yaf", "WSen"])
    ['xaf', 'yaf', 'WSen']
    """
    # None or False means the parameter is not specified, so return None
    if value in (None, False):
        return None

    # Convert any other value type to string
    if is_nonstr_iter(value):
        # Backward compatibility taking a list as repeated option.
        value = [str(item) for item in value]
        if separator:
            value = separator.join(value)
        else:
            return value
    elif value is True:
        value = ""
    return f"{prefix}{value}"


@dataclasses.dataclass
class Alias:
    """
    Alias.
    """

    name: str
    prefix: str = ""
    separator: str = ""
    value: Any = None


class AliasSystem:
    """
    Alias system.

    Examples
    --------

    >>> def func(par0, par1=None, par2=None, par3=None, par4=None, frame=False):
    ...     alias = AliasSystem(
    ...         A=[
    ...             ("par1", ""),
    ...             ("par2", "+j"),
    ...             ("par3", "+o", "/"),
    ...         ],
    ...         B=[("frame",)],
    ...     )
    ...
    ...     alias.apply()
    ...     return str(alias)
    >>> func("infile", par1="mytext", par3=(12, 12), frame=True)
    '-Amytext+o12/12 -B'
    """

    def __init__(self, **kwargs):
        self.options = {}
        for option, aliases in kwargs.items():
            self.options[option] = [Alias(*alias) for alias in aliases]

    def apply(self):
        """
        Apply to store current parameter values to the alias system.
        """
        p_locals = inspect.currentframe().f_back.f_locals
        p_kwargs = p_locals.get("kwargs", {})
        params = p_locals | p_kwargs
        for option, aliases in self.options.items():
            for alias in aliases:
                alias.value = params.get(alias.name)

    def todict(self):
        """
        Convert the current parameter values into keyword dictionary.
        """
        kwdict = defaultdict(str)  # default value is an empty string
        for option, aliases in self.options.items():
            for alias in aliases:
                value = value_to_string(alias.value, alias.prefix, alias.separator)
                if value is None:
                    continue
                kwdict[option] += value
        return kwdict

    def __str__(self):
        """
        String representation of the alias system.
        """
        kwdict = self.todict()
        return " ".join(f"-{key}{value}" for key, value in kwdict.items())
