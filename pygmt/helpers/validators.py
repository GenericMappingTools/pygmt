"""
Functions to check if given arguments are valid.
"""

import warnings
from typing import Literal

from pygmt.exceptions import GMTInvalidInput


def validate_output_table_type(
    output_type: Literal["pandas", "numpy", "file"], outfile: str | None = None
) -> Literal["pandas", "numpy", "file"]:
    """
    Check if the ``output_type`` and ``outfile`` parameters are valid.

    Parameters
    ----------
    output_type
        Desired output type of tabular data. Valid values are ``"pandas"``,
        ``"numpy"`` and ``"file"``.
    outfile
        File name for saving the result data. Required if ``output_type`` is ``"file"``.
        If specified, ``output_type`` will be forced to be ``"file"``.

    Returns
    -------
    str
        The original or updated output type.

    Examples
    --------
    >>> validate_output_table_type(output_type="pandas")
    'pandas'
    >>> validate_output_table_type(output_type="numpy")
    'numpy'
    >>> validate_output_table_type(output_type="file", outfile="output-fname.txt")
    'file'
    >>> validate_output_table_type(output_type="invalid-type")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Must specify 'output_type' either as 'file', ...
    >>> validate_output_table_type("file", outfile=None)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Must specify 'outfile' for output_type='file'.
    >>> with warnings.catch_warnings(record=True) as w:
    ...     validate_output_table_type("pandas", outfile="not-none.txt")
    ...     assert len(w) == 1
    'file'
    """
    if output_type not in {"file", "numpy", "pandas"}:
        raise GMTInvalidInput(
            "Must specify 'output_type' either as 'file', 'numpy', or 'pandas'."
        )
    if output_type == "file" and outfile is None:
        raise GMTInvalidInput("Must specify 'outfile' for output_type='file'.")
    if output_type != "file" and outfile is not None:
        msg = (
            f"Changing 'output_type' from '{output_type}' to 'file' "
            "since 'outfile' parameter is set. Please use output_type='file' "
            "to silence this warning."
        )
        warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
        output_type = "file"
    return output_type
