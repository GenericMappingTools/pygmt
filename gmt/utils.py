"""
Utilities and common tasks for wrapping the GMT modules.
"""
import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import numpy as np

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

    Make sure all arguments have been previously converted to a string
    representation using the ``kwargs_to_strings`` decorator.

    Any lists or tuples left will be interpreted as multiple entries for the
    same command line argument. For example, the kwargs entry ``'B': ['xa',
    'yaf']`` will be converted to ``-Bxa -Byaf`` in the argument string.

    Parameters
    ----------
    kwargs : dict
        Parsed keyword arguments.

    Returns
    -------
    args : str
        The space-delimited argument string with '-' inserted before each
        keyword. The arguments are sorted alphabetically.

    Examples
    --------

    >>> print(build_arg_string(dict(R='1/2/3/4', J="X4i", P='', E=200)))
    -E200 -JX4i -P -R1/2/3/4
    >>> print(build_arg_string(dict(R='1/2/3/4', J="X4i",
    ...                             B=['xaf', 'yaf', 'WSen'],
    ...                             I=('1/1p,blue', '2/0.25p,blue'))))
    -Bxaf -Byaf -BWSen -I1/1p,blue -I2/0.25p,blue -JX4i -R1/2/3/4

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


class GMTTempFile():
    """
    Context manager for creating closed temporary files.

    This class does not return a file-like object. So, you can't do
    ``for line in GMTTempFile()``, for example, or pass it to things that
    need file objects.

    Parameters
    ----------
    prefix : str
        The temporary file name begins with the prefix.
    suffix : str
        The temporary file name ends with the suffix.

    Examples
    --------
    >>> import numpy as np
    >>> with GMTTempFile() as tmpfile:
    ...     # write data to temporary file
    ...     x = y = z = np.arange(0, 3, 1)
    ...     np.savetxt(tmpfile.name, (x, y, z), fmt='%.1f')
    ...     lines = tmpfile.read()
    ...     print(lines)
    ...     nx, ny, nz = tmpfile.loadtxt(unpack=True, dtype=float)
    ...     print(nx, ny, nz)
    0.0 1.0 2.0
    0.0 1.0 2.0
    0.0 1.0 2.0
    <BLANKLINE>
    [0. 0. 0.] [1. 1. 1.] [2. 2. 2.]
    """
    def __init__(self, prefix="gmt-python-", suffix=".txt"):
        args = dict(prefix=prefix, suffix=suffix, delete=False)
        with NamedTemporaryFile(**args) as tmpfile:
            self.name = tmpfile.name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if os.path.exists(self.name):
            os.remove(self.name)

    def read(self, keep_tabs=False):
        """
        Read the entire contents of the file as a Unicode string.

        Parameters
        ----------
        keep_tabs : bool
            If False, replace the tabs that GMT uses with spaces.

        Returns
        -------
        content : str
            Content of the temporary file as a Unicode string.
        """
        with open(self.name) as tmpfile:
            content = tmpfile.read()
            if not keep_tabs:
                content = content.replace('\t', ' ')
            return content

    def loadtxt(self, **kwargs):
        """
        Load data from the temporary file using numpy.loadtxt.

        Parameters
        ----------
        kwargs : dict
            Any keyword arguments that can be passed to numpy.loadtxt.

        Returns
        -------
        ndarray
            Data read from the text file.

        """
        return np.loadtxt(self.name, **kwargs)
