"""
Utilities and common tasks for wrapping the GMT modules.
"""


def build_arg_string(kwargs):
    """
    Transform keyword arguments into a GMT argument string.

    Parameters
    ----------
    kwargs : dict
        Parsed keyword arguments. Doesn't do any fancy conversions. Make sure
        all arguments can be cast to a string and inserted as is into the
        GMT argument string (that means no bools, lists, or arrays).

    Returns
    -------
    args : str
        The space-delimited argument string with '-' inserted before each
        keyword. The arguments are sorted alphabetically.

    Examples
    --------

    >>> print(build_arg_string(dict(R='1/2/3/4', J="X4i", P='', E=200)))
    -E200 -JX4i -P -R1/2/3/4

    """
    sorted_args = (
        '-{}{}'.format(key, kwargs[key])
        for key in sorted(kwargs)
    )
    arg_str = ' '.join(sorted_args)
    return arg_str


def is_nonstr_iter(value):
    """
    Check if the value is not a string but is iterable (list, tuple, array)

    Parameters
    ----------
    value
        What you want to check.

    Returns
    -------
    is_iterable : bool
        Whether it is a non-string iterable or not.

    Examples
    --------

    >>> is_nonstr_iter('abc')
    False
    >>> is_nonstr_iter(10)
    False
    >>> is_nonstr_iter([1, 2, 3])
    True
    >>> is_nonstr_iter((1, 2, 3))
    True

    """
    try:
        [item for item in value]  # pylint: disable=pointless-statement
        is_iterable = True
    except TypeError:
        is_iterable = False
    return bool(not isinstance(value, str) and is_iterable)
