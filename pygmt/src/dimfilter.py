"""
dimfilter - Filter a grid file by dividing the filter circle.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    D="distance",
    F="filter",
    G="outgrid",
    I="spacing",
    N="sectors",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def dimfilter(grid, **kwargs):
    r"""
    Filter a grid file by dividing the filter circle.

    Filter a grid file in the space (or time) domain by
    dividing the given filter circle into *n\_sectors*, applying one of the
    selected primary convolution or non-convolution filters to each sector,
    and choosing the final outcome according to the selected secondary
    filter. It computes distances using Cartesian or Spherical geometries.
    The output *.nc* file can optionally be generated as a subregion of the
    input and/or with a new **-I**\ ncrement. In this way, one may have
    "extra space" in the input data so that there will be no edge effects
    for the output grid. If the filter is low-pass, then the output may be
    less frequently sampled than the input. The **-Q** option is for the
    error analysis mode and expects the input file to contains the filtered
    depths. Finally, one should know that **dimfilter** will not produce a
    smooth output as other spatial filters
    do because it returns a minimum median out of *N* medians of *N*
    sectors. The output can be rough unless the input data is noise-free.
    Thus, an additional filtering (e.g., Gaussian via :doc:`grdfilter`) of the
    DiM-filtered data is generally recommended.

    Full option list at :gmt-docs:`dimfilter.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("dimfilter", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
