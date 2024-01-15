"""
Alias system to convert PyGMT parameters to GMT options.
"""
import inspect
from collections import defaultdict
from typing import NamedTuple

from pygmt.helpers import is_nonstr_iter


class Alias(NamedTuple):
    """
    Alias system for mapping a PyGMT parameter to its equivalent GMT option string.

    Attributes
    ----------
    name : str
        PyGMT parameter name.
    flag : str
        GMT single-letter option flag.
    modifier : str
        GMT option modifier. Can be None.
    separator : str
        Separator to join the iterable argument into a string.
    """

    name: str
    flag: str
    modifier: str
    separator: str


def convert_aliases():
    """
    Convert PyGMT parameters to GMT options.

    The caller function must have the special variable ``_aliases`` defined.

    Examples
    --------
    >>> def module_func(**kwargs):
    ...     _aliases = [
    ...         Alias("par1", "A", "", ""),
    ...         Alias("par2", "B", "", "/"),
    ...         Alias("par3", "C", "", ","),
    ...         Alias("pard1", "D", "", ""),
    ...         Alias("pard2", "D", "+a", ""),
    ...         Alias("pard3", "D", "+b", ","),
    ...         Alias("pard4", "D", "+c", "/"),
    ...     ]
    ...     options = convert_aliases()
    ...     print(options)
    >>>
    >>> module_func(
    ...     par1="value1",
    ...     par2=[1, 2, 3, 4],
    ...     par3=[0, 1],
    ...     pard1="value2",
    ...     pard2="value3",
    ...     pard3=[1, 2, 3, 4],
    ...     pard4=[1, 2, 3, 4],
    ... )
    {'A': 'value1', 'B': '1/2/3/4', 'C': '0,1', 'D': 'value2+avalue3+b1,2,3,4+c1/2/3/4'}
    """
    # Get the local namespace of the caller function
    p_locals = inspect.currentframe().f_back.f_locals
    params = p_locals.pop("kwargs", {}) | p_locals

    # Define a dict to store GMT option flags and arguments
    kwdict = defaultdict(str)  # default value is an empty string
    for alias in p_locals.get("_aliases"):
        value = params.get(alias.name)
        if is_nonstr_iter(value):
            if alias.separator != "":
                value = alias.separator.join(str(item) for item in value)
            else:
                value = ""
        elif value in (None, False):  # None or False are skipped
            continue
        elif value is True:  # Convert True to an empty string
            value = ""
        kwdict[alias.flag] += f"{alias.modifier}{value}"
    return dict(kwdict)
