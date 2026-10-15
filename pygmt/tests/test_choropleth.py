"""
Test Figure.choropleth.
"""

import numpy as np
import pytest
from pygmt import Figure, makecpt
from pygmt.exceptions import GMTTypeError, GMTValueError

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


def test_choropleth_invalid_column(world):
    """
    Test that a nonexistent column raises an error.
    """
    fig = Figure()
    with pytest.raises(GMTValueError):
        fig.choropleth(world, column="invalid")


def test_choropleth_geometry_column(world):
    """
    Test that the geometry column is rejected, since it's not an attribute field.
    """
    fig = Figure()
    with pytest.raises(GMTValueError, match="Invalid column name: 'geometry'"):
        fig.choropleth(world, column="geometry")


def test_choropleth_invalid_data_kind():
    """
    Test that data that is neither geo-like nor a file name raises an error.
    """
    fig = Figure()
    with pytest.raises(GMTTypeError, match="Unrecognized data type"):
        fig.choropleth(np.array([[1.0, 2.0], [3.0, 4.0]]), column="POP")
