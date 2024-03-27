def choropleth(self, data, fillcol, cmap=True, **kwargs):
    """
    Plot a choropleth map from a :class:`geopandas.GeoDataFrame` object.

    Parameters
    ----------
    data : :class:`geopandas.GeoDataFrame`
        The geopandas dataframe containing the geometry and data to plot.
    fillcol : str
        The column name of the data to use for the fill.
    cmap : str
    """
    self.plot(
        data=data,
        close=True,
        fill="+z",
        cmap=cmap,
        aspatial=f"Z={fillcol}",
        **kwargs,
    )