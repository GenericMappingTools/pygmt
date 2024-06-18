"""
which - Find the full path to specified files.
"""

from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, is_nonstr_iter, use_alias


@fmt_docstring
@use_alias(G="download", V="verbose")
def which(fname, **kwargs) -> str | list[str]:
    r"""
    Find the full path to specified files.

    Reports the full paths to the files given through ``fname``. We look
    for the file in (1) the current directory, (2) in $GMT_USERDIR (if
    defined), (3) in $GMT_DATADIR (if defined), or (4) in $GMT_CACHEDIR
    (if defined).

    ``fname`` can also be a downloadable file (either a complete URL, an
    @file for downloading from the GMT data server, or any of the remote
    datasets at https://www.pygmt.org/latest/api/index.html#datasets).
    In these cases, use the ``download`` parameter to set the desired
    behavior. If ``download`` is not used (or ``False``), the file will
    not be found.

    Full option list at :gmt-docs:`gmtwhich.html`

    {aliases}

    Parameters
    ----------
    fname : str or list
        One or more file names of any data type (grids, tables, etc.).
    download : bool or str
        [**a**\|\ **c**\|\ **l**\|\ **u**].
        If the ``fname`` argument is a downloadable file (either a complete
        URL, an @file for downloading from the GMT data server, or any of
        the remote datasets at
        https://www.pygmt.org/latest/api/index.html#datasets)
        we will try to download the file if it is not found in your local
        data or cache directories. If set to ``True`` or **l** is passed
        the file is downloaded to the current directory. Use **a** to place
        files in the appropriate folder under the user directory (this is
        where GMT normally places downloaded files), **c** to place it in
        the user cache directory, or **u** for the user data directory
        instead (i.e., ignoring any subdirectory structure).
    {verbose}

    Returns
    -------
    path
        The path(s) to the file(s), depending on the parameters used.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    """
    with Session() as lib:
        with lib.virtualfile_out(kind="dataset") as vouttbl:
            lib.call_module(
                module="which",
                args=build_arg_list(kwargs, infile=fname, outfile=vouttbl),
            )
            paths = lib.virtualfile_to_dataset(vfname=vouttbl, output_type="strings")

    match paths.size:
        case 0:
            _fname = "', '".join(fname) if is_nonstr_iter(fname) else fname
            raise FileNotFoundError(f"File(s) '{_fname}' not found.")
        case 1:
            return paths[0]
        case _:
            return paths.tolist()
