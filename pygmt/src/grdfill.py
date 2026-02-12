"""
grdfill - Interpolate across holes in a grid.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, deprecate_parameter, fmt_docstring, use_alias

__doctest_skip__ = ["grdfill"]


def _validate_params(
    constant_fill=None,
    grid_fill=None,
    neighbor_fill=None,
    spline_fill=None,
    inquire=False,
):
    """
    Validate the fill/inquire parameters.

    >>> _validate_params(constant_fill=20.0)
    >>> _validate_params(inquire=True)
    >>> _validate_params(constant_fill=20.0, grid_fill="bggrid.nc")
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTParameterError: Mutually exclusive parameters: ...
    >>> _validate_params(constant_fill=20.0, inquire=True)
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTParameterError: Mutually exclusive parameters: ...
    >>> _validate_params()
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTParameterError: Missing parameter: requires at least one ...
    """
    params = {
        "constant_fill": constant_fill,
        "grid_fill": grid_fill,
        "neighbor_fill": neighbor_fill,
        "spline_fill": spline_fill,
        "inquire": inquire,
    }
    n_given = sum(param is not None and param is not False for param in params.values())
    match n_given:
        case 0:
            raise GMTParameterError(at_least_one=params)
        case 1:
            pass
        case _:
            raise GMTParameterError(at_most_one=params)


@fmt_docstring
# TODO(PyGMT>=0.20.0): Remove the deprecated '*fill' parameters.
@deprecate_parameter(
    "constantfill", "constant_fill", "v0.18.0", remove_version="v0.20.0"
)
@deprecate_parameter("gridfill", "grid_fill", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter(
    "neighborfill", "neighbor_fill", "v0.18.0", remove_version="v0.20.0"
)
@deprecate_parameter("splinefill", "spline_fill", "v0.18.0", remove_version="v0.20.0")
@use_alias(f="coltypes")
def grdfill(
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    constant_fill: float | None = None,
    grid_fill: PathLike | xr.DataArray | None = None,
    neighbor_fill: float | bool | None = None,
    spline_fill: float | bool | None = None,
    inquire: bool = False,
    hole: float | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | np.ndarray | None:
    r"""
    Interpolate across holes in a grid.

    Read a grid that presumably has unfilled holes that the user wants to fill in some
    fashion. Holes are identified by NaN values but this criteria can be changed via the
    ``hole`` parameter. There are several different algorithms that can be used to
    replace the hole values. If no holes are found the original unchanged grid is
    returned.

    Full GMT docs at :gmt-docs:`grdfill.html`.

    $aliases
       - Ac = constant_fill
       - Ag = grid_fill
       - An = neighbor_fill
       - As = spline_fill
       - G = outgrid
       - L = inquire
       - N = hole
       - R = region
       - V = verbose

    Parameters
    ----------
    $grid
    $outgrid
    constant_fill
        Fill the holes with a constant value. Specify the constant value to use.
    grid_fill
        Fill the holes with values sampled from another (possibly coarser) grid. Specify
        the grid (a file name or an :class:`xarray.DataArray`) to use for the fill.
    neighbor_fill
        Fill the holes with the nearest neighbor. Specify the search radius in pixels.
        If set to ``True``, the default search radius will be used
        (:math:`r^2 = \sqrt{n^2 + m^2}`, where (*n,m*) are the node dimensions of the
        grid).
    spline_fill
        Fill the holes with a bicubic spline. Specify the tension value to use. If set
        to ``True``, no tension will be used.
    hole
        Set the node value used to identify a point as a member of a hole [Default is
        NaN].
    inquire
        Output the bounds of each hole. The bounds are returned as a 2-D numpy array in
        the form of (west, east, south, north). No grid fill takes place and ``outgrid``
        is ignored.

    $region
    $verbose
    $coltypes

    Returns
    -------
    ret
        If ``inquire`` is ``True``, return the bounds of each hole as a 2-D numpy array.
        Otherwise, the return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    Fill holes in a bathymetric grid with a constant value of 20.

    >>> import pygmt
    >>> # Load a bathymetric grid with missing data
    >>> earth_relief_holes = pygmt.datasets.load_sample_data(name="earth_relief_holes")
    >>> # Fill the holes with a constant value of 20
    >>> filled_grid = pygmt.grdfill(grid=earth_relief_holes, constant_fill=20)

    Inquire the bounds of each hole.

    >>> pygmt.grdfill(grid=earth_relief_holes, inquire=True)
    array([[1.83333333, 6.16666667, 3.83333333, 8.16666667],
           [6.16666667, 7.83333333, 0.5       , 2.5       ]])
    """
    # Validate the fill/inquire parameters.
    _validate_params(constant_fill, grid_fill, neighbor_fill, spline_fill, inquire)

    # _validate_params has already ensured that only one of the parameters is set.
    aliasdict = AliasSystem(
        Ac=Alias(constant_fill, name="constant_fill"),
        # For grid_fill, append the actual or virtual grid file name later.
        Ag=Alias(grid_fill is not None, name="grid_fill"),
        An=Alias(neighbor_fill, name="neighbor_fill"),
        As=Alias(spline_fill, name="spline_fill"),
        L=Alias(inquire, name="inquire"),
        N=Alias(hole, name="hole"),
    ).add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
            if inquire:  # Inquire mode.
                with lib.virtualfile_out(kind="dataset") as vouttbl:
                    lib.call_module(
                        module="grdfill",
                        args=build_arg_list(aliasdict, infile=vingrd, outfile=vouttbl),
                    )
                    return lib.virtualfile_to_dataset(
                        vfname=vouttbl, output_type="numpy"
                    )

            # Fill mode.
            with (
                lib.virtualfile_in(
                    check_kind="raster", data=grid_fill, required=False
                ) as vbggrd,
                lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
            ):
                if grid_fill is not None:
                    # Fill by a grid. Append the actual or virtual grid file name.
                    aliasdict["Ag"] = vbggrd
                aliasdict["G"] = voutgrd
                lib.call_module(
                    module="grdfill", args=build_arg_list(aliasdict, infile=vingrd)
                )
                return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
