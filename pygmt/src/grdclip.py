"""
grdclip - Clip the range of grid values.
"""

from collections.abc import Sequence

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdclip"]


def _parse_sequence(name, value, separator="/", size=2, ndim=1):
    """
    Parse a sequence of values from a string or a list.

    >>> _parse_sequence("above", [1000, 0], size=2, ndim=1)
    '1000/0'
    >>> _parse_sequence("below", [1000, 0], size=2, ndim=1)
    '1000/0'
    >>> _parse_sequence("between", [1000, 1500, 10000], size=3, ndim=2)
    '1000/1500/10000'
    >>> _parse_sequence("between", [[1000, 1500, 10000]], size=3, ndim=2)
    ['1000/1500/10000']
    >>> _parse_sequence(
    ...     "between", [[1000, 1500, 10000], [1500, 2000, 20000]], size=3, ndim=2
    ... )
    ['1000/1500/10000', '1500/2000/20000']
    >>> _parse_sequence("replace", [1000, 0], size=2, ndim=1)
    '1000/0'
    >>> _parse_sequence("replace", [[1000, 0], [1500, 10000]], size=2, ndim=2)
    ['1000/0', '1500/10000']
    """
    if not is_nonstr_iter(value):  # Not a sequence. Likely str or None.
        return value

    # A sequence of sequences.
    if len(value) == 0:
        return None
    if is_nonstr_iter(value[0]):  # 2-D sequence
        if ndim == 1:
            msg = f"Parameter '{name}' must be a 1-D sequence, not a 2-D sequence."
            raise GMTInvalidInput(msg)

        actual_sizes = {len(i) for i in value}
        if len(actual_sizes) != 1 or actual_sizes != {size}:
            msg = f"Parameter '{name}' must be a 1-D or 2D sequence with {size} values."
            raise GMTInvalidInput(msg)
        return [separator.join(str(j) for j in value[i]) for i in range(len(value))]

    # A sequence.
    if len(value) != size:
        msg = f"Parameter '{name}' must be a 1-D sequence of {size} values, but got {len(value)}."
        raise GMTInvalidInput(msg)
    return separator.join(str(i) for i in value)


@fmt_docstring
@use_alias(R="region", V="verbose")
@kwargs_to_strings(R="sequence")
def grdclip(
    grid,
    outgrid: str | None = None,
    above: Sequence[float] | None = None,
    below: Sequence[float] | None = None,
    between: Sequence[float] | Sequence[Sequence[float]] | None = None,
    new: Sequence[float] | Sequence[Sequence[float]] | None = None,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Clip the range of grid values.

    This function operates on the values of a grid. It can:

    - Set values smaller than a threshold to a new value
    - Set values larger than a threshold to a new value
    - Set values within a range to a new value
    - Replace individual values with a new value

    Such operations are useful when you want all of a continent or an ocean to fall into
    one color or gray shade in image processing, when clipping of the range of data
    values is required, or for reclassification of data values. The values can be any
    number or even NaN (Not a Number).

    Full option list at :gmt-docs:`grdclip.html`

    {aliases}

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
    new
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
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Report the minimum and maximum data values
    >>> [grid.data.min(), grid.data.max()]
    [183.5, 1807.0]
    >>> # Create a new grid from an input grid. Set all values below 1,000 to
    >>> # 0 and all values above 1,500 to 10,000
    >>> new_grid = pygmt.grdclip(grid=grid, below=[1000, 0], above=[1500, 10000])
    >>> # Report the minimum and maximum data values
    >>> [new_grid.data.min(), new_grid.data.max()]
    [0.0, 10000.0]
    """
    if all(v is None for v in (above, below, between, new)):
        msg = (
            "Must specify at least one of the following parameters: ",
            "'above', 'below', 'between', or 'new'.",
        )
        raise GMTInvalidInput(msg)

    # Parse the -S option.
    kwargs["Sa"] = _parse_sequence("above", above, size=2)
    kwargs["Sb"] = _parse_sequence("below", below, size=2)
    kwargs["Si"] = _parse_sequence("between", between, size=3, ndim=2)
    kwargs["Sr"] = _parse_sequence("new", new, size=2, ndim=2)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="grdclip", args=build_arg_list(kwargs, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
