"""
Tests for fig.clip.
"""

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import Figure
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the static_earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return pd.DataFrame(data={"x": [-52, -50, -50, -52], "y": [-20, -20, -16, -16]})


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return [-55, -47, -24, -10]


@pytest.fixture(scope="module", name="projection")
def fixture_projection():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return "M4c"


@pytest.mark.mpl_image_compare(filename="test_clip.png")
def test_clip_xy(grid, dataframe, region, projection):
    """
    Test clip with x,y input.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True, projection=projection)
    with fig.clip(x=dataframe["x"], y=dataframe["y"]):
        fig.grdimage(grid=grid)
    return fig


@pytest.mark.parametrize("array_func", [np.array, xr.Dataset])
@pytest.mark.mpl_image_compare(filename="test_clip.png")
def test_clip_matrix(array_func, dataframe, grid, region, projection):
    """
    Test clip with matrix input for the clip path.
    """
    table = array_func(dataframe)
    fig = Figure()
    fig.basemap(region=region, frame=True, projection=projection)
    with fig.clip(data=table):
        fig.grdimage(grid=grid, region=region)
    return fig


@pytest.mark.mpl_image_compare(filename="test_clip.png")
def test_clip_dataframe(grid, dataframe, region, projection):
    """
    Test clip with dataframe input for the clip path.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True, projection=projection)
    with fig.clip(data=dataframe):
        fig.grdimage(grid=grid, region=region)
    return fig
