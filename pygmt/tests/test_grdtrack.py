"""
Tests for grdtrack.
"""
import os

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import grdtrack, which
from pygmt.datasets import load_earth_relief, load_ocean_ridge_points
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_TRACK = os.path.join(TEST_DATA_DIR, "tmp_track.txt")


@pytest.fixture(scope="module", name="dataarray")
def fixture_dataarray():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(registration="gridline").sel(
        lat=slice(-49, -42), lon=slice(-118, -107)
    )


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the ocean ridge file.
    """
    return load_ocean_ridge_points()


@pytest.fixture(scope="module", name="csvfile")
def fixture_csvfile():
    """
    Load the csvfile.
    """
    return which("@ridge.txt", download="c")


@pytest.fixture(scope="module", name="ncfile")
def fixture_ncfile():
    """
    Load the ncfile.
    """
    return which("@earth_relief_01d", download="a")


def test_grdtrack_input_dataframe_and_dataarray(dataarray, dataframe):
    """
    Run grdtrack by passing in a pandas.DataFrame and xarray.DataArray as
    inputs.
    """
    output = grdtrack(points=dataframe, grid=dataarray, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(output.iloc[0], [-110.9536, -42.2489, -2790.488422])

    return output


def test_grdtrack_input_csvfile_and_dataarray(dataarray, csvfile):
    """
    Run grdtrack by passing in a csvfile and xarray.DataArray as inputs.
    """
    try:
        output = grdtrack(points=csvfile, grid=dataarray, outfile=TEMP_TRACK)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_TRACK)  # check that outfile exists at path

        track = pd.read_csv(TEMP_TRACK, sep="\t", header=None, comment=">")
        npt.assert_allclose(track.iloc[0], [-110.9536, -42.2489, -2790.488422])
    finally:
        os.remove(path=TEMP_TRACK)

    return output


def test_grdtrack_input_dataframe_and_ncfile(dataframe, ncfile):
    """
    Run grdtrack by passing in a pandas.DataFrame and netcdf file as inputs.
    """

    output = grdtrack(points=dataframe, grid=ncfile, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    npt.assert_allclose(output.iloc[0], [-32.2971, 37.4118, -1939.748245])

    return output


def test_grdtrack_input_csvfile_and_ncfile(csvfile, ncfile):
    """
    Run grdtrack by passing in a csvfile and netcdf file as inputs.
    """
    try:
        output = grdtrack(points=csvfile, grid=ncfile, outfile=TEMP_TRACK)
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=TEMP_TRACK)  # check that outfile exists at path

        track = pd.read_csv(TEMP_TRACK, sep="\t", header=None, comment=">")
        npt.assert_allclose(track.iloc[0], [-32.2971, 37.4118, -1939.748245])
    finally:
        os.remove(path=TEMP_TRACK)

    return output


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


def test_grdtrack_without_outfile_setting(csvfile, ncfile):
    """
    Run grdtrack by not passing in outfile parameter setting.
    """
    output = grdtrack(points=csvfile, grid=ncfile)
    npt.assert_allclose(output.iloc[0], [-32.2971, 37.4118, -1939.748245])

    return output
