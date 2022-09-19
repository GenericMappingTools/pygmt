"""
Function to load raster basemap tiles from XYZ tile providers, and load as
:class:`xarray.DataArray`.
"""

try:
    import contextily
except ImportError:
    contextily = None

import numpy as np
import xarray as xr


def load_map_tiles(region, source=None, lonlat=False, **kwargs):
    """
    Load a georeferenced raster basemap from XYZ tile providers.

    The tiles that compose the map are merged and georeferenced into an
    :class:`xarray.DataArray` image with 3 bands (RGB). Note that the returned
    image is in a Spherical Mercator (EPSG:3857) coordinate reference system.

    Parameters
    ----------
    region : list
        The bounding box of the map in the form of a list [*xmin*, *xmax*,
        *ymin*, *ymax*]. These coordinates should be in Spherical Mercator
        (EPSG:3857) if ``lonlat=False``, or longitude/latitude if
        ``lonlat=True``.

    source : xyzservices.TileProvider or str
        [Optional. Default: Stamen Terrain web tiles] The tile source: web tile
        provider or path to local file. The web tile provider can be in the
        form of a :class:`xyzservices.TileProvider` object or a URL. The
        placeholders for the XYZ in the URL need to be {x}, {y}, {z},
        respectively. For local file paths, the file is read with rasterio and
        all bands are loaded into the basemap. IMPORTANT: tiles are assumed to
        be in the Spherical Mercator projection (EPSG:3857).

    lonlat : bool
        [Optional. Default: False]. If True, coordinates in ``region`` are
        assumed to be lon/lat as opposed to Spherical Mercator.

    kwargs : dict
        Extra keyword arguments to pass to :func:`contextily.bounds2img`.

    Returns
    -------
    raster : xarray.DataArray
        Georefenced 3D data array of RGB value.

    Raises
    ------
    ModuleNotFoundError
        If ``contextily`` is not installed. Follow
        :doc:`install instructions for contextily <contextily:index>`, (e.g.
        via ``pip install contextily``) before using this function.

    Examples
    --------
    >>> import contextily
    >>> from pygmt.datasets import load_map_tiles
    >>> raster = load_map_tiles(
    ...     region=[103.60, 104.06, 1.22, 1.49],  # West, East, South, North
    ...     source=contextily.providers.Stamen.TerrainBackground,
    ...     lonlat=True,  # bounding box coordinates are longitude/latitude
    ... )
    >>> raster.sizes
    Frozen({'band': 3, 'y': 1024, 'x': 1536})
    >>> raster.coords
    Coordinates:
      * band     (band) int64 0 1 2
      * y        (y) float64 1.663e+05 1.663e+05 1.663e+05 ... 1.272e+05 ...
      * x        (x) float64 1.153e+07 1.153e+07 1.153e+07 ... 1.158e+07 ...
    """
    if contextily is None:
        raise ModuleNotFoundError(
            "Package `contextily` is required to be installed to use this function. "
            "Please use `pip install contextily` or "
            "`conda install -c conda-forge contextily` "
            "to install the package"
        )

    west, east, south, north = region
    image, extent = contextily.bounds2img(
        w=west, s=south, e=east, n=north, source=source, ll=lonlat, **kwargs
    )

    # Turn RGBA image from channel-last to channel-first and get 3band RGB only
    _image = image.transpose(2, 0, 1)  # Change image from (H, W, C) to (C, H, W)
    rgb_image = _image[0:3, :, :]  # Get just RGB by dropping RGBA's alpha channel

    # Georeference RGB image into an xarray.DataArray
    left, right, bottom, top = extent  # xmin, xmax, ymin, ymax
    dataarray = xr.DataArray(
        data=rgb_image,
        coords=dict(
            band=[0, 1, 2],  # Red, Green, Blue
            y=np.linspace(start=top, stop=bottom, num=rgb_image.shape[1]),
            x=np.linspace(start=left, stop=right, num=rgb_image.shape[2]),
        ),
        dims=("band", "y", "x"),
    )

    # If rioxarray is installed, set the coordinate reference system
    if hasattr(dataarray, "rio"):
        dataarray = dataarray.rio.write_crs(input_crs="EPSG:3857")

    return dataarray
