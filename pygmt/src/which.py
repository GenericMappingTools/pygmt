"""
which - Find full path to specified files.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, is_nonstr_iter


@fmt_docstring
def which(
    fname: PathLike | Sequence[PathLike],
    download: Literal["auto", "cache", "local", "user"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> str | list[str]:
    """
    Find full path to specified files.

    Reports the full paths to the files given through ``fname``. It looks for the file
    in (1) the current directory, (2) in $GMT_USERDIR (if defined), (3) in $GMT_DATADIR
    (if defined), or (4) in $GMT_CACHEDIR (if defined).

    ``fname`` can also be a downloadable file (either a complete URL, an @file for
    downloading from the GMT data server, or any of the remote datasets at
    :ref:`datasets`. In these cases, use the ``download`` parameter to set the desired
    behavior. If ``download`` is not used (or ``False``), the file will not be found.

    Full GMT docs at :gmt-docs:`gmtwhich.html`.

    **Aliases:**

    .. hlist::
       :columns: 3

       - G = download
       - V = verbose

    Parameters
    ----------
    fname
        One or more file names to find the full path.
    download
        Try to download the file if it is not found in your local data or cache
        directories and the file is downloadable. Here, downloadable files include:

        - a file specified by a complete URL
        - a GMT remote file on the GMT data server, specified with a leading ``@``.
        - any of the GMT remote datasets at :ref:`datasets`

        Valid values are:

        - ``False``: Do not download the file.
        - ``True`` or ``"local"``: Download the file to the current directory.
        - ``"cache"``: Download the file to the user cache directory.
        - ``"user"``: Download the file to the user data directory but ignore any
          subdirectory structure.
        - ``"auto"``: Download the file to appropriate folder under the user directory
          (this is where GMT normally places downloaded files).
    $verbose

    Returns
    -------
    path
        The path(s) to the file(s), depending on the parameters used.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    """
    aliasdict = AliasSystem(
        G=Alias(
            download,
            name="download",
            mapping={
                "auto": "a",
                "cache": "c",
                "local": "l",
                "user": "u",
                True: True,
                False: False,
            },
        )
    ).add_common(
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_out(kind="dataset") as vouttbl:
            lib.call_module(
                module="which",
                args=build_arg_list(aliasdict, infile=fname, outfile=vouttbl),
            )
            paths = lib.virtualfile_to_dataset(vfname=vouttbl, output_type="strings")

    match paths.size:
        case 0:
            _fname = "', '".join(fname) if is_nonstr_iter(fname) else fname  # type: ignore[arg-type]
            msg = f"File(s) '{_fname}' not found."
            raise FileNotFoundError(msg)
        case 1:
            return paths[0]
        case _:
            return paths.tolist()
