"""
Test Figure.choropleth.
"""

import pytest
from pygmt import Figure, makecpt

geopandas = pytest.importorskip("geopandas")


@pytest.fixture(scope="module", name="world")
def fixture_world():
    """
    Download and cache the Natural Earth countries dataset for testing.
    """
    return geopandas.read_file(
        "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    )


@pytest.mark.mpl_image_compare
def test_choropleth(world):
    """
    Test Figure.choropleth method.
    """
    world["POP_EST"] *= 1e-6  # Population in millions

    fig = Figure()
    fig.basemap(region=[-19.5, 53, -38, 37.5], projection="M15c", frame=True)
    makecpt(cmap="bilbao", series=(0, 270, 10), reverse=True)
    fig.choropleth(world, column="POP_EST", pen="0.3p,gray10")
    fig.colorbar(frame=True)
    return fig
