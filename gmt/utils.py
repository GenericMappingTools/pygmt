"""
Utilities and common tasks for wrapping the GMT modules.
"""
import textwrap
import functools


GMT_DOCS = 'http://gmt.soest.hawaii.edu/doc/latest'


def gmt_docs_link(module_func):
    """
    Add to a module docstring a link to the GMT docs for that module.

    The docstring must have the placeholder ``{gmt_module_docs}`` where you
    want the link to appear.

    Assumes that the name of the GMT module is the same as the function name.

    Use this function as a decorator for the module functions.

    Parameters
    ----------
    module_func : function
        The module function. Must have the same name as the GMT module.

    Returns
    -------
    module_func
        The same *module_func* but with the link inserted into the docstring.


    Examples
    --------

    >>> @gmt_docs_link
    ... def gmtinfo(**kwargs):
    ...     '''
    ...     My nice module.
    ...     {gmt_module_docs}
    ...     '''
    ...     pass
    >>> print(gmtinfo.__doc__)
    <BLANKLINE>
        My nice module.
        Full option list at http://gmt.soest.hawaii.edu/doc/latest/gmtinfo.html
    <BLANKLINE>

    """
    url = "{}/{}.html".format(GMT_DOCS, module_func.__name__)
    text = "Full option list at"
    full_text = ' '.join([text, url])
    module_func.__doc__ = module_func.__doc__.format(gmt_module_docs=full_text)
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

    Formats the docstring of the module to include a description of the R
    parameter where a ``{region_docs}`` marker is present.

    Parameters
    ----------
    module_func : function
        The module function.

    Returns
    -------
    new_func
        A modified module with formatted docstring and that parses R into a
        string before doing any work.

    Examples
    --------

    >>> @parse_region
    ... def my_module(*args, **kwargs):
    ...     '''
    ...     My GMT module.
    ...
    ...     Parameters
    ...     ----------
    ...     {region_docs}
    ...     '''
    ...     print(kwargs)
    >>> print(my_module.__doc__)
    <BLANKLINE>
    My GMT module.
    <BLANKLINE>
    Parameters
    ----------
    R or region : str or list
        *Required if this is the first plot command*.
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.
    <BLANKLINE>
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

    # Format the docstring to include the help for R
    region_docs = '''\
        R or region : str or list
            *Required if this is the first plot command*.
            ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
            Specify the region of interest.'''
    region_docs = textwrap.dedent(region_docs)
    docs = textwrap.dedent(module_func.__doc__)
    new_module.__doc__ = docs.format(region_docs=region_docs)

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
