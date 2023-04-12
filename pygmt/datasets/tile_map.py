"""
Function to load raster tile maps from XYZ tile providers, and load as
:class:`xarray.DataArray`.
"""

try:
    import contextily
except ImportError:
    contextily = None

import numpy as np
import xarray as xr

__doctest_requires__ = {("load_tile_map"): ["contextily"]}


def load_tile_map(region, zoom="auto", source=None, lonlat=True, wait=0, max_retries=2):
    """
    Load a georeferenced raster tile map from XYZ tile providers.

    The tiles that compose the map are merged and georeferenced into an
    :class:`xarray.DataArray` image with 3 bands (RGB). Note that the returned
    image is in a Spherical Mercator (EPSG:3857) coordinate reference system.

    Parameters
    ----------
    region : list
        The bounding box of the map in the form of a list [*xmin*, *xmax*,
        *ymin*, *ymax*]. These coordinates should be in longitude/latitude if
        ``lonlat=True`` or Spherical Mercator (EPSG:3857) if ``lonlat=False``.

    zoom : int or str
        Optional. Level of detail. Higher levels (e.g. ``22``) mean a zoom
        level closer to the Earth's surface, with more tiles covering a smaller
        geographical area and thus more detail. Lower levels (e.g. ``0``) mean
        a zoom level further from the Earth's surface, with less tiles covering
        a larger geographical area and thus less detail [Default is
        ``"auto"`` to automatically determine the zoom level based on the
        bounding box region extent].

        **Note**: The maximum possible zoom level may be smaller than ``22``,
        and depends on what is supported by the chosen web tile provider
        source.

    source : xyzservices.TileProvider or str
        Optional. The tile source: web tile provider or path to a local file.
        Provide either:

        - A web tile provider in the form of a
          :class:`xyzservices.TileProvider` object. See
          :doc:`Contextily providers <contextily:providers_deepdive>` for a
          list of tile providers [Default is
          ``xyzservices.providers.Stamen.Terrain``, i.e. Stamen Terrain web
          tiles].
        - A web tile provider in the form of a URL. The placeholders for the
          XYZ in the URL need to be {x}, {y}, {z}, respectively. E.g.
          ``https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png``.
        - A local file path. The file is read with
          :doc:`rasterio <rasterio:index>` and all bands are loaded into the
          basemap. See
          :doc:`contextily:working_with_local_files`.

        IMPORTANT: Tiles are assumed to be in the Spherical Mercator projection
        (EPSG:3857).

    lonlat : bool
        Optional. If ``False``, coordinates in ``region`` are assumed to be
        Spherical Mercator as opposed to longitude/latitude [Default is
        ``True``].

    wait : int
        Optional. If the tile API is rate-limited, the number of seconds to
        wait between a failed request and the next try [Default is ``0``].

    max_retries : int
        Optional. Total number of rejected requests allowed before contextily
        will stop trying to fetch more tiles from a rate-limited API [Default
        is ``2``].

    Returns
    -------
    raster : xarray.DataArray
        Georeferenced 3-D data array of RGB values.

    Raises
    ------
    ImportError
        If ``contextily`` is not installed or can't be imported. Follow
        :doc:`install instructions for contextily <contextily:index>`, (e.g.
        via ``python -m pip install contextily``) before using this function.

    Examples
    --------
    >>> import contextily
    >>> from pygmt.datasets import load_tile_map
    >>> raster = load_tile_map(
    ...     region=[-180.0, 180.0, -90.0, 0.0],  # West, East, South, North
    ...     zoom=1,  # less detailed zoom level
    ...     source=contextily.providers.Stamen.TerrainBackground,
    ...     lonlat=True,  # bounding box coordinates are longitude/latitude
    ... )
    >>> raster.sizes
    Frozen({'band': 3, 'y': 256, 'x': 512})
    >>> raster.coords
    Coordinates:
      * band         (band) uint8 0 1 2
      * y            (y) float64 -7.081e-10 -7.858e+04 ... -1.996e+07 ...
      * x            (x) float64 -2.004e+07 -1.996e+07 ... 1.996e+07 2.004e+07
    """
    # pylint: disable=too-many-locals
    if contextily is None:
        raise ImportError(
            "Package `contextily` is required to be installed to use this function. "
            "Please use `python -m pip install contextily` or "
            "`mamba install -c conda-forge contextily` "
            "to install the package."
        )

    west, east, south, north = region
    image, extent = contextily.bounds2img(
        w=west,
        s=south,
        e=east,
        n=north,
        zoom=zoom,
        source=source,
        ll=lonlat,
        wait=wait,
        max_retries=max_retries,
    )

    # Turn RGBA img from channel-last to channel-first and get 3-band RGB only
    _image = image.transpose(2, 0, 1)  # Change image from (H, W, C) to (C, H, W)
    rgb_image = _image[0:3, :, :]  # Get just RGB by dropping RGBA's alpha channel

    # Georeference RGB image into an xarray.DataArray
    left, right, bottom, top = extent
    dataarray = xr.DataArray(
        data=rgb_image,
        coords={
            "band": np.uint8([0, 1, 2]),  # Red, Green, Blue
            "y": np.linspace(start=top, stop=bottom, num=rgb_image.shape[1]),
            "x": np.linspace(start=left, stop=right, num=rgb_image.shape[2]),
        },
        dims=("band", "y", "x"),
    )

    # If rioxarray is installed, set the coordinate reference system
    if hasattr(dataarray, "rio"):
        dataarray = dataarray.rio.set_crs(input_crs="EPSG:3857")

    return dataarray
