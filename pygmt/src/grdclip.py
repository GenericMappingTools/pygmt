"""
grdclip - Clip the range of grid values.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, deprecate_parameter, fmt_docstring

__doctest_skip__ = ["grdclip"]


# TODO(PyGMT>=0.19.0): Remove the deprecated "new" parameter.
@fmt_docstring
@deprecate_parameter("new", "replace", "v0.15.0", remove_version="v0.19.0")
def grdclip(
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    above: Sequence[float] | None = None,
    below: Sequence[float] | None = None,
    between: Sequence[float] | Sequence[Sequence[float]] | None = None,
    replace: Sequence[float] | Sequence[Sequence[float]] | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    """
    Clip the range of grid values.

    This function operates on the values of a grid. It can:

    - Set values smaller than a threshold to a new value
    - Set values larger than a threshold to a new value
    - Set values within a range to a new value
    - Replace individual values with a new value

    Such operations are useful when you want all of a continent or an ocean to fall into
    one color or gray shade in image processing, when clipping the range of data values
    is required, or for reclassification of data values. The values can be any number or
    NaN (Not a Number).

    Full GMT docs at :gmt-docs:`grdclip.html`.

    **Aliases:**

    .. hlist::
       :columns: 3

       - R = region
       - Sa = above
       - Sb = below
       - Si = between
       - Sr = replace
       - V = verbose

    Parameters
    ----------
    {grid}
    {outgrid}
    {region}
    above
        Pass a sequence of two values in the form of (*high*, *above*), to set all node
        values greater than *high* to *above*.
    below
        Pass a sequence of two values in the form of (*low*, *below*) to set all node
        values less than *low* to *below*.
    between
        Pass a sequence of three values in the form of (*low*, *high*, *between*) to set
        all node values between *low* and *high* to *between*. It can also accept a
        sequence of sequences (e.g., list of lists or 2-D numpy array) to set different
        values for different ranges.
    replace
        Pass a sequence of two values in the form of (*old*, *new*) to replace all node
        values equal to *old* with *new*. It can also accept a sequence of sequences
        (e.g., list of lists or 2-D numpy array) to replace different old values with
        different new values. This is mostly useful when your data are known to be
        integer values.
    {verbose}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load the 30 arc-minutes Earth relief grid, with a longitude range of 10° E to
    >>> # 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Report the minimum and maximum data values
    >>> [grid.data.min(), grid.data.max()]
    [183.5, 1807.0]
    >>> # Create a new grid from an input grid. Set all values below 1,000 to 0 and all
    >>> # values above 1,500 to 10,000
    >>> new_grid = pygmt.grdclip(grid=grid, below=[1000, 0], above=[1500, 10000])
    >>> # Report the minimum and maximum data values
    >>> [new_grid.data.min(), new_grid.data.max()]
    [0.0, 10000.0]
    """
    if all(v is None for v in (above, below, between, replace)):
        msg = (
            "Must specify at least one of the following parameters: ",
            "'above', 'below', 'between', or 'replace'.",
        )
        raise GMTInvalidInput(msg)

    aliasdict = AliasSystem(
        Sa=Alias(above, name="above", sep="/", size=2),
        Sb=Alias(below, name="below", sep="/", size=2),
        Si=Alias(between, name="between", sep="/", size=3, ndim=2),
        Sr=Alias(replace, name="replace", sep="/", size=2, ndim=2),
    ).add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdclip", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
