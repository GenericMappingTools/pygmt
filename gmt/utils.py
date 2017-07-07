"""
Utilities and common tasks for wrapping the GMT modules.
"""

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
