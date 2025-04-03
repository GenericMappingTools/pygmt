"""
PyGMT's alias system for converting PyGMT parameters to GMT short-form options.
"""

import dataclasses
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pygmt.helpers.utils import is_nonstr_iter


def to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    separator: Literal["/", ","] | None = None,
    mapping: bool | Mapping = False,
) -> str | Sequence[str] | None:
    """
    Convert any value to a string, a sequence of strings or None.

    - ``None`` or ``False`` will be converted to ``None``.
    - ``True`` will be converted to an empty string.
    - A sequence will be joined by the separator if a separator is provided. Otherwise,
      each item in the sequence will be converted to a string and a sequence of strings
      will be returned.
    - Any other value will be converted to a string if possible.

    If a mapping dictionary is provided, the value will be converted to the short-form
    string that GMT accepts (e.g., mapping PyGMT long-form argument ``"high"`` to GMT's
    short-form argument ``"h"``). If the value is not in the mapping dictionary, the
    original value will be returned. If ``mapping`` is set to ``True``, the first letter
    of the long-form argument will be used as the short-form argument.

    An optional prefix (e.g., `"+o"`) can be added to the beginning of the converted
    string.

    Need to note that this function doesn't check if the given parameters are valid, to
    avoid the overhead of checking. For example, if ``value`` is a sequence but
    ``separator`` is not specified, a sequence of strings will be returned. ``prefix``
    makes no sense here, but this function won't check it.

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
    # Return None if the value is None or False.
    if value is None or value is False:
        return None
    # Return an empty string if the value is True. We don't have to check 'prefix' since
    # it defaults to an empty string!
    if value is True:
        return f"{prefix}"

    # Convert any value to a string or a sequence of strings.
    if is_nonstr_iter(value):  # Is a sequence.
        value = [str(item) for item in value]  # Convert to a sequence of strings
        if separator is None:
            # A sequence is given but separator is not specified. Return a sequence of
            # strings, to support repeated GMT options like '-B'. 'prefix' makes no
            # sense and is ignored.
            return value
        value = separator.join(value)  # Join the sequence by the separator.
    elif mapping:  # Mapping long-form arguments to short-form arguments.
        value = value[0] if mapping is True else mapping.get(value, value)
    # Return the final string with the optional prefix.
    return f"{prefix}{value}"


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
    >>> par.value
    '+o3.0/3.0'

    >>> par = Alias(["xaf", "yaf", "WSen"])
    >>> par.value
    ['xaf', 'yaf', 'WSen']
    """

    def __init__(
        self,
        value: Any,
        prefix: str = "",
        separator: Literal["/", ","] | None = None,
        mapping: bool | Mapping = False,
    ):
        self.value = to_string(
            value=value, prefix=prefix, separator=separator, mapping=mapping
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
        Initialize as a dictionary of GMT options and their aliases.
        """
        self.options = {}
        for option, aliases in kwargs.items():
            match aliases:
                case list():
                    self.options[option] = aliases
                case _:
                    self.options[option] = [aliases]

    @property
    def kwdict(self):
        """
        A keyword dictionary that stores the current parameter values.
        """
        # Default value is an empty string to simplify code logic.
        kwdict = defaultdict(str)
        for option, aliases in self.options.items():
            for alias in aliases:
                # value can be a string, a sequence of strings or None.
                if alias.value is None:
                    continue
                # Special handing of repeatable parameter like -B/frame.
                if is_nonstr_iter(alias.value):
                    kwdict[option] = alias.value
                    # A repeatable option should have only one alias, so break.
                    break

                kwdict[option] += alias.value
        return kwdict
