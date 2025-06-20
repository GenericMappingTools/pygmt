"""
The PyGMT alias system to convert PyGMT long-form arguments to GMT's short-form.
"""

from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.utils import is_nonstr_iter, sequence_join


def _to_string(
    value: Any,
    prefix: str = "",  # Default to an empty string to simplify the code logic.
    mapping: bool | Mapping = False,
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
    function does not check for such inconsistencies. The maintaner should ensure that
    the parameter combinations are valid.

    Parameters
    ----------
    value
        The value to convert.
    prefix
        The string to add as a prefix to the returned value.
    mapping
        A mapping dictionary or ``True`` to map long-form arguments to GMT's short-form
        arguments. If ``True``, will use the first letter of the long-form arguments.
    separator
        The separator to use if the value is a sequence.

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

    >>> _to_string("high", mapping=True)
    'h'
    >>> _to_string("mean", mapping={"mean": "a", "mad": "d", "full": "g"})
    'a'
    >>> _to_string("invalid", mapping={"mean": "a", "mad": "d", "full": "g"})
    Traceback (most recent call last):
    ...
    pygmt...GMTInvalidInput: Invalid value: 'invalid'. Valid values are: mean, ...

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
        match mapping:
            case False:
                pass
            case True:
                value = value[0]
            case Mapping():
                if value not in mapping and value not in mapping.values():
                    _name = f"Parameter {name!r}: " if name else ""
                    msg = (
                        f"{_name}Invalid value: {value!r}. "
                        f"Valid values are: {', '.join(mapping)}."
                    )
                    raise GMTInvalidInput(msg)
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
