"""
Utilities and common tasks for wrapping the GMT modules.
"""

GMT_DOCS = 'http://gmt.soest.hawaii.edu/doc/latest'


def gmt_docs_link(module_func):
    """
    Add to a module docstring a link to the GMT docs for that module.

    The docstring must have the placeholder ``{gmt_mod}`` where you want the
    link to appear.

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
    ... def psconvert(**kwargs):
    ...     "Full docs at {gmt_mod}"
    ...     pass
    >>> print(psconvert.__doc__)
    Full docs at http://gmt.soest.hawaii.edu/doc/latest/psconvert.html

    """
    url = "{}/{}.html".format(GMT_DOCS, module_func.__name__)
    module_func.__doc__ = module_func.__doc__.format(gmt_mod=url)
    return module_func
