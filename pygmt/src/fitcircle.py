"""
fitcircle - Find mean position and great [or small] circle fit to points on
sphere.
"""

from typing import Literal

import numpy as np
import pandas as pd
from pygmt._typing import PathLike, TableLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    use_alias,
    validate_output_table_type,
)


@fmt_docstring
@use_alias(
    L="norm",
    S="small_circle",
)
def fitcircle(
    data: PathLike | TableLike,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: PathLike | None = None,
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

    Setting ``norm`` to **1** approximates the minimization of the sum of
    absolute values of cosines of angular distances. This solution finds the
    mean position as the Fisher average of the data, and the pole position
    as the Fisher average of the cross-products between the mean and the
    data. Averaging cross-products gives weight to points in proportion to
    their distance from the mean, analogous to the "leverage" of distant
    points in linear regression in the plane.

    Setting ``norm`` to **2** approximates the minimization of the sum of
    squares of cosines of angular distances. It creates a 3 by 3 matrix of
    sums of squares of components of the data vectors. The eigenvectors of
    this matrix give the mean and pole locations. This method may be more
    subject to roundoff errors when there are thousands of data. The pole is
    given by the eigenvector corresponding to the smallest eigenvalue; it is
    the least-well represented factor in the data and is not easily
    estimated by either method.

    Full GMT docs at :gmt-docs:`fitcircle.html`.

    $aliases
       - V = verbose

    Parameters
    ----------
    data
        Pass in (longitude, latitude) or (latitude, longitude) values by
        providing a file name to an ASCII data table, a 2-D
        $table_classes.
    $output_type
    $outfile
    norm : int or bool
        Specify the desired *norm* as **1** or **2**\ , or use ``True`` or
        **3** to see both solutions.
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
    if kwargs.get("L") is None:
        raise GMTParameterError(required="norm")

    output_type = validate_output_table_type(output_type, outfile=outfile)

    aliasdict = AliasSystem().add_common(
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
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
