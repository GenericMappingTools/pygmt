"""
Tests for triangulate.
"""
import os

import pandas as pd
import pytest
import xarray as xr
from pygmt import triangulate, which
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    fname = which("@Table_5_11_mean.xyz", download="c")
    return pd.read_csv(
        fname, sep=r"\s+", header=None, names=["x", "y", "z"], skiprows=1
    )[:10]


@pytest.fixture(scope="module", name="expected_grid")
def fixture_grid_result():
    """
    Load the expected triangulate grid result.
    """
    return xr.DataArray(
        data=[[779.6264, 752.1539, 749.38776], [771.2882, 726.9792, 722.1368]],
        coords=dict(y=[5, 6], x=[2, 3, 4]),
        dims=["y", "x"],
    )


def test_triangulate_input_file():
    """
    Run triangulate by passing in a filename.
    """
    output = triangulate(data="@Table_5_11_mean.xyz")
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (67, 3)


def test_triangulate_input_data_array(dataframe):
    """
    Run triangulate by passing in a numpy array into data.
    """
    data = dataframe.to_numpy()
    output = triangulate(data=data)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (67, 3)


def test_triangulate_input_xyz(dataframe):
    """
    Run triangulate by passing in x, y, z numpy.ndarrays individually.
    """
    output = triangulate(
        x=dataframe.x,
        y=dataframe.y,
        z=dataframe.z,
    )
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (67, 3)


def test_triangulate_input_xy_no_z(dataframe):
    """
    Run triangulate by passing in x and y, but no z.
    """
    output = triangulate(x=dataframe.x, y=dataframe.y)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (67, 3)


def test_triangulate_wrong_kind_of_input(dataframe):
    """
    Run triangulate using grid input that is not file/matrix/vectors.
    """
    data = dataframe.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        triangulate(data=data)


def test_triangulate_with_outgrid_true(dataframe, expected_grid):
    """
    Run triangulate with outgrid=True and see it load into an xarray.DataArray.
    """
    data = dataframe.to_numpy()
    output = triangulate(data=data, spacing=1, region=[2, 4, 5, 6], outgrid=True)
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    xr.testing.assert_allclose(a=output, b=expected_grid)


def test_triangulate_with_outgrid_param(dataframe, expected_grid):
    """
    Run triangulate with the -Goutputfile.nc parameter.
    """
    data = dataframe.to_numpy()
    with GMTTempFile(suffix=".nc") as tmpfile:
        output = triangulate(
            data=data, spacing=1, region=[2, 4, 5, 6], outgrid=tmpfile.name
        )
        assert output is None  # check that output is None since outgrid is set
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        with xr.open_dataarray(tmpfile.name) as grid:
            assert isinstance(grid, xr.DataArray)
            assert grid.gmt.registration == 0  # Gridline registration
            assert grid.gmt.gtype == 0  # Cartesian type
            xr.testing.assert_allclose(a=grid, b=expected_grid)
