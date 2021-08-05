"""
Tests for xyz2grd.
"""
import pytest
import xarray as xr
from pygmt import xyz2grd
from pygmt.datasets import load_sample_bathymetry
import numpy as np


@pytest.fixture(scope="module", name="ship_data")
def fixture_ship_data():
    """
    Load the data from the sample bathymetry dataset.
    """
    return load_sample_bathymetry()


def test_xyz2grd_input_file():
    """
    Run xyz2grd by passing in a filename.
    """
    output = xyz2grd(table="@tut_ship.xyz", spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output

def test_xyz2grd_input_array(ship_data):
    """
    Run xyz2grd by passing in a numpy array.
    """
    output = xyz2grd(table=np.array(ship_data), spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output

def test_xyz2grd_input_df(ship_data):
    """
    Run xyz2grd by passing in a data frame.
    """
    output = xyz2grd(table=ship_data, spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output