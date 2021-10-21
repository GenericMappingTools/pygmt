"""
Tests for grdvolume.
"""
import os

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import grdvolume
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_earth_relief(resolution="01d", region=[-100, -95, 34, 39])


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the expected grdvolume data result as a numpy array.
    """
    data = np.array(
        [
            [
                2.00000000e02,
                1.59920815e11,
                3.16386172e13,
                1.97839269e02,
            ],
            [
                2.50000000e02,
                1.44365835e11,
                2.38676788e13,
                1.65327751e02,
            ],
            [
                3.00000000e02,
                1.23788259e11,
                1.71278707e13,
                1.38364259e02,
            ],
            [
                3.50000000e02,
                9.79597525e10,
                1.15235913e13,
                1.17635978e02,
            ],
            [
                4.00000000e02,
                7.26646663e10,
                7.22303463e12,
                9.94022955e01,
            ],
        ]
    )
    return data


def test_grdvolume_format(grid):
    """
    Test that correct formats are returned.
    """
    grdvolume_default = grdvolume(grid=grid)
    assert isinstance(grdvolume_default, pd.DataFrame)
    grdvolume_array = grdvolume(grid=grid, output_type="numpy")
    assert isinstance(grdvolume_array, np.ndarray)
    grdvolume_df = grdvolume(grid=grid, output_type="pandas")
    assert isinstance(grdvolume_df, pd.DataFrame)


def test_grdvolume_invalid_format(grid):
    """
    Test that grdvolume fails with incorrect output_type argument.
    """
    with pytest.raises(GMTInvalidInput):
        grdvolume(grid=grid, output_type=1)


def test_grdvolume_no_outfile(grid):
    """
    Test that grdvolume fails when output_type set to 'file' but no outfile is
    specified.
    """
    with pytest.raises(GMTInvalidInput):
        grdvolume(grid=grid, output_type="file")


def test_grdvolume_no_outgrid(grid, data):
    """
    Test the expected output of grdvolume with no output file set.
    """
    test_output = grdvolume(grid=grid, contour=[200, 400, 50], output_type="numpy")
    npt.assert_allclose(test_output, data)


def test_grdvolume_outgrid(grid):
    """
    Test the expected output of grdvolume with an output file set.
    """
    with GMTTempFile(suffix=".csv") as tmpfile:
        result = grdvolume(
            grid=grid, contour=[200, 400, 50], output_type="file", outfile=tmpfile.name
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists
