"""
The PyGMT alias system to convert PyGMT's long-form arguments to GMT's short-form.
"""

import dataclasses
import warnings
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.helpers.utils import is_nonstr_iter, sequence_join


def _to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    mapping: Mapping | None = None,
    separator: Literal["/", ","] | None = None,
    size: int | Sequence[int] | None = None,
    ndim: int = 1,
    name: str | None = None,
) -> str | list[str] | None:
    """
    Convert any value to a string, a sequence of strings or None.

    The general rules are:

    - ``None``/``False`` will be converted to ``None``.
    - ``True`` will be converted to an empty string.
    - A sequence will be joined by the separator if a separator is provided. Otherwise,
      each item in the sequence will be converted to a string and a sequence of strings
      will be returned. It's also possible to validate the size and dimension of the
      sequence.
    - Any other type of values will be converted to a string if possible.

    If a mapping dictionary is provided, the value will be converted to the short-form
    string that GMT accepts (e.g., mapping PyGMT's long-form argument ``"high"`` to
    GMT's short-form argument ``"h"``).

    An optional prefix (e.g., `"+o"`) can be added to the beginning of the converted
    string.

    To avoid extra overhead, this function does not validate parameter combinations. For
    example, if ``value`` is a sequence but ``separator`` is not specified, the function
    will return a sequence of strings. In this case, ``prefix`` has no effect, but the
    function does not check for such inconsistencies. The maintainer should ensure that
    the parameter combinations are valid.

    Parameters
    ----------
    value
        The value to convert.
    prefix
        The string to add as a prefix to the returned value.
    mapping
        A mapping dictionary to map PyGMT's long-form arguments to GMT's short-form.
    separator
        The separator to use if the value is a sequence.
    size
        Expected size of the 1-D sequence. It can be either an integer or a sequence of
        integers. If an integer, it is the expected size of the 1-D sequence. If it is a
        sequence, it is the allowed sizes of the 1-D sequence.
    ndim
        The expected maximum number of dimensions of the sequence.
    name
        The name of the parameter to be used in the error message.

    Returns
    -------
    ret
        The converted value.

    Examples
    --------
    >>> _to_string("text")
    'text'
    >>> _to_string(12)
    '12'
    >>> _to_string(True)
    ''
    >>> _to_string(False)
    >>> _to_string(None)

    >>> _to_string("text", prefix="+a")
    '+atext'
    >>> _to_string(12, prefix="+a")
    '+a12'
    >>> _to_string(True, prefix="+a")
    '+a'
    >>> _to_string(False, prefix="+a")
    >>> _to_string(None, prefix="+a")

    >>> _to_string("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    'a'
    >>> _to_string("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    Traceback (most recent call last):
    ...
    pygmt...GMTValueError: Invalid value: 'invalid'. Expected one of: 'mean', ...

    >>> _to_string((12, 34), separator="/")
    '12/34'
    >>> _to_string(("12p", "34p"), separator=",")
    '12p,34p'
    >>> _to_string(("12p", "34p"), prefix="+o", separator="/")
    '+o12p/34p'

    >>> _to_string(["xaf", "yaf", "WSen"])
    ['xaf', 'yaf', 'WSen']
    """
    # None and False are converted to None.
    if value is None or value is False:
        return None
    # True is converted to an empty string with the optional prefix.
    if value is True:
        return f"{prefix}"
    # Any non-sequence value is converted to a string.
    if not is_nonstr_iter(value):
        if mapping:
            if value not in mapping and value not in mapping.values():
                raise GMTValueError(
                    value,
                    description="value for parameter {name!r}" if name else "value",
                    choices=mapping.keys(),
                )
            value = mapping.get(value, value)
        return f"{prefix}{value}"

    # Return the sequence if separator is not specified for options like '-B'.
    # True in a sequence will be converted to an empty string.
    if separator is None:
        return [str(item) if item is not True else "" for item in value]
    # Join the sequence of values with the separator.
    # "prefix" and "mapping" are ignored. We can enable them when needed.
    _value = sequence_join(value, separator=separator, size=size, ndim=ndim, name=name)
    return f"{prefix}{_value}"


