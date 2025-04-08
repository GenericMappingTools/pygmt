"""
PyGMT's alias system for converting PyGMT parameters to GMT short-form options.
"""

import dataclasses
from collections import defaultdict
from collections.abc import Mapping
from typing import Any, Literal

from pygmt.helpers.utils import is_nonstr_iter


def to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    separator: Literal["/", ","] | None = None,
    mapping: bool | Mapping = False,
) -> str | list[str] | None:
    """
    Convert any value to a string, a sequence of strings or None.

    The general rules are:

    - ``None``/``False`` will be converted to ``None``.
    - ``True`` will be converted to an empty string.
    - A sequence will be joined by the separator if a separator is provided. Otherwise,
      each item in the sequence will be converted to a string and a sequence of strings
      will be returned.
    - Any other type of values will be converted to a string if possible.

    If a mapping dictionary is provided, the value will be converted to the short-form
    string that GMT accepts (e.g., mapping PyGMT long-form argument ``"high"`` to GMT's
    short-form argument ``"h"``). If the value is not in the mapping dictionary, the
    original value will be returned. If ``mapping`` is set to ``True``, the first letter
    of the long-form argument will be used as the short-form argument.

    An optional prefix (e.g., `"+o"`) can be added to the beginning of the converted
    string.

    To avoid extra overhead, this function does not validate parameter combinations. For
    example, if ``value`` is a sequence but ``separator`` is not specified, the function
    will return a sequence of strings. In this case, ``prefix`` has no effect, but the
    function does not check for such inconsistencies.

    Parameters
    ----------
    value
        The value to convert.
    prefix
        The string to add as a prefix to the returned value.
    separator
        The separator to use if the value is a sequence.
    mapping
        A mapping dictionary or ``True`` to map long-form arguments to GMT's short-form
        arguments. If ``True``, will use the first letter of the long-form arguments.

    Returns
    -------
    ret
        The converted value.

    Examples
    --------
    >>> to_string("text")
    'text'
    >>> to_string(12)
    '12'
    >>> to_string((12, 34), separator="/")
    '12/34'
    >>> to_string(("12p", "34p"), separator=",")
    '12p,34p'
    >>> to_string(("12p", "34p"), prefix="+o", separator="/")
    '+o12p/34p'
    >>> to_string(True)
    ''
    >>> to_string(True, prefix="+a")
    '+a'
    >>> to_string(False)
    >>> to_string(None)
    >>> to_string(["xaf", "yaf", "WSen"])
    ['xaf', 'yaf', 'WSen']
    >>> to_string("high", mapping=True)
    'h'
    >>> to_string("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    'a'
    >>> to_string("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    'invalid'
    """
    if value is None or value is False:  # None and False are converted to None.
        return None
    if value is True:  # True is converted to an empty string with the optional prefix.
        return f"{prefix}"

    # Convert a non-sequence value to a string.
    if not is_nonstr_iter(value):
        if mapping:  # Mapping long-form arguments to short-form arguments.
            value = value[0] if mapping is True else mapping.get(value, value)
        return f"{prefix}{value}"

    # Convert a sequence of values to a sequence of strings.
    # In some cases, "prefix" and "mapping" are ignored. We can enable them when needed.
    _values = [str(item) for item in value]
    # When separator is not specified, return a sequence of strings for repeatable GMT
    # options like '-B'. Otherwise, join the sequence of strings with the separator.
    return _values if separator is None else f"{prefix}{separator.join(_values)}"


@dataclasses.dataclass
class Alias:
    """
    Class for aliasing a PyGMT parameter to a GMT option or a modifier.

    Attributes
    ----------
    value
        Value of the parameter.
    prefix
        String to add at the beginning of the value.
    separator
        Separator to use if the value is a sequence.
    mapping
        Map long-form arguments to GMT's short-form arguments. If ``True``, will use the
        first letter of the long-form arguments.

    Examples
    --------
    >>> par = Alias((3.0, 3.0), prefix="+o", separator="/")
    >>> par._value
    '+o3.0/3.0'

    >>> par = Alias(["xaf", "yaf", "WSen"])
    >>> par._value
    ['xaf', 'yaf', 'WSen']

    >>> par = Alias("high", mapping=True)
    >>> par._value
    'h'

    >>> par = Alias("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    >>> par._value
    'a'

    >>> par = Alias("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    >>> par._value
    'invalid'
    """

    value: Any
    prefix: str = ""
    separator: Literal["/", ","] | None = None
    mapping: bool | Mapping = False

    @property
    def _value(self) -> str | list[str] | None:
        """
        The value of the alias as a string, a sequence of strings or None.
        """
        return to_string(
            value=self.value,
            prefix=self.prefix,
            separator=self.separator,
            mapping=self.mapping,
        )


class AliasSystem:
    """
    Alias system for converting PyGMT parameters to GMT options.

    The AliasSystem class is initialized with keyword arguments, where each key is a GMT
    option flag, and the corresponding value is an ``Alias`` object or a list of
    ``Alias`` objects.

    The class provides the ``kwdict`` attribute, which is a dictionary mapping each GMT
    option flag to its current value. The value can be a string or a list of strings.
    This keyword dictionary can then be passed to the ``build_arg_list`` function.

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
    ...             Alias(par1),
    ...             Alias(par2, prefix="+j"),
    ...             Alias(par3, prefix="+o", separator="/"),
    ...         ],
    ...         B=Alias(frame),
    ...         c=Alias(panel, separator=","),
    ...     )
    ...     return build_arg_list(alias.kwdict | kwargs)
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
        Initialize the alias system and create the keyword dictionary that stores the
        current parameter values.
        """
        # Keyword dictionary with an empty string as default value.
        self.kwdict = defaultdict(str)

        for option, aliases in kwargs.items():
            if not is_nonstr_iter(aliases):  # Single alias.
                self.kwdict[option] = aliases._value
                continue

            for alias in aliases:  # List of aliases.
                match alias._value:
                    case None:
                        continue
                    case str():
                        self.kwdict[option] += alias._value
                    case list():
                        # A repeatable option should have only one alias, so break.
                        self.kwdict[option] = alias._value
                        break
