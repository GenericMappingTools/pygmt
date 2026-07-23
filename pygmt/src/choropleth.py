"""
choropleth - Plot a choropleth map.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import GeoLike, PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Axis, Frame

__doctest_skip__ = ["choropleth"]


@fmt_docstring
def choropleth(
    self,
    data: GeoLike | PathLike,
    column: str,
    cmap: str | bool = True,
    intensity: float | None = None,
    pen: str | None = None,
    no_clip: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
):
    """
    Plot a choropleth map.

    This method creates a choropleth map by filling each polygon according to an
    attribute value. It requires the input data to be a geo-like Python object that
    implements ``__geo_interface__`` and includes the values used to fill the polygons
    as an attribute field (e.g. a :class:`geopandas.GeoDataFrame`), or an OGR_GMT file
    containing the geometry and data to plot.

    **Aliases:**

    .. hlist::
       :columns: 3

       - B = frame
       - C = cmap
       - I = intensity
       - J = projection
       - R = region
       - N = no_clip
       - W = pen
       - V = verbose
       - a = column
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    data
        A geo-like Python object which implements ``__geo_interface__`` and includes
        the values used to fill the polygons as an attribute field (e.g. a
        :class:`geopandas.GeoDataFrame`), or an OGR_GMT file containing the geometry and
        data to plot.
    column
        The name of the data column to use for the fill.
    cmap
        The CPT to use for filling the polygons. If set to ``True``, the current CPT
        will be used.
    intensity
        The intensity (nominally in the ±1 range) to modulate the fill color by
        simulating illumination [Default is no illumination].
    no_clip
        Do **not** clip polygons that fall outside the frame boundaries.
    $pen
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency

    Examples
    --------
    >>> import geopandas
    >>> import pygmt
    >>> world = geopandas.read_file(
    ...     "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    ... )
    >>> world["POP_EST"] *= 1e-6  # Population in millions
    >>>
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[-19.5, 53, -38, 37.5], projection="M15c", frame=True)
    >>> pygmt.makecpt(cmap="bilbao", series=(0, 270, 10), reverse=True)
    >>> fig.choropleth(world, column="POP_EST", pen="0.3p,gray10")
    >>> fig.colorbar(frame=True)
    >>> fig.show()
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        C=Alias(cmap, name="cmap"),
        I=Alias(intensity, name="intensity"),
        N=Alias(no_clip, name="no_clip"),
        W=Alias(pen, name="pen"),
        a=Alias(f"Z={column}", name="column"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    # Force -G+z and -L to be set for choropleth
    aliasdict.update({"G": "+z", "L": True})

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="plot", args=build_arg_list(aliasdict, infile=vintbl)
            )
