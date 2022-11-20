"""
Internal function to download remote Earth datasets.
"""
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings
from pygmt.io import load_dataarray
from pygmt.src import grdcut, which


@kwargs_to_strings(region="sequence")
def _load_earth_dataset(
    resolution,
    region,
    registration,
    non_tiled_resolutions,
    tiled_resolutions,
    dataset_prefix,
    dataset_name,
):
    r"""
    Load Earth datasets.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d`` and ``m`` stand for
        arc-degree and arc-minute.

    region : str or list
        The subregion of the grid to load, in the forms of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minute (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth dataset grid.

    Note
    ----
    The :class:`xarray.DataArray` grid doesn't support slice operation, for
    Earth seafloor crustal age with resolutions of 5 arc-minutes or higher,
    which are stored as smaller tiles.
    """

    if registration in ("pixel", "gridline", None):
        # If None, let GMT decide on Pixel/Gridline type
        reg = f"_{registration[0]}" if registration else ""
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: '{registration}', should be either "
            "'pixel', 'gridline' or None. Default is None, where a "
            "pixel-registered grid is returned unless only the "
            "gridline-registered grid is available."
        )

    if resolution not in non_tiled_resolutions + tiled_resolutions:
        raise GMTInvalidInput(f"Invalid {dataset_name} resolution '{resolution}'.")

    # different ways to load tiled and non-tiled earth age data
    # Known issue: tiled grids don't support slice operation
    # See https://github.com/GenericMappingTools/pygmt/issues/524
    if region is None:
        if resolution not in non_tiled_resolutions:
            raise GMTInvalidInput(
                f"'region' is required for {dataset_name} resolution '{resolution}'."
            )
        fname = which(f"@{dataset_prefix}{resolution}{reg}", download="a")
        grid = load_dataarray(fname, engine="netcdf4")
    else:
        grid = grdcut(f"@{dataset_prefix}{resolution}{reg}", region=region)
    return grid
