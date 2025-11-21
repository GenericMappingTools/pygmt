"""
choropleth - Plot a choropleth map.
"""

import contextlib

from pygmt._typing import PathLike

with contextlib.suppress(ImportError):
    import geopandas as gpd


def choropleth(
    self,
    data: gpd.GeoDataFrame | PathLike,
    column: str,
    cmap: str | bool = True,
    **kwargs,
):
    """
    Plot a choropleth map.

    This method creates a choropleth map by filling polygons based on the values in a
    specific data column.

    Parameters
    ----------
    data
        A :class:`geopandas.DataFrame` object or a OGR_GMT file containing the geometry
        and data to plot.
    column
        The name of the data column to use for the fill.
    cmap
        The CPT to use for filling the polygons. If set to ``True``, the current
        colormap will be used.
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
    >>> fig.choropleth(gdf, fillcol="population", pen="0.3p,gray10")
    >>> fig.colorbar(frame=True)
    >>> fig.show()
    """
    self.plot(data=data, close=True, fill="+z", aspatial=f"Z={column}", **kwargs)
