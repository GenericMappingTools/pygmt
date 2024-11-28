"""
Test pygmt.grdvolume.
"""

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import grdvolume
from pygmt.helpers.testing import load_static_earth_relief


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_static_earth_relief()


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the expected grdvolume data result as a numpy array.
    """
    data = np.array(
        [
            [2.00000000e02, 2.30079975e10, 3.92142453e12, 1.70437454e02],
            [2.50000000e02, 2.30079975e10, 2.77102465e12, 1.20437454e02],
            [3.00000000e02, 2.30079975e10, 1.62062477e12, 7.04374542e01],
            [3.50000000e02, 1.76916116e10, 4.53991397e11, 2.56613930e01],
            [4.00000000e02, 2.81602292e09, 2.34764859e10, 8.33675242e00],
        ]
    )
    return data


@pytest.mark.benchmark
def test_grdvolume(grid, data):
    """
    Test the basic functionality of grdvolume.
    """
    test_output = grdvolume(
        grid=grid,
        contour=[200, 400, 50],
        region=[-53, -50, -22, -20],
    )
    assert isinstance(test_output, pd.DataFrame)
    npt.assert_allclose(test_output, data)
