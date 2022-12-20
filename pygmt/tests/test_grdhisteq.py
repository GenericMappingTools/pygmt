"""
Tests for grdhisteq.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import grdhisteq, load_dataarray
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    Load the grid data from the sample earth_relief file.
    """
    return [-52, -48, -22, -18]


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected grdhisteq grid result.
    """
    return xr.DataArray(
        data=[[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1]],
        coords=dict(lon=[-51.5, -50.5, -49.5, -48.5], lat=[-21.5, -20.5, -19.5, -18.5]),
        dims=["lat", "lon"],
    )


@pytest.fixture(scope="module", name="expected_df")
def fixture_expected_df():
    """
    Load the expected grdhisteq table result.
    """
    return pd.DataFrame(
        data=np.array([[345.5, 519.5, 0], [519.5, 726.5, 1]]),
        columns=["start", "stop", "bin_id"],
    ).astype({"start": np.float32, "stop": np.float32, "bin_id": np.uint32})


def test_equalize_grid_outgrid_file(grid, expected_grid, region):
    """
    Test grdhisteq.equalize_grid with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdhisteq.equalize_grid(
            grid=grid, divisions=2, region=region, outgrid=tmpfile.name
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        temp_grid = load_dataarray(tmpfile.name)
        xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_equalize_grid_outgrid(grid, expected_grid, region):
    """
    Test grdhisteq.equalize_grid with ``outgrid=None``.
    """
    temp_grid = grdhisteq.equalize_grid(
        grid=grid, divisions=2, region=region, outgrid=None
    )
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 1  # Pixel registration
    xr.testing.assert_allclose(a=temp_grid, b=expected_grid)


def test_compute_bins_no_outfile(grid, expected_df, region):
    """
    Test grdhisteq.compute_bins with no ``outfile``.
    """
    temp_df = grdhisteq.compute_bins(grid=grid, divisions=2, region=region)
    assert isinstance(temp_df, pd.DataFrame)
    pd.testing.assert_frame_equal(left=temp_df, right=expected_df.set_index("bin_id"))


def test_compute_bins_ndarray_output(grid, expected_df, region):
    """
    Test grdhisteq.compute_bins with "numpy" output type.
    """
    temp_array = grdhisteq.compute_bins(
        grid=grid, divisions=2, region=region, output_type="numpy"
    )
    assert isinstance(temp_array, np.ndarray)
    np.testing.assert_allclose(temp_array, expected_df.to_numpy())


def test_compute_bins_outfile(grid, expected_df, region):
    """
    Test grdhisteq.compute_bins with ``outfile``.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with pytest.warns(RuntimeWarning) as record:
            result = grdhisteq.compute_bins(
                grid=grid,
                divisions=2,
                region=region,
                outfile=tmpfile.name,
            )
            assert len(record) == 1  # check that only one warning was raised
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0
        temp_df = pd.read_csv(
            filepath_or_buffer=tmpfile.name,
            sep="\t",
            header=None,
            names=["start", "stop", "bin_id"],
            dtype={"start": np.float32, "stop": np.float32, "bin_id": np.uint32},
            index_col="bin_id",
        )
        pd.testing.assert_frame_equal(
            left=temp_df, right=expected_df.set_index("bin_id")
        )


def test_compute_bins_invalid_format(grid):
    """
    Test that compute_bins fails with incorrect format.
    """
    with pytest.raises(GMTInvalidInput):
        grdhisteq.compute_bins(grid=grid, output_type=1)
    with pytest.raises(GMTInvalidInput):
        grdhisteq.compute_bins(grid=grid, output_type="pandas", header="o+c")


def test_equalize_grid_invalid_format(grid):
    """
    Test that equalize_grid fails with incorrect format.
    """
    with pytest.raises(GMTInvalidInput):
        grdhisteq.equalize_grid(grid=grid, outgrid=True)
