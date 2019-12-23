"""
Decorators to help wrap the GMT modules.

Apply them to functions wrapping GMT modules to automate: alias generation for
arguments, insert common text into docstrings, transform arguments to strings,
etc.
"""
import textwrap
import functools

from .utils import is_nonstr_iter
from ..exceptions import GMTInvalidInput


COMMON_OPTIONS = {
    "R": """\
        R : str or list
            *Required if this is the first plot command*.
            ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
            Specify the region of interest.""",
    "J": """\
        J : str
            *Required if this is the first plot command*.
            Select map projection.""",
    "B": """\
        B : str or list
            Set map boundary frame and axes attributes.""",
    "U": """\
        U : bool or str
            Draw GMT time stamp logo on plot.""",
    "CPT": """\
        C : str
           File name of a CPT file or ``C='color1,color2[,color3,...]'`` to
           build a linear continuous CPT from those colors automatically.""",
    "G": """\
        G : str
            Select color or pattern for filling of symbols or polygons. Default
            is no fill.""",
    "W": """\
        W : str
            Set pen attributes for lines or the outline of symbols.""",
}


def fmt_docstring(module_func):
    """
    Decorator to insert common text into module docstrings.

    Should be the last decorator (at the top).

    Use any of these placeholders in your docstring to have them substituted:

    * ``{aliases}``: Insert a section listing the parameter aliases defined by
      decorator ``use_alias``.

    The following are places for common parameter descriptions:

    * ``{R}``: R (region) option with 4 bounds
    * ``{J}``: J (projection)
    * ``{B}``: B (frame)
    * ``{U}``: U (insert time stamp)
    * ``{CPT}``: CPT (the color palette table)
    * ``{G}``: G (color)
    * ``{W}``: W (pen)

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

    if hasattr(module_func, "aliases"):
        aliases = ["**Aliases:**\n"]
        for arg in sorted(module_func.aliases):
            alias = module_func.aliases[arg]
            aliases.append("- {} = {}".format(arg, alias))
        filler_text["aliases"] = "\n".join(aliases)

    for marker, text in COMMON_OPTIONS.items():
        # Remove the indentation from the multiline strings so that it doesn't
        # mess up the original docstring
        filler_text[marker] = textwrap.dedent(text)

    # Dedent the docstring to make it all match the option text.
    docstring = textwrap.dedent(module_func.__doc__)

    module_func.__doc__ = docstring.format(**filler_text)

    return module_func


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


def kwargs_to_strings(convert_bools=True, **conversions):
    """
    Decorator to convert given keyword arguments to strings.

    The strings are what GMT expects from command line arguments.

    Converts all boolean arguments by default. Transforms ``True`` into ``''``
    (empty string) and removes the argument from ``kwargs`` if ``False``.

    You can also specify other conversions to specific arguments.

    Conversions available:

    * 'sequence': transforms a sequence (list, tuple) into a ``'/'`` separated
      string
    * 'sequence_comma': transforms a sequence into a ``','`` separated string
    * 'sequence_plus': transforms a sequence into a ``'+'`` separated string
    * 'sequence_space': transforms a sequence into a ``' '`` separated string

    Parameters
    ----------
    convert_bools : bool
        If ``True``, convert all boolean arguments to strings using the rules
        specified above. If ``False``, leave them as they are.
    conversions : keyword arguments
        Keyword arguments specifying other kinds of conversions that should be
        performed. The keyword is the name of the argument and the value is the
        conversion type (see list above).

    Examples
    --------

    >>> @kwargs_to_strings(
    ...     R='sequence', i='sequence_comma', files='sequence_space'
    ... )
    ... def module(*args, **kwargs):
    ...     "A module that prints the arguments it received"
    ...     print('{', end='')
    ...     print(', '.join(
    ...         "'{}': {}".format(k, repr(kwargs[k])) for k in sorted(kwargs)),
    ...         end='')
    ...     print('}')
    ...     if args:
    ...         print("args:", ' '.join('{}'.format(x) for x in args))
    >>> module(R=[1, 2, 3, 4])
    {'R': '1/2/3/4'}
    >>> # It's already a string, do nothing
    >>> module(R='5/6/7/8')
    {'R': '5/6/7/8'}
    >>> module(P=True)
    {'P': ''}
    >>> module(P=False)
    {}
    >>> module(i=[1, 2])
    {'i': '1,2'}
    >>> module(files=["data1.txt", "data2.txt"])
    {'files': 'data1.txt data2.txt'}
    >>> # Other non-boolean arguments are passed along as they are
    >>> module(123, bla=(1, 2, 3), foo=True, A=False, i=(5, 6))
    {'bla': (1, 2, 3), 'foo': '', 'i': '5,6'}
    args: 123

    """
    valid_conversions = [
        "sequence",
        "sequence_comma",
        "sequence_plus",
        "sequence_space",
    ]

    for arg, fmt in conversions.items():
        if fmt not in valid_conversions:
            raise GMTInvalidInput(
                "Invalid conversion type '{}' for argument '{}'.".format(fmt, arg)
            )

    separators = {
        "sequence": "/",
        "sequence_comma": ",",
        "sequence_plus": "+",
        "sequence_space": " ",
    }

    # Make the actual decorator function
    def converter(module_func):
        "The decorator that creates our new function with the conversions"

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            "New module instance that converts the arguments first"
            if convert_bools:
                kwargs = remove_bools(kwargs)
            for arg, fmt in conversions.items():
                if arg in kwargs:
                    value = kwargs[arg]
                    issequence = fmt in separators
                    if issequence and is_nonstr_iter(value):
                        kwargs[arg] = separators[fmt].join(
                            "{}".format(item) for item in value
                        )
            # Execute the original function and return its output
            return module_func(*args, **kwargs)

        return new_module

    return converter


def remove_bools(kwargs):
    """
    Remove booleans from arguments.

    If ``True``, replace it with an empty string. If ``False``, completely
    remove the entry from the argument list.

    Parameters
    ----------
    kwargs : dict
        Dictionary with the keyword arguments.

    Returns
    -------
    new_kwargs : dict
        A copy of `kwargs` with the booleans parsed.

    """
    new_kwargs = {}
    for arg, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                new_kwargs[arg] = ""
        else:
            new_kwargs[arg] = value
    return new_kwargs
