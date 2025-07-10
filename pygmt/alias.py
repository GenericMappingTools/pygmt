"""
The PyGMT alias system to convert PyGMT's long-form arguments to GMT's short-form.
"""

from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pygmt.exceptions import GMTValueError
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
    function does not check for such inconsistencies. The maintaner should ensure that
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
