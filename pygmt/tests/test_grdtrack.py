"""
Tests for grdtrack.
"""
import os

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import grdtrack
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind
from pygmt.helpers.testing import load_static_earth_relief

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "track.txt")


@pytest.fixture(scope="module", name="dataarray")
def fixture_dataarray():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="expected_array")
def fixture_numpy_array():
    """
    Load a numpy array with x, y, and bathymetry data.
    """
    array = [
        [-51.613, -17.93, 796.59434514],
        [-48.917, -22.434, 566.49184359],
        [-50.444, -16.358, 571.1492788],
        [-50.721, -16.628, 578.76116859],
        [-51.394, -12.196, 274.43205501],
        [-50.207, -18.404, 532.11444935],
        [-52.56, -16.977, 670.16934401],
        [-51.866, -19.794, 426.77300768],
        [-48.001, -14.144, 741.35824074],
        [-54.438, -19.193, 490.02716679],
    ]
    return array


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load a pandas DataFrame with points.
    """
    return pd.read_csv(
        POINTS_DATA, sep=r"\s+", header=None, names=["longitude", "latitude"]
    )


def test_grdtrack_input_dataframe_and_dataarray(dataarray, dataframe, expected_array):
    """
    Run grdtrack by passing in a pandas.DataFrame and xarray.DataArray as
    inputs.
    """
    output = grdtrack(points=dataframe, grid=dataarray, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(np.array(output), expected_array)


def test_grdtrack_input_csvfile_and_dataarray(dataarray, expected_array):
    """
    Run grdtrack by passing in a csvfile and xarray.DataArray as inputs.
    """
    with GMTTempFile() as tmpfile:
        output = grdtrack(points=POINTS_DATA, grid=dataarray, outfile=tmpfile.name)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists at path
        output = np.loadtxt(tmpfile.name)
        npt.assert_allclose(np.array(output), expected_array)


def test_grdtrack_input_dataframe_and_ncfile(dataframe, expected_array):
    """
    Run grdtrack by passing in a pandas.DataFrame and netcdf file as inputs.
    """
    output = grdtrack(
        points=dataframe, grid="@static_earth_relief.nc", newcolname="bathymetry"
    )
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(np.array(output), expected_array)


def test_grdtrack_input_csvfile_and_ncfile_to_dataframe(expected_array):
    """
    Run grdtrack by passing in a csv file and netcdf file as inputs with a
    pandas.DataFrame output.
    """
    output = grdtrack(points=POINTS_DATA, grid="@static_earth_relief.nc")
    assert isinstance(output, pd.DataFrame)
    npt.assert_allclose(np.array(output), expected_array)


def test_grdtrack_wrong_kind_of_points_input(dataarray, dataframe):
    """
    Run grdtrack using points input that is not a pandas.DataFrame (matrix) or
    file.
    """
    invalid_points = dataframe.longitude.to_xarray()

    assert data_kind(invalid_points) == "grid"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=invalid_points, grid=dataarray, newcolname="bathymetry")


def test_grdtrack_wrong_kind_of_grid_input(dataarray, dataframe):
    """
    Run grdtrack using grid input that is not as xarray.DataArray (grid) or
    file.
    """
    invalid_grid = dataarray.to_dataset()

    assert data_kind(invalid_grid) == "matrix"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=invalid_grid, newcolname="bathymetry")


def test_grdtrack_without_newcolname_setting(dataarray, dataframe):
    """
    Run grdtrack by not passing in newcolname parameter setting.
    """
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=dataarray)


def test_grdtrack_without_outfile_setting(dataarray, dataframe):
    """
    Run grdtrack by not passing in outfile parameter setting.
    """
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=dataarray)
