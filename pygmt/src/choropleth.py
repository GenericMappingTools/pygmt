"""
choropleth - Plot a choropleth map.
"""

from pygmt._typing import GeoLike, PathLike


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
    :class:`geopandas.GeoDataFrame`), or a OGR_GMT file contaning the geometry and data
    to plot.

    Parameters
    ----------
    data
        A geo-like Python object which implements ``__geo_interface__`` (e.g. a
        :class:`geopandas.GeoDataFrame` or :class:`shapely.geometry`), or a OGR_GMT file
        containing the geometry and data to plot.
    column
        The name of the data column to use for the fill.
    cmap
        The CPT to use for filling the polygons. If set to ``True``, the current CPT
        will be used.
    **kwargs
        Additional keyword arguments passed to :meth:`pygmt.Figure.plot`.

    Examples
    --------
    >>> import geopandas as gpd
    >>> import pygmt
    >>> gdf = gpd.read_file(
    ...     "https://geodacenter.github.io/data-and-lab/data/airbnb.zip"
    ... )

    >>> fig = pygmt.Figure()
    >>> pygmt.makecpt(
    ...     cmap="acton",
    ...     series=[gdf["population"].min(), gdf["population"].max(), 10],
    ...     continuous=True,
    ...     reverse=True,
    ... )
    >>> fig.choropleth(gdf, column="population", pen="0.3p,gray10")
    >>> fig.colorbar(frame=True)
    >>> fig.show()
    """
    self.plot(
        data=data, close=True, fill="+z", cmap=cmap, aspatial=f"Z={column}", **kwargs
    )
