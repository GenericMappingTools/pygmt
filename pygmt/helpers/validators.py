"""
Functions to check if given arguments are valid.
"""
import warnings

from pygmt.exceptions import GMTInvalidInput


def validate_output_table_type(output_type, outfile=None):
    """
    Check if the ``output_type`` and ``outfile`` parameters are valid.

    Parameters
    ----------
    output_type : str
        The type for a table output. Valid values are "file", "numpy", and
        "pandas".
    outfile : str
        The file name for the output table file. Required if
        ``output_type="file"``.

    Returns
    -------
    str
        The original or corrected output type.
    """
    if output_type not in ["file", "numpy", "pandas"]:
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
