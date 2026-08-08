"""
fitcircle - Find mean position and great [or small] circle fit to points on
sphere.
"""

from typing import Literal

import numpy as np
import pandas as pd
from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, validate_output_table_type


@fmt_docstring
def fitcircle(
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: PathLike | None = None,
    norm: Literal["absolutes", "squares", "both"] | None = None,
    small_circle: bool | float = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> pd.DataFrame | np.ndarray | None:
    r"""
    Find mean position and great [or small] circle fit to points on sphere.

    **fitcircle** reads (longitude, latitude) or (latitude, longitude) values from the
    first two columns of the input data. These are converted to Cartesian
    three-vectors on the unit sphere. Then two locations are found: the mean
    of the input positions, and the pole to the great circle which best fits
    the input positions. The user may choose one or both of two possible
    solutions to this problem. When the data are closely grouped along a
    great circle both solutions are similar. If the data have large
    dispersion, the pole to the great circle will be less well determined
    than the mean. Compare both solutions as a qualitative check.

    Setting ``norm`` to ``"absolutes"`` approximates the minimization of the
    sum of absolute values of cosines of angular distances. This solution
    finds the mean position as the Fisher average of the data, and the pole
    position as the Fisher average of the cross-products between the mean
    and the data. Averaging cross-products gives weight to points in
    proportion to their distance from the mean, analogous to the "leverage"
    of distant points in linear regression in the plane.

    Setting ``norm`` to ``"squares"`` approximates the minimization of the
    sum of squares of cosines of angular distances. It creates a 3 by 3
    matrix of sums of squares of components of the data vectors. The
    eigenvectors of this matrix give the mean and pole locations. This
    method may be more subject to roundoff errors when there are thousands
    of data. The pole is given by the eigenvector corresponding to the
    smallest eigenvalue; it is the least-well represented factor in the data
    and is not easily estimated by either method.

    Takes a matrix, (x, y) pairs, or a file name as input.

    Must provide either ``data`` or ``x`` and ``y``.

    Full GMT docs at :gmt-docs:`fitcircle.html`.

    $aliases
       - V = verbose

    Parameters
    ----------
    data
        Pass in (longitude, latitude) or (latitude, longitude) values by
        providing a file name to an ASCII data table, a 2-D
        $table_classes.
    x/y : 1-D arrays
        Arrays of x and y coordinates of the data points.
    $output_type
    $outfile
    norm
        Specify the desired norm. Use ``"absolutes"`` or ``"squares"`` to
        select a single solution, or ``"both"`` to see both solutions. Note
        that ``output_type="pandas"`` is not supported when ``norm`` is
        ``"both"``; use ``output_type="numpy"`` or ``output_type="file"``
        instead.
    small_circle : bool or float
        Attempt to fit a small circle instead of a great circle. The pole
        will be constrained to lie on the great circle connecting the pole
        of the best-fit great circle and the mean location of the data.
        Optionally append the desired fixed latitude of the small circle
        [Default will determine the optimal latitude].
    $verbose

    Returns
    -------
    ret
        Return type depends on ``outfile`` and ``output_type``:

        - ``None`` if ``outfile`` is set (output will be stored in the file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not set
          (depends on ``output_type``)
    """
    if norm is None:
        raise GMTParameterError(required="norm")

    output_type = validate_output_table_type(output_type, outfile=outfile)
    if output_type == "pandas" and norm == "both":
        raise GMTValueError(
            norm,
            description="value for parameter 'norm'",
            reason=(
                "Pandas output is not supported when 'norm' is set to 'both' "
                "since both solutions are stacked in the same rows. Use "
                "output_type='numpy' or output_type='file' instead."
            ),
        )

    aliasdict = AliasSystem(
        L=Alias(norm, name="norm", mapping={"absolutes": 1, "squares": 2, "both": 3}),
        S=Alias(small_circle, name="small_circle"),
    ).add_common(
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector", data=data, x=x, y=y, mincols=2
            ) as vintbl,
            lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
        ):
            lib.call_module(
                module="fitcircle",
                args=build_arg_list(aliasdict, infile=vintbl, outfile=vouttbl),
            )
        return lib.virtualfile_to_dataset(
            vfname=vouttbl,
            output_type=output_type,
            column_names=["longitude", "latitude", "method"],
        )
