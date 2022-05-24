"""
fitcircle - Find mean position and great [or small] circle fit to points on
sphere.
"""
import warnings

import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, build_arg_string, fmt_docstring, use_alias


@fmt_docstring
@use_alias(
    L="norm",
    S="small_circle",
    V="verbose",
)
def fitcircle(data, output_type="pandas", outfile=None, **kwargs):
    r"""
    Find mean position and great [or small] circle fit to points on sphere.

    **fitcircle** reads lon,lat [or lat,lon] values from the first two
    columns of the table. These are converted to
    Cartesian three-vectors on the unit sphere. Then two locations are
    found: the mean of the input positions, and the pole to the great circle
    which best fits the input positions. The user may choose one or both of
    two possible solutions to this problem. When the data are closely grouped
    along a great circle both solutions are similar. If the data have large
    dispersion, the pole to the great circle will be less well determined
    than the mean. Compare both solutions as a qualitative check.

    Setting ``norm`` to **1** approximates the
    minimization of the sum of absolute values of cosines of angular
    distances. This solution finds the mean position as the Fisher average
    of the data, and the pole position as the Fisher average of the
    cross-products between the mean and the data. Averaging cross-products
    gives weight to points in proportion to their distance from the mean,
    analogous to the "leverage" of distant points in linear regression in
    the plane.

    Setting ``norm`` to **2** approximates the
    minimization of the sum of squares of cosines of angular distances. It
    creates a 3 by 3 matrix of sums of squares of components of the data
    vectors. The eigenvectors of this matrix give the mean and pole
    locations. This method may be more subject to roundoff errors when there
    are thousands of data. The pole is given by the eigenvector
    corresponding to the smallest eigenvalue; it is the least-well
    represented factor in the data and is not easily estimated by either
    method.

    Full option list at :gmt-docs:`fitcircle.html`

    {aliases}

    Parameters
    ----------
    data : str or list or {table-like}
        Pass in either a file name to an ASCII data table, a Python list, a 2D
        {table-classes} containing longitude and latitude values.
    output_type : str
        Determine the format the xyz data will be returned in [Default is
        ``pandas``]:

            - ``numpy`` - :class:`numpy.ndarray`
            - ``pandas``- :class:`pandas.DataFrame`
            - ``file`` - ASCII file (requires ``outfile``)
    outfile : str
        The file name for the output ASCII file.
    norm : int or bool
        Specify the desired *norm* as **1** or **2**\ , or use ``True``
        or **3** to see both solutions.
    small_circle : float
        Attempt to fit a small circle instead of a great circle. The pole
        will be constrained to lie on the great circle connecting the pole
        of the best-fit great circle and the mean location of the data.
        Optionally append the desired fixed latitude of the small circle
        [Default will determine the optimal latitude].
    {V}

    Returns
    -------
    ret : pandas.DataFrame or numpy.ndarray or None
        Return type depends on ``outfile`` and ``output_type``:

        - None if ``outfile`` is set (output will be stored in file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is
          not set (depends on ``output_type`` [Default is
          :class:`pandas.DataFrame`])

    """
    if kwargs.get("L") is None:
        raise GMTInvalidInput("Pass a required argument to 'norm'.")
    if output_type not in ["numpy", "pandas", "file"]:
        raise GMTInvalidInput("Must specify format as either numpy, pandas, or file.")
    if outfile is not None and output_type != "file":
        msg = (
            f"Changing `output_type` of fitcirle from '{output_type}' to 'file' "
            "since `outfile` parameter is set. Please use `output_type='file'` "
            "to silence this warning."
        )
        warnings.warn(msg, category=RuntimeWarning, stacklevel=2)
        output_type = "file"
    elif output_type == "file" and outfile is None:
        raise GMTInvalidInput("Must specify outfile for ASCII output.")
    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                lib.call_module(
                    module="fitcircle",
                    args=build_arg_string(kwargs, infile=infile, outfile=outfile),
                )

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(
                tmpfile.name,
                sep="\t",
                names=["longitude", "latitude", "method"],
                comment=">",
            )
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "numpy":
            result = result.to_numpy()
    return result
