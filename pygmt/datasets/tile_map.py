"""
Function to load raster tile maps from XYZ tile providers, and load as
:class:`xarray.DataArray`.
"""

from collections.abc import Sequence
from typing import Literal

try:
    import contextily
    from rasterio.crs import CRS
    from xyzservices import TileProvider

    _HAS_CONTEXTILY = True
except ImportError:
    CRS = None
    TileProvider = None
    _HAS_CONTEXTILY = False

try:
    import rioxarray  # noqa: F401

    _HAS_RIOXARRAY = True
except ImportError:
    _HAS_RIOXARRAY = False

import numpy as np
import xarray as xr

__doctest_requires__ = {("load_tile_map"): ["contextily"]}


def load_tile_map(
    region: Sequence[float],
    zoom: int | Literal["auto"] = "auto",
    source: TileProvider | str | None = None,
    lonlat: bool = True,
    crs: str | CRS = "EPSG:3857",
    wait: int = 0,
    max_retries: int = 2,
    zoom_adjust: int | None = None,
) -> xr.DataArray:
    """
    Load a georeferenced raster tile map from XYZ tile providers.

    The tiles that compose the map are merged and georeferenced into an
    :class:`xarray.DataArray` image with 3 bands (RGB). Note that the returned image is
    in a Spherical Mercator (EPSG:3857) coordinate reference system (CRS) by default,
    but can be customized using the ``crs`` parameter.

    Parameters
    ----------
    region
        The bounding box of the map in the form of a list [*xmin*, *xmax*, *ymin*,
        *ymax*]. These coordinates should be in longitude/latitude if ``lonlat=True`` or
        Spherical Mercator (EPSG:3857) if ``lonlat=False``.
    zoom
        Level of detail. Higher levels (e.g. ``22``) mean a zoom level closer to the
        Earth's surface, with more tiles covering a smaller geographical area and thus
        more detail. Lower levels (e.g. ``0``) mean a zoom level further from the
        Earth's surface, with less tiles covering a larger geographical area and thus
        less detail. Default is ``"auto"`` to automatically determine the zoom level
        based on the bounding box region extent.

        .. note::
           The maximum possible zoom level may be smaller than ``22``, and depends on
           what is supported by the chosen web tile provider source.
    source
        The tile source: web tile provider or path to a local file. Provide either:

        - A web tile provider in the form of a :class:`xyzservices.TileProvider` object.
          See :doc:`Contextily providers <contextily:providers_deepdive>` for a list of
          tile providers. Default is ``xyzservices.providers.OpenStreetMap.HOT``, i.e.
          OpenStreetMap Humanitarian web tiles.
        - A web tile provider in the form of a URL. The placeholders for the XYZ in the
          URL need to be {x}, {y}, {z}, respectively. E.g.
          ``https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png``.
        - A local file path. The file is read with :doc:`rasterio <rasterio:index>` and
          all bands are loaded into the basemap. See
          :doc:`contextily:working_with_local_files`.

        .. important::
           Tiles are assumed to be in the Spherical Mercator projection (EPSG:3857).
    lonlat
        If ``False``, coordinates in ``region`` are assumed to be Spherical Mercator as
        opposed to longitude/latitude.
    crs
        Coordinate reference system (CRS) of the returned :class:`xarray.DataArray`
        image. Default is ``"EPSG:3857"`` (i.e., Spherical Mercator). The CRS can be in
        either string or :class:`rasterio.crs.CRS` format.
    wait
        If the tile API is rate-limited, the number of seconds to wait between a failed
        request and the next try.
    max_retries
        Total number of rejected requests allowed before contextily will stop trying to
        fetch more tiles from a rate-limited API.
    zoom_adjust
        The amount to adjust a chosen zoom level if it is chosen automatically. Values
        outside of -1 to 1 are not recommended as they can lead to slow execution.

    Returns
    -------
    raster
        Georeferenced 3-D data array of RGB values.

    Raises
    ------
    ImportError
        If ``contextily`` is not installed or can't be imported. Follow the
        :doc:`install instructions for contextily <contextily:index>`, (e.g. via
        ``python -m pip install contextily``) before using this function.

    Examples
    --------
    >>> import contextily
    >>> from pygmt.datasets import load_tile_map
    >>> raster = load_tile_map(
    ...     region=[-180.0, 180.0, -90.0, 0.0],  # West, East, South, North
    ...     zoom=1,  # less detailed zoom level
    ...     source=contextily.providers.OpenTopoMap,
    ...     lonlat=True,  # bounding box coordinates are longitude/latitude
    ... )
    >>> raster.sizes
    Frozen({'band': 3, 'y': 256, 'x': 512})
    >>> raster.coords  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Coordinates:
      * band         (band) uint8... 1 2 3
      * y            (y) float64... -7.081e-10 -7.858e+04 ... -1.996e+07 -2.004e+07
      * x            (x) float64... -2.004e+07 -1.996e+07 ... 1.996e+07 2.004e+07
        spatial_ref  int... 0
    >>> # CRS is set only if rioxarray is available
    >>> if hasattr(raster, "rio"):
    ...     raster.rio.crs.to_string()
    'EPSG:3857'
    """
    # The CRS of the source tile provider. If the source is a TileProvider object, use
    # its crs attribute if available. Otherwise, default to EPSG:3857.
    _source_crs = getattr(source, "crs", "EPSG:3857")

    if not _HAS_CONTEXTILY:
        msg = (
            "Package `contextily` is required to be installed to use this function. "
            "Please use `python -m pip install contextily` or "
            "`mamba install -c conda-forge contextily` to install the package."
        )
        raise ImportError(msg)

    if crs != _source_crs and not _HAS_RIOXARRAY:
        msg = (
            f"Package `rioxarray` is required if CRS is not '{_source_crs}'. "
            "Please use `python -m pip install rioxarray` or "
            "`mamba install -c conda-forge rioxarray` to install the package."
        )
        raise ImportError(msg)

    # Keyword arguments for contextily.bounds2img
    contextily_kwargs = {
        "zoom": zoom,
        "source": source,
        "ll": lonlat,
        "wait": wait,
        "max_retries": max_retries,
        "zoom_adjust": zoom_adjust,
    }

    west, east, south, north = region
    image, extent = contextily.bounds2img(
        w=west, s=south, e=east, n=north, **contextily_kwargs
    )

    # Turn RGBA img from channel-last to channel-first and get 3-band RGB only
    _image = image.transpose(2, 0, 1)  # Change image from (H, W, C) to (C, H, W)
    rgb_image = _image[0:3, :, :]  # Get just RGB by dropping RGBA's alpha channel

    # Georeference RGB image into an xarray.DataArray
    left, right, bottom, top = extent
    dataarray = xr.DataArray(
        data=rgb_image,
        coords={
            "band": np.array(object=[1, 2, 3], dtype=np.uint8),  # Red, Green, Blue
            "y": np.linspace(start=top, stop=bottom, num=rgb_image.shape[1]),
            "x": np.linspace(start=left, stop=right, num=rgb_image.shape[2]),
        },
        dims=("band", "y", "x"),
    )

    # If rioxarray is installed, set the coordinate reference system.
    if hasattr(dataarray, "rio"):
        dataarray = dataarray.rio.write_crs(input_crs=_source_crs)

        # Reproject raster image from the source CRS to the specified CRS.
        if crs != _source_crs:
            dataarray = dataarray.rio.reproject(dst_crs=crs)

    return dataarray
