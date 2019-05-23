"""
Tests for grdtrack
"""

import pandas as pd
import pytest

from .. import grdtrack
from .. import which
from ..datasets import load_east_pacific_rise_grid, load_ocean_ridge_points
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind


def test_grdtrack_input_dataframe_and_dataarray():
    """
    Run grdtrack by passing in a pandas.DataFrame and xarray.DataArray as inputs
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_east_pacific_rise_grid()

    output = grdtrack(points=dataframe, grid=dataarray, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    assert output.iloc[0].to_list() == [-110.9536, -42.2489, -2950.49576833]

    return output


def test_grdtrack_input_dataframe_and_ncfile():
    """
    Run grdtrack by passing in a pandas.DataFrame and netcdf file as inputs
    """
    dataframe = load_ocean_ridge_points()
    ncfile = which("@spac_33.nc", download="c")

    output = grdtrack(points=dataframe, grid=ncfile, newcolname="bathymetry")
    assert isinstance(output, pd.DataFrame)
    assert output.columns.to_list() == ["longitude", "latitude", "bathymetry"]
    assert output.iloc[0].to_list() == [-110.9536, -42.2489, -2950.49576833]

    return output


def test_grdtrack_wrong_kind_of_points_input():
    """
    Run grdtrack using points input that is not a pandas.DataFrame (matrix)
    """
    dataframe = load_ocean_ridge_points()
    invalid_points = dataframe.longitude.to_xarray()
    dataarray = load_east_pacific_rise_grid()

    assert data_kind(invalid_points) == "grid"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=invalid_points, grid=dataarray, newcolname="bathymetry")


def test_grdtrack_wrong_kind_of_grid_input():
    """
    Run grdtrack using grid input that is not as xarray.DataArray (grid) or file
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_east_pacific_rise_grid()
    invalid_grid = dataarray.to_dataset()

    assert data_kind(invalid_grid) == "matrix"
    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=invalid_grid, newcolname="bathymetry")


def test_grdtrack_without_newcolname_setting():
    """
    Run grdtrack by not passing in newcolname parameter setting
    """
    dataframe = load_ocean_ridge_points()
    dataarray = load_east_pacific_rise_grid()

    with pytest.raises(GMTInvalidInput):
        grdtrack(points=dataframe, grid=dataarray)