@dataclasses.dataclass
class Alias:
    """
    Class for aliasing a PyGMT parameter to a GMT option or a modifier.

    Attributes
    ----------
    value
        The value of the alias.
    name
        The name of the parameter to be used in the error message.
    prefix
        The string to add as a prefix to the returned value.
    mapping
        A mapping dictionary to map PyGMT's long-form arguments to GMT's short-form.
    separator
        The separator to use if the value is a sequence.
    size
        Expected size of the 1-D sequence. It can be either an integer or a sequence of
        integers. If an integer, it is the expected size of the 1-D sequence. If it is a
        sequence, it is the allowed size of the 1-D sequence.
    ndim
        The expected maximum number of dimensions of the sequence.

    Examples
    --------
    >>> par = Alias((3.0, 3.0), prefix="+o", separator="/")
    >>> par._value
    '+o3.0/3.0'

    >>> par = Alias("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    >>> par._value
    'a'

    >>> par = Alias(["xaf", "yaf", "WSen"])
    >>> par._value
    ['xaf', 'yaf', 'WSen']
    """

    value: Any
    name: str | None = None
    prefix: str = ""
    mapping: Mapping | None = None
    separator: Literal["/", ","] | None = None
    size: int | Sequence[int] | None = None
    ndim: int = 1

    @property
    def _value(self) -> str | list[str] | None:
        """
        The value of the alias as a string, a sequence of strings or None.
        """
        return _to_string(
            value=self.value,
            name=self.name,
            prefix=self.prefix,
            mapping=self.mapping,
            separator=self.separator,
            size=self.size,
            ndim=self.ndim,
        )


class AliasSystem:
    """
    Alias system for converting long-form PyGMT parameters to GMT short-form options.

    This class is initialized with keyword arguments, where each key is a GMT option
    flag, and the corresponding value is an ``Alias`` object or a list of ``Alias``
    objects.

    The class provides the ``kwdict`` attribute, which is a dictionary mapping each GMT
    option flag to its current value. The value can be a string or a list of strings.
    This keyword dictionary can then be passed to the ``build_arg_list`` function.

    Examples
    --------
    >>> from pygmt.alias import Alias, AliasSystem
    >>> from pygmt.helpers import build_arg_list
    >>>
    >>> def func(
    ...     par0, par1=None, par2=None, frame=False, repeat=None, panel=None, **kwargs
    ... ):
    ...     alias = AliasSystem(
    ...         A=[
    ...             Alias(par1, name="par1"),
    ...             Alias(par2, name="par2", prefix="+o", separator="/"),
    ...         ],
    ...         B=Alias(frame, name="frame"),
    ...         D=Alias(repeat, name="repeat"),
    ...         c=Alias(panel, name="panel", separator=","),
    ...     )
    ...     return build_arg_list(alias.kwdict | kwargs)
    >>> func(
    ...     "infile",
    ...     par1="mytext",
    ...     par2=(12, 12),
    ...     frame=True,
    ...     repeat=[1, 2, 3],
    ...     panel=(1, 2),
    ...     J="X10c/10c",
    ... )
    ['-Amytext+o12/12', '-B', '-D1', '-D2', '-D3', '-JX10c/10c', '-c1,2']
    """

    def __init__(self, **kwargs):
        """
        Initialize the alias system and create the keyword dictionary that stores the
        current parameter values.
        """
        # Keyword dictionary with an empty string as default value.
        self.kwdict = defaultdict(str)
        for option, aliases in kwargs.items():
            if not is_nonstr_iter(aliases):  # A single alias.
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

        # Dictionary mapping option flags to their alias objects.
        self._aliasdict = {}
        for option, aliases in kwargs.items():
            if not is_nonstr_iter(aliases):
                self._aliasdict[option] = [aliases.name]
            else:
                self._aliasdict[option] = [alias.name for alias in aliases]

    def merge(self, kwargs):
        """
        Merge additional keyword arguments into the existing keyword dictionary.

        This method is necessary to allow users to use the single-letter parameters for
        option flags that are not aliased.
        """
        # Loop over short-form parameters passed in kwargs.
        for short_param, value in kwargs.items():
            if self._aliasdict.get(short_param):
                long_form = ", ".join(repr(r) for r in self._aliasdict.get(short_param))

            # Long-form exists and is already given.
            if short_param in self.kwdict and self.kwdict[short_param] is not None:
                msg = f"Parameters in short-form {short_param!r} and long-form {long_form} can't coexist."
                raise GMTInvalidInput(msg)

            # Long-form exists, but not given.
            if short_param in self._aliasdict:
                msg = (
                    f"Short-form parameter {short_param!r} is not recommended. "
                    f"Use long-form parameter {long_form} instead."
                )
                warnings.warn(msg, category=SyntaxWarning, stacklevel=2)
            self.kwdict[short_param] = value
        return self
