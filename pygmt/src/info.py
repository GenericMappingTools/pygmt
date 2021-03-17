"""
info - Get information about data tables.
"""
import numpy as np
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(C="per_column", I="spacing", T="nearest_multiple", V="verbose", f="coltypes")
@kwargs_to_strings(I="sequence")
def info(table, **kwargs):
    r"""
    Get information about data tables.

    Reads from files and finds the extreme values in each of the columns
    reported as min/max pairs. It recognizes NaNs and will print warnings if
    the number of columns vary from record to record. As an option, it will
    find the extent of the first two columns rounded up and down to the nearest
    multiple of the supplied increments given by ``spacing``. Such output will
    be in a numpy.ndarray form [*w*, *e*, *s*, *n*], which can be used
    directly as the ``region`` parameter for other modules (hence only *dx*
    and *dy* are needed). If the ``per_column`` parameter is combined with
    ``spacing``, then the numpy.ndarray output will be rounded up/down for as
    many columns as there are increments provided in ``spacing``. A similar
    parameter ``nearest_multiple`` will provide a numpy.ndarray in the form
    of [*zmin*, *zmax*, *dz*] for makecpt.

    Full option list at :gmt-docs:`gmtinfo.html`

    {aliases}

    Parameters
    ----------
    table : str or np.ndarray or pandas.DataFrame or xarray.Dataset
        Pass in either a file name to an ASCII data table, a 1D/2D numpy array,
        a pandas dataframe, or an xarray dataset made up of 1D xarray.DataArray
        data variables.
    per_column : bool
        Report the min/max values per column in separate columns.
    spacing : str
        [**b**\|\ **p**\|\ **f**\|\ **s**]\ *dx*\[/*dy*\[/*dz*...]].
        Report the min/max of the first n columns to the nearest multiple of
        the provided increments and output results in the form
        ``[w, e, s, n]``.
    nearest_multiple : str
        **dz**\[\ **+c**\ *col*].
        Report the min/max of the first (0'th) column to the nearest multiple
        of dz and output this in the form ``[zmin, zmax, dz]``.

    {V}
    {f}

    Returns
    -------
    output : np.ndarray or str
        Return type depends on whether any of the ``per_column``,
        ``spacing``, or ``nearest_multiple`` parameters are set.

        - :class:`numpy.ndarray` if either of the above parameters are used.
        - str if none of the above parameters are used.
    """
    with Session() as lib:
        file_context = lib.virtualfile_from_data(data=table)
        with GMTTempFile() as tmpfile:
            with file_context as fname:
                arg_str = " ".join(
                    [fname, build_arg_string(kwargs), "->" + tmpfile.name]
                )
                lib.call_module("info", arg_str)
            result = tmpfile.read()

        if any(arg in kwargs for arg in ["C", "I", "T"]):
            # Converts certain output types into a numpy array
            # instead of a raw string that is less useful.
            if result.startswith(("-R", "-T")):  # e.g. -R0/1/2/3 or -T0/9/1
                result = result[2:].replace("/", " ")
            try:
                result = np.loadtxt(result.splitlines())
            except ValueError:
                # Load non-numerical outputs in str type, e.g. for datetime
                result = np.loadtxt(result.splitlines(), dtype="str")

        return result
