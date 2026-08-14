"""
fitcircle - Find mean position and great or small circle fit to points on sphere.
"""

from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.helpers.utils import is_given


@fmt_docstring
def fitcircle(
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    norm: Literal["absolutes", "squares"] | None = None,
    small_circle: bool | float = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> dict[str, tuple[float, float] | float]:
    """
    Find mean position and great or small circle fit to points on sphere.

    This method takes (longitude, latitude) values and converts them to Cartesian
    three-vectors on the unit sphere. Then two locations are found: the mean
    of the input positions, and the pole to the great circle which best fits
    the input positions.

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

    When the data are closely grouped along a great circle both solutions
    are similar. If the data have large dispersion, the pole to the great
    circle will be less well determined than the mean. Compare both
    solutions as a qualitative check by calling :func:`pygmt.fitcircle`
    twice, once for each ``norm``.

    Takes a matrix, (x, y) pairs, or a file name as input.

    Must provide either ``data`` or ``x`` and ``y``.

    Full GMT docs at :gmt-docs:`fitcircle.html`.

    $aliases
       - V = verbose

    Parameters
    ----------
    data
        Pass in (longitude, latitude) values by
        providing a file name to an ASCII data table, a 2-D
        $table_classes.
    x/y : 1-D arrays
        Arrays of x and y coordinates of the data points.
    norm
        Specify the desired norm, either ``"absolutes"`` or ``"squares"``.
    small_circle
        Attempt to fit a small circle instead of a great circle. The pole
        will be constrained to lie on the great circle connecting the pole
        of the best-fit great circle and the mean location of the data.
        Optionally append the desired fixed latitude of the small circle
        [Default will determine the optimal latitude].
    $verbose

    Returns
    -------
    ret
        A ``dict`` with the following keys, each mapping to a
        ``(longitude, latitude)`` tuple:

        - ``"flat_mean"``: the flat Earth mean position
        - ``"mean"``: the mean position (Fisher or eigenvalue method,
          depending on ``norm``)
        - ``"north_pole"``: the north hemisphere great circle pole
        - ``"south_pole"``: the south hemisphere great circle pole

        If ``small_circle`` is set, two more keys are added:

        - ``"small_circle_pole"``: the small circle pole
        - ``"small_circle_distance"``: the colatitude/distance in degrees
          from the small circle pole to the small circle (a ``float``, not a
          tuple)
    """
    if norm is None:
        raise GMTParameterError(required="norm")

    aliasdict = AliasSystem(
        L=Alias(norm, name="norm", mapping={"absolutes": 1, "squares": 2}),
        S=Alias(small_circle, name="small_circle"),
    ).add_common(
        V=verbose,
    )
    aliasdict.merge(kwargs)

    # "c" (small-circle pole and colatitude) is only valid with -S; GMT errors
    # ("Cannot select c without setting -S") if "c" is requested without it.
    aliasdict["F"] = "fmnsc" if is_given(small_circle) else "fmns"

    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector", data=data, x=x, y=y, mincols=2
            ) as vintbl,
            lib.virtualfile_out(kind="dataset") as vouttbl,
        ):
            lib.call_module(
                module="fitcircle",
                args=build_arg_list(aliasdict, infile=vintbl, outfile=vouttbl),
            )
            row = lib.virtualfile_to_dataset(vfname=vouttbl, output_type="numpy")[0]
            values = [float(value) for value in row]

    solution: dict[str, tuple[float, float] | float] = {
        "flat_mean": (values[0], values[1]),
        "mean": (values[2], values[3]),
        "north_pole": (values[4], values[5]),
        "south_pole": (values[6], values[7]),
    }
    if is_given(small_circle):
        solution["small_circle_pole"] = (values[8], values[9])
        solution["small_circle_distance"] = values[10]
    return solution
