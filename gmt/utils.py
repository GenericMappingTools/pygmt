"""
Utilities and common tasks for wrapping the GMT modules.
"""
import textwrap
import functools


GMT_DOCS = 'http://gmt.soest.hawaii.edu/doc/latest'

COMMON_OPTIONS = {
    'R': '''\
        R : str or list
            *Required if this is the first plot command*.
            ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
            Specify the region of interest.''',
    'J': '''\
        J : str
            *Required if this is the first plot command*.
            Select map projection.''',
    'B': '''\
        B : str
            Set map boundary frame and axes attributes.''',
    'P': '''\
        P : bool
            Select “Portrait” plot orientation.''',
    'U': '''\
        U : bool or str
            Draw GMT time stamp logo on plot.''',
    'CPT': '''\
        C : str
           File name of a CPT file or ``C='color1,color2[,color3,...]'`` to
           build a linear continuous CPT from those colors automatically.''',
    'G': '''\
        G : str
            Select color or pattern for filling of symbols or polygons. Default
            is no fill.''',
}


def fmt_docstring(module_func):
    """
    Decorator to insert common text into module docstrings.

    Should be the last decorator (at the top).

    Use any of these placeholders in your docstring to have them substituted:

    * ``{gmt_module_docs}``: link to the GMT docs for that module. Assumes that
      the name of the GMT module is the same as the function name.
    * ``{aliases}``: Insert a section listing the parameter aliases defined by
      decorator ``use_alias``.

    The following are places for common parameter descriptions:

    * ``{R}``: R (region) option with 4 bounds
    * ``{J}``: J (projection)
    * ``{B}``: B (frame)
    * ``{P}``: P (portrait)
    * ``{U}``: U (insert time stamp)
    * ``{CPT}``: CPT (the color palette table)
    * ``{G}``: G (color)

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
    ... @use_alias(R='region', J='projection')
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
    ...
    ...     {aliases}
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
    R : str or list
        *Required if this is the first plot command*.
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.
    J : str
        *Required if this is the first plot command*.
        Select map projection.
    <BLANKLINE>
    **Aliases:**
    <BLANKLINE>
    - J = projection
    - R = region
    <BLANKLINE>

    """
    filler_text = {}

    url = "{}/{}.html".format(GMT_DOCS, module_func.__name__)
    text = "Full option list at"
    filler_text['gmt_module_docs'] = ' '.join([text, url])

    if hasattr(module_func, 'aliases'):
        aliases = ['**Aliases:**\n']
        for arg in sorted(module_func.aliases):
            alias = module_func.aliases[arg]
            aliases.append('- {} = {}'.format(arg, alias))
        filler_text['aliases'] = '\n'.join(aliases)

    for marker, text in COMMON_OPTIONS.items():
        # Remove the identation from the multiline strings so that it doesn't
        # mess up the original docstring
        filler_text[marker] = textwrap.dedent(text)

    # Dedent the docstring to make it all match the option text.
    docstring = textwrap.dedent(module_func.__doc__)

    module_func.__doc__ = docstring.format(**filler_text)

    return module_func


def kwargs2string(kwargs):
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

    >>> print(kwargs2string(dict(R='1/2/3/4', J="X4i", P='', E=200)))
    -E200 -JX4i -P -R1/2/3/4

    """
    sorted_args = (
        '-{}{}'.format(key, kwargs[key])
        for key in sorted(kwargs)
    )
    arg_str = ' '.join(sorted_args)
    return arg_str


def use_alias(**aliases):
    """
    Decorator to add aliases to keyword arguments of a function.

    Use this decorator above the argument parsing decorators, usually only
    below ``fmt_docstring``.

    Replaces the aliases with their desired names before passing them along to
    the module function.

    Keywords passed to this decorator are the desired argument name and their
    value is the alias.

    Adds a dictionary attribute to the function with the aliases. Use in
    conjunction with ``fmt_docstring`` to insert a list of valid aliases in
    your docstring.

    Examples
    --------

    >>> @use_alias(R='region', J='projection')
    ... def my_module(**kwargs):
    ...     print('R =', kwargs['R'], 'J =', kwargs['J'])
    >>> my_module(R='bla', J='meh')
    R = bla J = meh
    >>> my_module(region='bla', J='meh')
    R = bla J = meh
    >>> my_module(R='bla', projection='meh')
    R = bla J = meh
    >>> my_module(region='bla', projection='meh')
    R = bla J = meh

    """

    def alias_decorator(module_func):
        """
        Decorator that replaces the aliases for arguments.
        """

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            """
            New module that parses and replaces the registered aliases.
            """
            for arg, alias in aliases.items():
                if alias in kwargs:
                    kwargs[arg] = kwargs.pop(alias)
            return module_func(*args, **kwargs)

        new_module.aliases = aliases

        return new_module

    return alias_decorator


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

    """

    @functools.wraps(module_func)
    def new_module(*args, **kwargs):
        """
        New function that parses R before executing the module.
        """
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
