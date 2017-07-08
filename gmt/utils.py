"""
Utilities and common tasks for wrapping the GMT modules.
"""
import textwrap
import functools


GMT_DOCS = 'http://gmt.soest.hawaii.edu/doc/latest'

COMMON_OPTIONS = {
    'R': '''\
        R or region : str or list
            *Required if this is the first plot command*.
            ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
            Specify the region of interest.''',
    'J': '''\
        J or projection : str
            *Required if this is the first plot command*.
            Select map projection.''',
}


def fmt_docstring(module_func):
    """
    Decorator to insert common text into module docstrings.

    Use any of these placeholders in your docstring to have them substituted:

    * ``{gmt_module_docs}``: link to the GMT docs for that module. Assumes that
      the name of the GMT module is the same as the function name.
    * ``{R}``: Parameter description for the R (region) option with 4 bounds.
    * ``{J}``: Parameter description for the J (projection) option.

    Parameters
    ----------
    module_func : function
        The module function.

    Returns
    -------
    module_func
        The same *module_func* but with the docstring formatted.

    Examples
    --------

    >>> @fmt_docstring
    ... def gmtinfo(**kwargs):
    ...     '''
    ...     My nice module.
    ...
    ...     {gmt_module_docs}
    ...
    ...     Parameters
    ...     ----------
    ...     {R}
    ...     {J}
    ...     '''
    ...     pass
    >>> print(gmtinfo.__doc__)
    <BLANKLINE>
    My nice module.
    <BLANKLINE>
    Full option list at http://gmt.soest.hawaii.edu/doc/latest/gmtinfo.html
    <BLANKLINE>
    Parameters
    ----------
    R or region : str or list
        *Required if this is the first plot command*.
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.
    J or projection : str
        *Required if this is the first plot command*.
        Select map projection.
    <BLANKLINE>

    """
    url = "{}/{}.html".format(GMT_DOCS, module_func.__name__)
    text = "Full option list at"
    gmt_module_docs = ' '.join([text, url])

    filler_text = {'gmt_module_docs': gmt_module_docs}
    for marker, text in COMMON_OPTIONS.items():
        # Remove the identation from the multiline strings so that it doesn't
        # mess up the original docstring
        filler_text[marker] = textwrap.dedent(text)

    # Dedent the docstring to make it all match the option text.
    docstring = textwrap.dedent(module_func.__doc__)

    module_func.__doc__ = docstring.format(**filler_text)

    return module_func


def parse_bools(module_func):
    """
    Parse boolean arguments and transform them into option strings.

    Decorator function transforms ``kwargs['P']`` from ``True`` into ``''``. If
    ``False``, remove the argument from ``kwargs``.

    Parameters
    ----------
    module_func : function
        The module function.

    Returns
    -------
    new_func
        A modified module that parses bools into strings before doing any work.

    Examples
    --------

    >>> @parse_bools
    ... def my_module(*args, **kwargs):
    ...     'My docstring'
    ...     print('{', end='')
    ...     print(', '.join(
    ...         "'{}': '{}'".format(k, kwargs[k]) for k in sorted(kwargs)),
    ...         end='')
    ...     print('}')
    >>> print(my_module.__doc__)
    My docstring
    >>> my_module(P=True)
    {'P': ''}
    >>> my_module(P=False)
    {}
    >>> my_module(A='something', P=True)
    {'A': 'something', 'P': ''}
    >>> my_module(A='something', P=False)
    {'A': 'something'}

    """

    @functools.wraps(module_func)
    def new_func(*args, **kwargs):
        "New function that parses bools before executing the module"
        new_kwargs = {}
        for arg, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    new_kwargs[arg] = ''
            else:
                new_kwargs[arg] = value
        return module_func(*args, **new_kwargs)

    return new_func


def parse_region(module_func):
    """
    Parse the region argument (R) before handing it off to the function.

    Decorator function that replaces R in the arguments dictionary with a
    string version that the C API will accept.

    Parameters
    ----------
    module_func : function
        The module function.

    Returns
    -------
    new_func
        A modified module that parses R into a string before doing any work.

    Examples
    --------

    >>> @parse_region
    ... def my_module(*args, **kwargs):
    ...     '''
    ...     My GMT module.
    ...     '''
    ...     print(kwargs)
    >>> my_module(R='1/2/3/4')
    {'R': '1/2/3/4'}
    >>> my_module(R=[1, 2, 3, 4])
    {'R': '1/2/3/4'}
    >>> my_module(region=[1, 2, 3, 4])
    {'R': '1/2/3/4'}
    >>> my_module(region='1/2/3/4')
    {'R': '1/2/3/4'}

    """

    @functools.wraps(module_func)
    def new_module(*args, **kwargs):
        """
        New function that parses R before executing the module.
        """
        if 'region' in kwargs:
            kwargs['R'] = kwargs.pop('region')
        if 'R' in kwargs:
            value = kwargs['R']
            if is_nonstr_iter(value):
                kwargs['R'] = '/'.join('{}'.format(item) for item in value)
        return module_func(*args, **kwargs)

    return new_module


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
