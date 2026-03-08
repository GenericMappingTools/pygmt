"""
choropleth - Plot a choropleth map.
"""

from pygmt._typing import GeoLike, PathLike

__doctest_skip__ = ["choropleth"]


def choropleth(
    self,
    data: GeoLike | PathLike,
    column: str,
    cmap: str | bool = True,
    **kwargs,
):
    """
    Plot a choropleth map.

    This method is a thin wrapper around :meth:`pygmt.Figure.plot` that sets the
    appropriate parameters for creating a choropleth map by filling polygons based on
    values in a specified data column. It requires the input data to be a geo-like
    Python object that implements ``__geo_interface__`` (e.g. a
    :class:`geopandas.GeoDataFrame`), or an OGR_GMT file containing the geometry and
    data to plot.

    Parameters
    ----------
    data
        A geo-like Python object which implements ``__geo_interface__`` (e.g. a
        :class:`geopandas.GeoDataFrame` or :class:`shapely.geometry`), or an OGR_GMT
        file containing the geometry and data to plot.
    column
        The name of the data column to use for the fill.
    cmap
        The CPT to use for filling the polygons. If set to ``True``, the current CPT
        will be used.
    **kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.plot`.

    Examples
    --------
    >>> import geopandas
    >>> import pygmt
    >>> world = geopandas.read_file(
    ...     "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    ... )
    >>> world["POP_EST"] *= 1e-6  # Population in millions

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[-19.5, 53, -38, 37.5], projection="M15c", frame=True)
    >>> pygmt.makecpt(cmap="bilbao", series=(0, 270, 10), reverse=True)
    >>> fig.choropleth(world, column="POP_EST", pen="0.3p,gray10")
    >>> fig.colorbar(frame=True)
    >>> fig.show()
    """
    self.plot(
        data=data, close=True, fill="+z", cmap=cmap, aspatial=f"Z={column}", **kwargs
    )
