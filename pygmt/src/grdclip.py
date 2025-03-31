"""
grdclip - Clip the range of grid values.
"""

from collections.abc import Sequence

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdclip"]


def _parse_sequence(name, value, separator="/", size=2, ndim=1):
    """
    Parse a 1-D or 2-D sequence of values and join them by a separator.

    Parameters
    ----------
    name
        The parameter name.
    value
        The 1-D or 2-D sequence of values to parse.
    separator
        The separator to join the values.
    size
        The number of values in the sequence.
    ndim
        The expected maximum number of dimensions of the sequence.

    Returns
    -------
    str
        The parsed sequence.

    Examples
    --------
    >>> _parse_sequence("above_or_below", [1000, 0], size=2, ndim=1)
    '1000/0'
    >>> _parse_sequence("between", [1000, 1500, 10000], size=3, ndim=2)
    '1000/1500/10000'
    >>> _parse_sequence("between", [[1000, 1500, 10000]], size=3, ndim=2)
    ['1000/1500/10000']
    >>> _parse_sequence(
    ...     "between", [[1000, 1500, 10000], [1500, 2000, 20000]], size=3, ndim=2
    ... )
    ['1000/1500/10000', '1500/2000/20000']
    >>> _parse_sequence("replace", [1000, 0], size=2, ndim=2)
    '1000/0'
    >>> _parse_sequence("replace", [[1000, 0]], size=2, ndim=2)
    ['1000/0']
    >>> _parse_sequence("replace", [[1000, 0], [1500, 10000]], size=2, ndim=2)
    ['1000/0', '1500/10000']
    >>> _parse_sequence("any", "1000/100")
    '1000/100'
    >>> _parse_sequence("any", None)
    >>> _parse_sequence("any", [])
    []
    >>> _parse_sequence("above_or_below", [[100, 1000], [1500, 2000]], size=2, ndim=1)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Parameter ... must be a 1-D sequence...
    >>> _parse_sequence("above_or_below", [100, 200, 300], size=2, ndim=1)
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTInvalidInput: Parameter .. must be a 1-D sequence ...
    >>> _parse_sequence("between", [[100, 200, 300], [500, 600]], size=3, ndim=2)
    Traceback (most recent call last):
    ...
    pygmt.exceptions.GMTInvalidInput: Parameter .. must be a 2-D sequence with ...
    """
    # Return the value as is if not a sequence (e.g., str or None) or empty.
    if not is_nonstr_iter(value) or len(value) == 0:
        return value

    # 1-D sequence
    if not is_nonstr_iter(value[0]):
        if len(value) != size:
            msg = (
                f"Parameter '{name}' must be a 1-D sequence of {size} values, "
                f"but got {len(value)} values."
            )
            raise GMTInvalidInput(msg)
        return separator.join(str(i) for i in value)

    # 2-D sequence
    if ndim == 1:
        msg = f"Parameter '{name}' must be a 1-D sequence, not a 2-D sequence."
        raise GMTInvalidInput(msg)

    if any(len(i) != size for i in value):
        msg = (
            f"Parameter '{name}' must be a 2-D sequence with each sub-sequence "
            f"having {size} values."
        )
        raise GMTInvalidInput(msg)
    return [separator.join(str(j) for j in value[i]) for i in range(len(value))]


# TODO(PyGMT>=0.19.0): Remove the deprecated "new" parameter.
@fmt_docstring
@deprecate_parameter("new", "replace", "v0.15.0", remove_version="v0.19.0")
@use_alias(R="region", V="verbose")
@kwargs_to_strings(R="sequence")
def grdclip(
    grid,
    outgrid: str | None = None,
    above: Sequence[float] | None = None,
    below: Sequence[float] | None = None,
    between: Sequence[float] | Sequence[Sequence[float]] | None = None,
    replace: Sequence[float] | Sequence[Sequence[float]] | None = None,
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
    if all(v is None for v in (above, below, between, replace)):
        msg = (
            "Must specify at least one of the following parameters: ",
            "'above', 'below', 'between', or 'replace'.",
        )
        raise GMTInvalidInput(msg)

    # Parse the -S option.
    kwargs["Sa"] = _parse_sequence("above", above, size=2, ndim=1)
    kwargs["Sb"] = _parse_sequence("below", below, size=2, ndim=1)
    kwargs["Si"] = _parse_sequence("between", between, size=3, ndim=2)
    kwargs["Sr"] = _parse_sequence("replace", replace, size=2, ndim=2)

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
