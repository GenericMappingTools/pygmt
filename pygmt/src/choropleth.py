"""
choropleth - Plot a choropleth map.
"""

import contextlib

with contextlib.suppress(ImportError):
    import geopandas as gpd


def choropleth(self, data: gpd.GeoDataFrame, column: str, **kwargs):
    """
    Plot a choropleth map.

    Parameters
    ----------
    data
        A :class:`geopandas.DataFrame` object or a OGR_GMT file containing the geometry
        and data to plot.
    column
        The name of the data column to use for the fill.
    """
    self.plot(
        data=data,
        close=True,
        fill="+z",
        aspatial=f"Z={column}",
        **kwargs,
    )
