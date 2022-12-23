"""
Tests for grdtrack.
"""
import os
from pathlib import Path

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
def fixture_expected_array():
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
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
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


def test_grdtrack_profile(dataarray):
    """
    Run grdtrack by passing a profile.
    """
    output = grdtrack(grid=dataarray, profile="-51/-17/-54/-19")
    assert isinstance(output, pd.DataFrame)
    npt.assert_allclose(
        np.array(output),
        np.array(
            [
                [-51.0, -17.0, 669.671875],
                [-51.42430204, -17.28838525, 847.40745877],
                [-51.85009439, -17.57598444, 885.30534844],
                [-52.27733766, -17.86273467, 829.85423488],
                [-52.70599151, -18.14857333, 776.83702212],
                [-53.13601473, -18.43343819, 631.07867839],
                [-53.56736521, -18.7172675, 504.28037216],
                [-54.0, -19.0, 486.10351562],
            ]
        ),
    )


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


def test_grdtrack_no_points_and_profile(dataarray):
    """
    Run grdtrack but don't set 'points' and 'profile'.
    """
    with pytest.raises(GMTInvalidInput):
        grdtrack(grid=dataarray)


def test_grdtrack_set_points_and_profile(dataarray, dataframe):
    """
    Run grdtrack but set both 'points' and 'profile'.
    """
    with pytest.raises(GMTInvalidInput):
        grdtrack(grid=dataarray, points=dataframe, profile="BL/TR")


def test_grdtrack_old_parameter_order(dataframe, dataarray, expected_array):
    """
    Run grdtrack with the old parameter order 'points, grid'.

    This test should be removed in v0.9.0.
    """
    for points in (POINTS_DATA, dataframe):
        for grid in ("@static_earth_relief.nc", dataarray):
            with pytest.warns(expected_warning=FutureWarning) as record:
                output = grdtrack(points, grid)
                assert len(record) == 1
                assert isinstance(output, pd.DataFrame)
                npt.assert_allclose(np.array(output), expected_array)
