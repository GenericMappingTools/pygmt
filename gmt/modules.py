"""
Non-plot GMT modules.
"""
from .clib import LibGMT
from .helpers import build_arg_string, fmt_docstring, GMTTempFile, use_alias


@fmt_docstring
def info(fname, **kwargs):
    """
    Get information about data tables.

    {gmt_module_docs}

    Parameters
    ----------
    fname : str
        The file name of the input data table file.
    """
    assert isinstance(fname, str), 'Only accepts file names.'

    with GMTTempFile() as tmpfile:
        arg_str = ' '.join([fname, build_arg_string(kwargs),
                            "->" + tmpfile.name])
        with LibGMT() as lib:
            lib.call_module('info', arg_str)
        return tmpfile.read()


@fmt_docstring
@use_alias(G='download')
def which(fname, **kwargs):
    """
    Find the full path to specified files.

    Reports the full paths to the files given through *fname*. We look for
    the file in (1) the current directory, (2) in $GMT_USERDIR (if defined),
    (3) in $GMT_DATADIR (if defined), or (4) in $GMT_CACHEDIR (if defined).

    *fname* can also be a downloadable file (either a full URL, a
    `@file` special file for downloading from the GMT Site Cache, or
    `@earth_relief_*` topography grids). In these cases, use option *download*
    to set the desired behavior. If *download* is not used (or False), the file
    will not be found.

    {gmt_module_docs}

    {aliases}

    Parameters
    ----------
    fname : str
        The file name that you want to check.
    G : bool or str
        If the file is downloadable and not found, we will try to download the
        it. Use True or 'l' (default) to download to the current directory. Use
        'c' to place in the user cache directory or 'u' user data directory
        instead.

    Returns
    -------
    path : str
        The path of the file, depending on the options used.

    Raises
    ------
    FileNotFoundError
        If the file is not found.

    """
    with GMTTempFile() as tmpfile:
        arg_str = ' '.join([fname, build_arg_string(kwargs),
                            "->" + tmpfile.name])
        with LibGMT() as lib:
            lib.call_module('which', arg_str)
        path = tmpfile.read().strip()
    if not path:
        raise FileNotFoundError("File '{}' not found.".format(fname))
    return path
