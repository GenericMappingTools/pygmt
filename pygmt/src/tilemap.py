"""
tilemap - Plot XYZ tile maps.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.datasets.tile_map import load_tile_map
from pygmt.enums import GridType
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

try:
    from xyzservices import TileProvider
except ImportError:
    TileProvider = None


@fmt_docstring
@use_alias(
    B="frame",
    E="dpi",
    I="shading",
    Q="nan_transparent",
    p="perspective",
)
@kwargs_to_strings(p="sequence")
def tilemap(  # noqa: PLR0913
    self,
    region: Sequence[float],
    zoom: int | Literal["auto"] = "auto",
    source: TileProvider | str | None = None,
    lonlat: bool = True,
    wait: int = 0,
    max_retries: int = 2,
    zoom_adjust: int | None = None,
    monochrome: bool = False,
    no_clip: bool = False,
    projection: str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot an XYZ tile map.

    This method loads XYZ tile maps from a tile server or local file using
    :func:`pygmt.datasets.load_tile_map` into a georeferenced form, and plots the tiles
    as a basemap or overlay using :meth:`pygmt.Figure.grdimage`.

    **Note**: By default, standard web map tiles served in a Spherical Mercator
    (EPSG:3857) Cartesian format will be reprojected to a geographic coordinate
    reference system (OGC:CRS84) and plotted with longitude/latitude bounds when
    ``lonlat=True``. If reprojection is not desired, please set ``lonlat=False`` and
    provide Spherical Mercator (EPSG:3857) coordinates to the ``region`` parameter.

    {aliases}
       - J = projection
       - M = monochrome
       - N = no_clip
       - V = verbose
       - c = panel
       - t = transparency

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
          URL need to be ``{{x}}``, ``{{y}}``, ``{{z}}``, respectively. E.g.
          ``https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png``.
        - A local file path. The file is read with :doc:`rasterio <rasterio:index>` and
          all bands are loaded into the basemap. See
          :doc:`contextily:working_with_local_files`.

        .. important::
           Tiles are assumed to be in the Spherical Mercator projection (EPSG:3857).
    lonlat
        If ``False``, coordinates in ``region`` are assumed to be Spherical Mercator as
        opposed to longitude/latitude.
    wait
        If the tile API is rate-limited, the number of seconds to wait between a failed
        request and the next try.
    max_retries
        Total number of rejected requests allowed before contextily will stop trying to
        fetch more tiles from a rate-limited API.
    zoom_adjust
        The amount to adjust a chosen zoom level if it is chosen automatically. Values
        outside of -1 to 1 are not recommended as they can lead to slow execution.
    kwargs : dict
        Extra keyword arguments to pass to :meth:`pygmt.Figure.grdimage`.
    """
    self._activate_figure()

    raster = load_tile_map(
        region=region,
        zoom=zoom,
        source=source,
        lonlat=lonlat,
        crs="OGC:CRS84" if lonlat is True else "EPSG:3857",
        wait=wait,
        max_retries=max_retries,
        zoom_adjust=zoom_adjust,
    )
    if lonlat:
        raster.gmt.gtype = GridType.GEOGRAPHIC

    # If no_clip is not True, set region to None so that plot is clipped to exact
    # bounding box region.
    if kwargs.get("N", no_clip) not in {None, False}:
        region = None  # type: ignore[assignment]

    aliasdict = AliasSystem(
        M=Alias(monochrome, name="monochrome"),
        N=Alias(no_clip, name="no_clip"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="raster", data=raster) as vingrd:
            lib.call_module(
                module="grdimage", args=build_arg_list(aliasdict, infile=vingrd)
            )
