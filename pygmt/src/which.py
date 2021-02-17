"""
which - Find the full path to specified files.
"""
from pygmt.clib import Session
from pygmt.helpers import GMTTempFile, build_arg_string, fmt_docstring, use_alias


@fmt_docstring
@use_alias(G="download", V="verbose")
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

    Full option list at :gmt-docs:`gmtwhich.html`

    {aliases}

    Parameters
    ----------
    fname : str
        The file name that you want to check.
    download : bool or str
        If the file is downloadable and not found, we will try to download the
        it. Use True or 'l' (default) to download to the current directory. Use
        'c' to place in the user cache directory or 'u' user data directory
        instead.
    {V}

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
        arg_str = " ".join([fname, build_arg_string(kwargs), "->" + tmpfile.name])
        with Session() as lib:
            lib.call_module("which", arg_str)
        path = tmpfile.read().strip()
    if not path:
        raise FileNotFoundError("File '{}' not found.".format(fname))
    return path
