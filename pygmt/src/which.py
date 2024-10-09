"""
which - Find the full path to specified files.
"""

from collections.abc import Sequence
from pathlib import PurePath
from typing import Literal

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, is_nonstr_iter, use_alias


@fmt_docstring
@use_alias(V="verbose")
def which(
    fname: str | PurePath | Sequence[str | PurePath],
    download: bool | Literal["auto", "cache", "local", "user"] = False,
    **kwargs,
) -> str | list[str]:
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
    fname
        One or more file names to find the full path.
    download
        Try to download the file if it is not found in your local data or cache
        directories and the file is downloadable. Here, downloadable files include:

        - a file specified by a complete URL
        - a GMT remote file on the GMT data server, specified with a leading ``@``.
        - any of the GMT remote datasets at https://www.pygmt.org/latest/api/index.html#datasets

        Valid values are:

        - ``False``: Do not download the file.
        - ``True`` or ``"local"``: Download the file to the current directory.
        - ``"cache"``: Download the file to the user cache directory.
        - ``"user"``: Download the file to the user data directory but ignore any
          subdirectory structure.
        - ``"auto"``: Download the file to appropriate folder under the user directory
          (this is where GMT normally places downloaded files).
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
    match download:
        case bool() | "a" | "c" | "l" | "u":
            kwargs["G"] = download
        case "auto" | "cache" | "local" | "user":
            kwargs["G"] = download[0]
        case _:
            msg = (
                "'download' should be either bool, 'auto', 'cache', 'local', or 'user'."
            )
            raise GMTInvalidInput(msg)

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
            msg = f"File(s) '{_fname}' not found."
            raise FileNotFoundError(msg)
        case 1:
            return paths[0]
        case _:
            return paths.tolist()
