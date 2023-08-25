"""
tilemap - Plot XYZ tile maps.
"""
from pygmt.clib import Session
from pygmt.datasets.tile_map import load_tile_map
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias

try:
    import rioxarray
except ImportError:
    rioxarray = None


@fmt_docstring
@use_alias(
    B="frame",
    E="dpi",
    I="shading",
    J="projection",
    M="monochrome",
    N="no_clip",
    Q="nan_transparent",
    # R="region",
    V="verbose",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(c="sequence_comma", p="sequence")  # R="sequence",
def tilemap(
    self, region, zoom="auto", source=None, lonlat=True, wait=0, max_retries=2, **kwargs
):
    r"""
    Plots an XYZ tile map.

    This method loads XYZ tile maps from a tile server or local file using
    :func:`pygmt.datasets.load_tile_map` into a georeferenced form, and plots
    the tiles as a basemap or overlay using :meth:`pygmt.Figure.grdimage`.

    **Note**: By default, standard web map tiles served in a Spherical Mercator
    (EPSG:3857) Cartesian format will be reprojected to a geographic coordinate
    reference system (OGC:WGS84) and plotted with longitude/latitude bounds
    when ``lonlat=True``. If reprojection is not desired, please set
    ``lonlat=False`` and provide Spherical Mercator (EPSG:3857) coordinates to
    the ``region`` parameter.

    {aliases}

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
          XYZ in the URL need to be {{x}}, {{y}}, {{z}}, respectively. E.g.
          ``https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png``.
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

    kwargs : dict
        Extra keyword arguments to pass to :meth:`pygmt.Figure.grdimage`.

    Raises
    ------
    ImportError
        If ``rioxarray`` is not installed. Follow
        :doc:`install instructions for rioxarray <rioxarray:installation>`,
        (e.g. via ``python -m pip install rioxarray``) before using this
        function.
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    if rioxarray is None:
        raise ImportError(
            "Package `rioxarray` is required to be installed to use this function. "
            "Please use `python -m pip install rioxarray` or "
            "`mamba install -c conda-forge rioxarray` "
            "to install the package."
        )

    raster = load_tile_map(
        region=region,
        zoom=zoom,
        source=source,
        lonlat=lonlat,
        wait=wait,
        max_retries=max_retries,
    )

    # Reproject raster from Spherical Mercator (EPSG:3857) to
    # lonlat (OGC:CRS84) if bounding box region was provided in lonlat
    if lonlat and raster.rio.crs == "EPSG:3857":
        raster = raster.rio.reproject(dst_crs="OGC:CRS84")
        raster.gmt.gtype = 1  # set to geographic type

    # Only set region if no_clip is None or False, so that plot is clipped to
    # exact bounding box region
    if kwargs.get("N") in [None, False]:
        kwargs["R"] = "/".join(str(coordinate) for coordinate in region)

    with Session() as lib:
        file_context = lib.virtualfile_from_data(check_kind="raster", data=raster)
        with file_context as infile:
            lib.call_module(
                module="grdimage", args=build_arg_string(kwargs, infile=infile)
            )
