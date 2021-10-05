"""
Tests for xyz2grd.
"""
import os

import numpy as np
import pytest
import xarray as xr
from pygmt import grdinfo, xyz2grd
from pygmt.datasets import load_sample_bathymetry
from pygmt.helpers import GMTTempFile


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
    output = xyz2grd(data="@tut_ship.xyz", spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output


def test_xyz2grd_input_array(ship_data):
    """
    Run xyz2grd by passing in a numpy array.
    """
    output = xyz2grd(data=np.array(ship_data), spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output


def test_xyz2grd_input_df(ship_data):
    """
    Run xyz2grd by passing in a data frame.
    """
    output = xyz2grd(data=ship_data, spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output


def test_xyz2grd_input_array_file_out(ship_data):
    """
    Run xyz2grd by passing in a numpy array and set an outgrid file.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = xyz2grd(
            data=np.array(ship_data),
            spacing=5,
            region=[245, 255, 20, 30],
            outgrid=tmpfile.name,
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)
        result = grdinfo(tmpfile.name, per_column=True).strip()
        assert result == "245 255 20 30 -3651.06079102 -352.379486084 5 5 3 3 0 0"
