"""
Alias system that converts PyGMT parameters to GMT short-form options.
"""

import dataclasses
import inspect
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from pygmt.helpers.utils import is_nonstr_iter


def value_to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    separator: str | None = None,
    mapping: bool | Mapping = False,
) -> str | Sequence[str] | None:
    """
    Convert any value to a string, a sequence of strings or None.

    ``None`` or ``False`` will be converted to ``None``.

    ``True`` will be converted to an empty string. If the value is a sequence and a
    separator is provided, the sequence will be joined by the separator. Otherwise, each
    item in the sequence will be converted to a string and a sequence of strings will be
    returned. Any other value will be converted to a string if possible. It also tried
    to convert PyGMT's long-form arguments into GMT's short-form arguments by using a
    mapping dictionary or simply using the first letter of the long-form arguments.

    An optional prefix (e.g., `"+o"`) can be added to the beginning of the converted
    string.

    Parameters
    ----------
    value
        The value to convert.
    prefix
        The string to add as a prefix to the value.
    separator
        The separator to use if the value is a sequence.
    mapping
        Map long-form arguments to GMT's short-form arguments. If ``True``, will use the
        first letter of the long-form arguments.

    Examples
    --------
    >>> value_to_string("text")
    'text'
    >>> value_to_string(12)
    '12'
    >>> value_to_string((12, 34), separator="/")
    '12/34'
    >>> value_to_string(("12p", "34p"), separator=",")
    '12p,34p'
    >>> value_to_string(("12p", "34p"), prefix="+o", separator="/")
    '+o12p/34p'
    >>> value_to_string(True)
    ''
    >>> value_to_string(True, prefix="+a")
    '+a'
    >>> value_to_string(False)
    >>> value_to_string(None)
    >>> value_to_string(["xaf", "yaf", "WSen"])
    ['xaf', 'yaf', 'WSen']
    >>> value_to_string("high", mapping=True)
    'h'
    >>> value_to_string("low", mapping=True)
    'l'
    >>> value_to_string("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    'a'
    >>> value_to_string("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    'invalid'
    """
    # None or False means the parameter is not specified, returns None.
    if value is None or value is False:
        return None
    # True means the parameter is specified, returns an empty string with the optional
    # prefix ('prefix' defaults to an empty string!).
    if value is True:
        return f"{prefix}"

    # Convert any value to a string or a sequence of strings
    if is_nonstr_iter(value):  # Is a sequence
        value = [str(item) for item in value]  # Convert to a sequence of strings
        if separator is None:
            # A sequence is given but separator is not specified. In this case, return
            # a sequence of strings, which is used to support repeated GMT options like
            # '-B'. 'prefix' makes no sense here, so ignored.
            return value
        value = separator.join(value)  # Join the sequence by the specified separator.
    if mapping:  # Mapping long-form arguments to short-form arguments
        value = value[0] if mapping is True else mapping.get(value, value)
    return f"{prefix}{value}"


@dataclasses.dataclass
class Alias:
    """
    Class for aliasing a PyGMT parameter to a GMT option or a modifier.

    Attributes
    ----------
    name
        Parameter name.
    prefix
        String to add at the beginning of the value.
    separator
        Separator to use if the value is a sequence.
    mapping
        Map long-form arguments to GMT's short-form arguments. If ``True``, will use the
        first letter of the long-form arguments.
    value
        Value of the parameter.

    Examples
    --------
    >>> par = Alias("offset", prefix="+o", separator="/")
    >>> par.value = (2.0, 2.0)
    >>> par.value
    '+o2.0/2.0'
    >>> par = Alias("frame")
    >>> par.value = ("xaf", "yaf", "WSen")
    >>> par.value
    ['xaf', 'yaf', 'WSen']
    """

    name: str
    prefix: str = ""  # Default to an empty string to simplify code logic.
    separator: str | None = None
    mapping: bool | Mapping = False
    _value: Any = None

    @property
    def value(self) -> str | Sequence[str] | None:
        """
        Get the value of the parameter.
        """
        return self._value

    @value.setter
    def value(self, new_value: Any):
        """
        Set the value of the parameter.

        Internally, the value is converted to a string, a sequence of strings or None.
        """
        self._value = value_to_string(
            new_value, self.prefix, self.separator, self.mapping
        )


