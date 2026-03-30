"""
The PyGMT alias system to convert PyGMT's long-form arguments to GMT's short-form.
"""

import warnings
from collections import UserDict
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers.utils import is_nonstr_iter, sequence_join


def _to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    suffix: str = "",  # Default to an empty string to simplify the code logic.
    mapping: Mapping | None = None,
    sep: Literal["/", ","] | None = None,
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

    An optional prefix or suffix (e.g., `"+o"`) can be added to the beginning (or end)
    of the converted string.

    To avoid extra overhead, this function does not validate parameter combinations. For
    example, if ``value`` is a sequence but ``sep`` is not specified, the function will
    return a sequence of strings. In this case, ``prefix`` and ``suffix`` have no
    effect, but the function does not check for such inconsistencies. The maintainer
    should ensure that the parameter combinations are valid.

    Parameters
    ----------
    value
        The value to convert.
    prefix
        The string to add as a prefix to the returned value.
    suffix
        The string to add as a suffix to the returned value.
    mapping
        A mapping dictionary to map PyGMT's long-form arguments to GMT's short-form.
    sep
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

    >>> _to_string("blue", suffix="+l")
    'blue+l'
    >>> _to_string(True, suffix="+l")
    '+l'

    >>> _to_string("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    'a'
    >>> _to_string("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    Traceback (most recent call last):
    ...
    pygmt...GMTValueError: Invalid value: 'invalid'. Expected one of: 'mean', ...

    >>> _to_string((12, 34), sep="/")
    '12/34'
    >>> _to_string(("12p", "34p"), sep=",")
    '12p,34p'
    >>> _to_string(("12p", "34p"), prefix="+o", sep="/")
    '+o12p/34p'

    >>> # Works for parameters that accept Sequence and Mappable objects.
    >>> # E.g., project -Lw|lmin/lmax.
    >>> _to_string("limit", sep="/", size=2, mapping={"limit": "w"})
    'w'
    >>> _to_string((12, 34), sep="/", size=2, mapping={"limit": "w"})
    '12/34'

    >>> _to_string(["xaf", "yaf", "WSen"])
    ['xaf', 'yaf', 'WSen']

    >>> _to_string([[1, 2], [3, 4]], sep="/", ndim=2)
    ['1/2', '3/4']

    >>> import datetime
    >>> import numpy as np
    >>> import pandas as pd
    >>> import xarray as xr
    >>> _to_string(
    ...     [
    ...         datetime.date(2010, 1, 1),
    ...         datetime.datetime(2010, 3, 1),
    ...         pd.Timestamp("2015-01-01T12:00:00.123456789"),
    ...         xr.DataArray(data=np.datetime64("2005-01-01T08:00:00", "ns")),
    ...     ],
    ...     sep="/",
    ... )
    '2010-01-01/2010-03-01T00:00:00.000000/2015-01-01T12:00:00.123456/2005-01-01T08:00:00.000000000'
    """
    # None and False are converted to None.
    if value is None or value is False:
        return None
    # True is converted to an empty string with the optional prefix and suffix.
    if value is True:
        return f"{prefix}{suffix}"
    # Any non-sequence value is converted to a string.
    if not is_nonstr_iter(value):
        if mapping:
            if value not in mapping and value not in mapping.values():
                raise GMTValueError(
                    value,
                    description=f"value for parameter {name!r}" if name else "value",
                    choices=mapping.keys(),
                )
            value = mapping.get(value, value)
        return f"{prefix}{value}{suffix}"

    # Return the sequence if separator is not specified for options like '-B'.
    # True in a sequence will be converted to an empty string.
    if sep is None:
        return [str(item) if item is not True else "" for item in value]
    # Join the sequence of values with the separator.
    # "prefix", "suffix", and "mapping" are ignored. We can enable them when needed.
    _value = sequence_join(value, sep=sep, size=size, ndim=ndim, name=name)
    return _value if is_nonstr_iter(_value) else f"{prefix}{_value}{suffix}"


class Alias:
    """
    Class for aliasing a PyGMT parameter to a GMT option or a modifier.

    Parameters
    ----------
    value
        The value of the alias.
    name
        The name of the parameter to be used in the error message.
    prefix
        The string to add as a prefix to the returned value.
    suffix
        The string to add as a suffix to the returned value.
    mapping
        A mapping dictionary to map PyGMT's long-form arguments to GMT's short-form.
    sep
        The separator to use if the value is a sequence.
    size
        Expected size of the 1-D sequence. It can be either an integer or a sequence
        of integers. If an integer, it is the expected size of the 1-D sequence.
        If it is a sequence, it is the allowed sizes of the 1-D sequence.
    ndim
        The expected maximum number of dimensions of the sequence.

    Examples
    --------
    >>> par = Alias((3.0, 3.0), prefix="+o", sep="/")
    >>> par._value
    '+o3.0/3.0'

    >>> par = Alias("blue", suffix="+l")
    >>> par._value
    'blue+l'

    >>> par = Alias("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    >>> par._value
    'a'

    >>> par = Alias(["xaf", "yaf", "WSen"])
    >>> par._value
    ['xaf', 'yaf', 'WSen']
    """

    def __init__(
        self,
        value: Any,
        name: str | None = None,
        prefix: str = "",
        suffix: str = "",
        mapping: Mapping | None = None,
        sep: Literal["/", ","] | None = None,
        size: int | Sequence[int] | None = None,
        ndim: int = 1,
    ):
        self.name = name
        self.prefix = prefix
        self.suffix = suffix
        self._value = _to_string(
            value=value,
            name=name,
            prefix=prefix,
            suffix=suffix,
            mapping=mapping,
            sep=sep,
            size=size,
            ndim=ndim,
        )


class AliasSystem(UserDict):
    """
    Alias system mapping PyGMT long-form parameters to GMT short-form options.

    This class inherits from ``UserDict`` so it behaves like a dictionary and can be
    passed directly to ``build_arg_list``. It also provides ``merge`` to update the
    alias dictionary with additional keyword arguments.

    Initialize with keyword arguments where each key is a GMT option flag and each value
    is an ``Alias`` instance or a list of ``Alias`` instances. For a single ``Alias``,
    we use its ``_value`` property. For a list, we check for suffixes:

    - If any ``Alias`` has a suffix, return a list of values for repeated GMT options.
      For example, ``[Alias("blue", suffix="+l"), Alias("red", suffix="+r")]`` becomes
      ``-Cblue+l -Cred+r``.
    - Otherwise, concatenate into a single string for combined modifiers. For example,
      ``[Alias("TL", prefix="j"), Alias((1, 1), prefix="+o")]`` becomes ``jTL+o1/1``.

    ``alias._value`` is produced by ``_to_string`` and is one of: ``None``, ``str``, or
    a sequence of strings.

    - ``None`` means the parameter is not specified.
    - A sequence of strings means this is a repeatable option and can only have one
      long-form parameter.

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
    ...     repeat=None,
    ...     panel=None,
    ...     verbose=None,
    ...     **kwargs,
    ... ):
    ...     aliasdict = AliasSystem(
    ...         A=[
    ...             Alias(par1, name="par1"),
    ...             Alias(par2, name="par2", prefix="+o", sep="/"),
    ...         ],
    ...         B=Alias(frame, name="frame"),
    ...         C=[Alias(par3, suffix="+l"), Alias(par4, suffix="+r")],
    ...         D=Alias(repeat, name="repeat"),
    ...     ).add_common(
    ...         V=verbose,
    ...         c=panel,
    ...     )
    ...     aliasdict.merge(kwargs)
    ...     return build_arg_list(aliasdict)
    >>> func(
    ...     "infile",
    ...     par1="mytext",
    ...     par2=(12, 12),
    ...     par3="blue",
    ...     par4="red",
    ...     frame=True,
    ...     repeat=[1, 2, 3],
    ... )
    ['-Amytext+o12/12', '-B', '-Cblue+l', '-Cred+r', '-D1', '-D2', '-D3']
    >>> func("infile", panel=(1, 2), verbose="debug", J="X10c/10c")
    ['-JX10c/10c', '-Vd', '-c1,2']
    """

    def __init__(self, **kwargs):
        """
        Initialize the alias system as a dictionary with current parameter values.
        """
        # Store the aliases in a dictionary, to be used in the merge() method.
        self.aliasdict = kwargs

        kwdict = {}
        for option, aliases in kwargs.items():
            if isinstance(aliases, Sequence):  # A sequence of Alias objects.
                values = [alias._value for alias in aliases if alias._value is not None]
                if values:
                    # Check if any alias has suffix - if so, return as list
                    has_suffix = any(alias.suffix for alias in aliases)
                    # If has suffix and multiple values, return as list;
                    # else concatenate into a single string.
                    kwdict[option] = (
                        values if has_suffix and len(values) > 1 else "".join(values)
                    )
            elif aliases._value is not None:  # A single Alias object and not None.
                kwdict[option] = aliases._value
        super().__init__(kwdict)

    def add_common(self, **kwargs):  # noqa: PLR0912
        """
        Add common parameters to the alias dictionary.
        """
        for key, value in kwargs.items():
            match key:
                case "B":
                    # Mapping frame="none" to '-B+n'.
                    _value = "+n" if value == "none" else value
                    alias = Alias(_value, name="frame")
                case "J":
                    alias = Alias(value, name="projection")
                case "R":
                    alias = Alias(value, name="region", sep="/", size=(4, 6))
                case "V":
                    alias = Alias(
                        value,
                        name="verbose",
                        mapping={
                            "quiet": "q",
                            "error": "e",
                            "warning": "w",
                            "timing": "t",
                            "info": "i",
                            "compat": "c",
                            "debug": "d",
                        },
                    )
                case "c":
                    alias = Alias(value, name="panel", sep=",", size=2)
                case "i":
                    alias = Alias(value, name="incols", sep=",")
                case "r":
                    alias = Alias(
                        value,
                        name="registration",
                        mapping={"gridline": "g", "pixel": "p"},
                    )
                case "o":
                    alias = Alias(value, name="outcols", sep=",")
                case "p":
                    alias = Alias(value, name="perspective", sep="/", size={2, 3})
                case "t":
                    alias = Alias(value, name="transparency")
                case "x":
                    alias = Alias(value, name="cores")
                case _:
                    raise GMTValueError(key, description="common parameter")
            self.aliasdict[key] = alias
            if alias._value is not None:
                self[key] = alias._value
        return self

    def merge(self, kwargs: Mapping[str, Any]):
        """
        Update the dictionary with additional keyword arguments.

        This method is necessary to allow users to use the single-letter parameters for
        option flags that are not aliased.
        """
        # Loop over short-form parameters passed via kwargs.
        for short_param, value in kwargs.items():
            # Check if long-form parameters exist and given.
            long_param_exists = short_param in self.aliasdict
            long_param_given = short_param in self

            # Update the dictionary with the short-form parameter anyway.
            self[short_param] = value

            # Long-form parameters do not exist.
            if not long_param_exists:
                continue

            # Long-form parameters exist.
            aliases = self.aliasdict.get(short_param)
            if not isinstance(aliases, Sequence):
                aliases = [aliases]

            long_params = [v.name for v in aliases]
            long_params_text = ", ".join(
                [
                    f"{v.name!r} ({v.prefix})"
                    if v.prefix.startswith("+")
                    else f"{v.name!r}"
                    for v in aliases
                ]
            )
            msg = (
                f"Short-form parameter {short_param!r} is not recommended. "
                f"Use long-form parameter(s) {long_params_text} instead."
            )

            if long_param_given:
                raise GMTParameterError(
                    conflicts_with=(short_param, long_params), reason=msg
                )

            # Long-form parameters are not specified.
            warnings.warn(msg, category=SyntaxWarning, stacklevel=2)
        return self
