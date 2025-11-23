"""
Test Figure.choropleth.
"""

import pytest
from pygmt import Figure, makecpt

gpd = pytest.importorskip("geopandas")


@pytest.mark.mpl_image_compare
def test_choropleth():
    """
    Test Figure.choropleth method.
    """
    gdf = gpd.read_file("https://geodacenter.github.io/data-and-lab/data/airbnb.zip")
    fig = Figure()
    makecpt(
        cmap="acton",
        series=[gdf["population"].min(), gdf["population"].max(), 10],
        continuous=True,
        reverse=True,
    )
    fig.choropleth(gdf, column="population", pen="0.3p,gray10")
    fig.colorbar(frame=True)
    return fig
