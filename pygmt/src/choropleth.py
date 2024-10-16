"""
choropleth - Plot a choropleth map.
"""


def choropleth(self, data, fillcol: str, **kwargs):
    """
    Plot a choropleth map.

    Parameters
    ----------
    data : :class:`geopandas.GeoDataFrame`
        The geopandas dataframe containing the geometry and data to plot.
    fillcol
        The column name of the data to use for the fill.
    """
    self.plot(
        data=data,
        close=True,
        fill="+z",
        aspatial=f"Z={fillcol}",
        **kwargs,
    )