class AliasSystem:
    """
    Alias system to convert PyGMT parameter into a keyword dictionary for GMT options.

    The AliasSystem class is initialized by keyword arguments where the key is the GMT
    single-letter option flag and the value is one or a list of ``Alias`` objects.

    The ``kwdict`` property is a keyword dictionary that stores the current parameter
    values. The key of the dictionary is the GMT single-letter option flag, and the
    value is the corresponding value of the option. The value can be a string or a
    sequence of strings, or None. The keyword dictionary can be passed to the
    ``build_arg_list`` function.

    Need to note that the ``kwdict`` property is dynamically computed from the current
    values of parameters. So, don't change it and avoid accessing it multiple times.

    Examples
    --------
    >>> from pygmt.alias import Alias, AliasSystem
    >>> from pygmt.helpers import build_arg_list
    >>>
    >>> def func(
    ...     par0,
    ...     par1=None,
    ...     par2=None,
    ...     par3=None,
    ...     par4=None,
    ...     frame=False,
    ...     panel=None,
    ...     **kwargs,
    ... ):
    ...     alias = AliasSystem(
    ...         A=[
    ...             Alias("par1"),
    ...             Alias("par2", prefix="+j"),
    ...             Alias("par3", prefix="+o", separator="/"),
    ...         ],
    ...         B=Alias("frame"),
    ...         c=Alias("panel", separator=","),
    ...     )
    ...     return build_arg_list(alias.kwdict)
    >>> func(
    ...     "infile",
    ...     par1="mytext",
    ...     par3=(12, 12),
    ...     frame=True,
    ...     panel=(1, 2),
    ...     J="X10c/10c",
    ... )
    ['-Amytext+o12/12', '-B', '-JX10c/10c', '-c1,2']
    """

    def __init__(self, **kwargs):
        """
        Initialize as a dictionary of GMT options and their aliases.
        """
        self.options = {}
        for option, aliases in kwargs.items():
            if isinstance(aliases, list):
                self.options[option] = aliases
            elif isinstance(aliases, str):  # Support shorthand like 'J="projection"'
                self.options[option] = [Alias(aliases)]
            else:
                self.options[option] = [aliases]

    @property
    def kwdict(self):
        """
        A keyword dictionary that stores the current parameter values.
        """
        # Get the local variables from the calling function.
        p_locals = inspect.currentframe().f_back.f_locals
        # Get parameters/arguments from **kwargs of the calling function.
        p_kwargs = p_locals.pop("kwargs", {})

        params = p_locals | p_kwargs
        # Default value is an empty string to simplify code logic.
        kwdict = defaultdict(str)
        for option, aliases in self.options.items():
            for alias in aliases:
                alias.value = params.get(alias.name)
                # value can be a string, a sequence of strings or None.
                if alias.value is None:
                    continue

                # Special handing of repeatable parameter like -B/frame.
                if is_nonstr_iter(alias.value):
                    kwdict[option] = alias.value
                    # A repeatable option should have only one alias, so break.
                    break

                kwdict[option] += alias.value

        # Support short-form parameter names specified in kwargs.
        # Short-form parameters can be either one-letter (e.g., '-B'), or two-letters
        # (e.g., '-Td').
        for option, value in p_kwargs.items():
            # Here, we assume that long-form parameters specified in kwargs are longer
            # than two characters. Sometimes, we may use parameter like 'az', but it's
            # not specified in kwargs. So, the assumption is still valid.
            if len(option) > 2:
                continue

            # Two cases for short-form parameters:
            #
            # If it has an alias and the long-form parameter is also specified, (e.g.,
            # 'projection="X10c", J="X10c"'), then we silently ignore the short-form
            # parameter.
            #
            # If it has an alias but the long-form parameter is not specified, or it
            # doesn't has an alias, then we use the value of the short-form parameter.
            if option not in self.options or option not in kwdict:
                kwdict[option] = value
        return kwdict
