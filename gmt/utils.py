"""
Utilities and common tasks for wrapping the GMT modules.
"""
from contextlib import contextmanager

from .exceptions import GMTError


def data_kind(data, x, y):
    """
    Check what kind of data is provided to a module.

    Possible types:

    * a file name provided as 'data'
    * a matrix provided as 'data'
    * 1D arrays x and y

    Arguments should be ``None`` is not used. If doesn't fit any of these
    categories (or fits more than one), will raise an exception.

    Parameters
    ----------
    data : str, 2d array, or None
       Data file name or numpy array.
    x, y : 1d arrays or None
        x and y columns as numpy arrays.

    Returns
    -------
    kind : str
        One of: ``'file'``, ``'matrix'``, ``'vectors'``.

    Examples
    --------

    >>> import numpy as np
    >>> data_kind(data=None, x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)), x=None, y=None)
    'matrix'
    >>> data_kind(data='my-data-file.txt', x=None, y=None)
    'file'
    >>> data_kind(data=None, x=None, y=None)
    Traceback (most recent call last):
        ...
    gmt.exceptions.GMTError: No input data provided.
    >>> data_kind(data='data.txt', x=np.array([1, 2]), y=np.array([4, 5]))
    Traceback (most recent call last):
        ...
    gmt.exceptions.GMTError: Too much data. Use either data or x and y.
    >>> data_kind(data='data.txt', x=np.array([1, 2]), y=None)
    Traceback (most recent call last):
        ...
    gmt.exceptions.GMTError: Too much data. Use either data or x and y.
    >>> data_kind(data=None, x=np.array([1, 2]), y=None)
    Traceback (most recent call last):
        ...
    gmt.exceptions.GMTError: Must provided both x and y.

    """
    if data is None and x is None and y is None:
        raise GMTError('No input data provided.')
    if data is not None and (x is not None or y is not None):
        raise GMTError('Too much data. Use either data or x and y.')
    if data is None and (x is None or y is None):
        raise GMTError('Must provided both x and y.')

    if isinstance(data, str):
        kind = 'file'
    elif data is not None:
        kind = 'matrix'
    else:
        kind = 'vectors'
    return kind


@contextmanager
def dummy_context(arg):
    """
    Dummy context manager.

    Does nothing when entering or exiting a ``with`` block and yields the
    argument passed to it.

    Useful when you have a choice of context managers but need one that does
    nothing.

    Parameters
    ----------
    arg : anything
        The argument that will be returned by the context manager.

    Examples
    --------

    >>> with dummy_context('some argument') as temp:
    ...     print(temp)
    some argument

    """
    yield arg


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
    >>> print(build_arg_string(dict(B=['xaf', 'yaf', 'WSen'],
    ...                             I=['1/1p,blue', '2/0.25p,blue'])))
    -Bxaf -Byaf -BWSen -I1/1p,blue -I2/0.25p,blue

    """
    sorted_args = []
    for key in sorted(kwargs):
        if is_nonstr_iter(kwargs[key]):
            for value in kwargs[key]:
                sorted_args.append('-{}{}'.format(key, value))
        else:
            sorted_args.append('-{}{}'.format(key, kwargs[key]))

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
