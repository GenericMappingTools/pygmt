"""
Tests for surface.
"""
from pathlib import Path

import pandas as pd
import pytest
import xarray as xr
from pygmt import surface, which
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load Table 5.11 in Davis: Statistics and Data Analysis in Geology.
    """
    fname = which("@Table_5_11_mean.xyz", download="c")
    return pd.read_csv(
        fname, sep=r"\s+", header=None, names=["x", "y", "z"], skiprows=1
    )


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Define the region.
    """
    return [0, 4, 0, 8]


@pytest.fixture(scope="module", name="spacing")
def fixture_spacing():
    """
    Define the spacing.
    """
    return "1"


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdcut grid result.
    """
    return xr.DataArray(
        data=[
            [962.2361, 909.526, 872.2578, 876.5983, 950.573],
            [944.369, 905.8253, 872.1614, 901.8583, 943.6854],
            [911.0599, 865.305, 845.5058, 855.7317, 867.1638],
            [878.5973, 851.71, 814.6884, 812.1127, 819.9591],
            [842.0522, 815.2896, 788.2292, 777.0031, 785.6345],
            [854.2515, 813.3035, 781, 742.3641, 735.6497],
            [882.972, 818.4636, 773.611, 718.7798, 685.4824],
            [897.4532, 822.9642, 756.4472, 687.594, 626.2299],
            [910.2932, 823.3307, 737.9952, 651.4994, 565.9981],
        ],
        coords=dict(
            y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            x=[0, 1, 2, 3, 4],
        ),
        dims=[
            "y",
            "x",
        ],
    )


def check_values(grid, expected_grid):
    """
    Check the attributes and values of the DataArray returned by surface.
    """
    assert isinstance(grid, xr.DataArray)
    assert grid.gmt.registration == 0  # Gridline registration
    assert grid.gmt.gtype == 0  # Cartesian type
    xr.testing.assert_allclose(a=grid, b=expected_grid)


def test_surface_input_file(region, spacing, expected_grid):
    """
    Run surface by passing in a filename.
    """
    output = surface(
        data="@Table_5_11_mean.xyz",
        spacing=spacing,
        region=region,
        verbose="e",  # Suppress warnings for IEEE 754 rounding
    )
    check_values(output, expected_grid)


def test_surface_input_data_array(data, region, spacing, expected_grid):
    """
    Run surface by passing in a numpy array into data.
    """
    data = data.values  # convert pandas.DataFrame to numpy.ndarray
    output = surface(
        data=data,
        spacing=spacing,
        region=region,
        verbose="e",  # Suppress warnings for IEEE 754 rounding
    )
    check_values(output, expected_grid)


def test_surface_input_xyz(data, region, spacing, expected_grid):
    """
    Run surface by passing in x, y, z numpy.ndarrays individually.
    """
    output = surface(
        x=data.x,
        y=data.y,
        z=data.z,
        spacing=spacing,
        region=region,
        verbose="e",  # Suppress warnings for IEEE 754 rounding
    )
    check_values(output, expected_grid)


def test_surface_wrong_kind_of_input(data, region, spacing):
    """
    Run surface using grid input that is not file/matrix/vectors.
    """
    data = data.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, spacing=spacing, region=region)


def test_surface_with_outgrid_param(data, region, spacing, expected_grid):
    """
    Run surface with the -Goutputfile.nc parameter.
    """
    data = data.values  # convert pandas.DataFrame to numpy.ndarray
    with GMTTempFile(suffix=".nc") as tmpfile:
        output = surface(
            data=data,
            spacing=spacing,
            region=region,
            outgrid=tmpfile.name,
            verbose="e",  # Suppress warnings for IEEE 754 rounding
        )
        assert output is None  # check that output is None since outgrid is set
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        with xr.open_dataarray(tmpfile.name) as grid:
            check_values(grid, expected_grid)
