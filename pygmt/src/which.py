"""
which - Find the full path to specified files.
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(G="download", V="verbose")
@kwargs_to_strings(fname="sequence_space")
def which(fname, **kwargs):
    r"""
    Find the full path to specified files.

    Reports the full paths to the files given through ``fname``. We look
    for the file in (1) the current directory, (2) in $GMT_USERDIR (if
    defined), (3) in $GMT_DATADIR (if defined), or (4) in $GMT_CACHEDIR
    (if defined).

    ``fname`` can also be a downloadable file (either a full URL, a
    `@file` special file for downloading from the GMT Site Cache, or
    `@earth_relief_*` topography grids). In these cases, use parameter
    ``download`` to set the desired behavior. If ``download`` is not used
    (or False), the file will not be found.

    Full option list at :gmt-docs:`gmtwhich.html`

    {aliases}

    Parameters
    ----------
    fname : str or list
        One or more file names of any data type (grids, tables, etc.).
    download : bool or str
        [**a**\|\ **c**\|\ **l**\|\ **u**].
        If the fname argument is a downloadable file (either a complete URL, an
        @file for downloading from the GMT data server, or @earth_relief_xxy)
        we will try to download the file if it is not found in your local data
        or cache dirs. By default [``download=True`` or ``download="l"``] we
        download to the current directory. Use **a** to place files in the
        appropriate folder under the user directory (this is where GMT normally
        places downloaded files), **c** to place it in the user cache
        directory, or **u** for the user data directory instead (i.e., ignoring
        any subdirectory structure).
    {verbose}

    Returns
    -------
    path : str or list
        The path(s) to the file(s), depending on the parameters used.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    """
    with GMTTempFile() as tmpfile:
        with Session() as lib:
            lib.call_module(
                module="which",
                args=build_arg_string(kwargs, infile=fname, outfile=tmpfile.name),
            )
        path = tmpfile.read().strip()
    if not path:
        _fname = fname.replace(" ", "', '")
        raise FileNotFoundError(f"File(s) '{_fname}' not found.")
    return path.split("\n") if "\n" in path else path
