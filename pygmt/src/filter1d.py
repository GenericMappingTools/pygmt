"""
filter1d - Time domain filtering of 1-D data tables.
"""

from typing import Literal

import numpy as np
import pandas as pd
from pygmt._typing import PathLike, TableLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    use_alias,
    validate_output_table_type,
)


@fmt_docstring
@use_alias(E="end", F="filter_type", N="time_col")
def filter1d(
    data: PathLike | TableLike,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: PathLike | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> pd.DataFrame | np.ndarray | None:
    r"""
    Time domain filtering of 1-D data tables.

    A general time domain filter for multiple column time
    series data. The user specifies which column is the time (i.e., the
    independent variable) via ``time_col``. The fastest operation
    occurs when the input time series are equally spaced and have no gaps or
    outliers and the special options are not needed.
    Read a table and output as a :class:`numpy.ndarray`,
    :class:`pandas.DataFrame`, or ASCII file.

    Full GMT docs at :gmt-docs:`filter1d.html`.

    {aliases}
       - V = verbose

    Parameters
    ----------
    {output_type}
    {outfile}
    filter_type : str
        **type**\ *width*\ [**+h**].
        Set the filter **type**. Choose among convolution and non-convolution
        filters. Append the filter code followed by the full filter
        *width* in same units as time column. By default, this
        performs a low-pass filtering; append **+h** to select high-pass
        filtering. Some filters allow for optional arguments and a modifier.

        Available convolution filter types are:

        - **b**: boxcar. All weights are equal.
        - **c**: cosine arch. Weights follow a cosine arch curve.
        - **g**: Gaussian. Weights are given by the Gaussian function.
        - **f**: custom. Instead of *width* give name of a one-column file
          with your own weight coefficients.

        Non-convolution filter types are:

        - **m**: median. Returns median value.
        - **p**: maximum likelihood probability (a mode estimator). Return
          modal value. If more than one mode is found we return their average
          value. Append **+l** or **+u** if you rather want
          to return the lowermost or uppermost of the modal values.
        - **l**: lower (absolute). Return the minimum of all values.
        - **L**: lower. Return minimum of all positive values only.
        - **u**: upper (absolute). Return maximum of all values.
        - **U**: upper. Return maximum of all negative values only.

        Uppercase type **B**, **C**, **G**, **M**, **P**, **F** will use
        robust filter versions: i.e., replace outliers (2.5 L1 scale off
        median, using 1.4826 \* median absolute deviation [MAD]) with median
        during filtering.

        In the case of **L**\|\ **U** it is possible that no data passes
        the initial sign test; in that case the filter will return 0.0.
        Apart from custom coefficients (**f**), the other filters may accept
        variable filter widths by passing *width* as a two-column time-series
        file with filter widths in the second column.  The filter-width file
        does not need to be co-registered with the data as we obtain the
        required filter width at each output location via interpolation.  For
        multi-segment data files the filter file must either have the same
        number of segments or just a single segment to be used for all data
        segments.

    end : bool
        Include ends of time series in output. The default [False] loses
        half the filter-width of data at each end.

    time_col : int
        Indicate which column contains the independent variable (time). The
        left-most column is 0, while the right-most is (*n_cols* - 1)
        [Default is ``0``].

    Returns
    -------
    ret
        Return type depends on ``outfile`` and ``output_type``:

        - ``None`` if ``outfile`` is set (output will be stored in the file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not set
          (depends on ``output_type``)
    """
    if kwargs.get("F") is None:
        msg = "Pass a required argument to 'filter_type'."
        raise GMTInvalidInput(msg)

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
                module="filter1d",
                args=build_arg_list(aliasdict, infile=vintbl, outfile=vouttbl),
            )
        return lib.virtualfile_to_dataset(vfname=vouttbl, output_type=output_type)
