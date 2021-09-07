"""
Tests for sphdistance.
"""
import os

import numpy as np
import numpy.testing as npt
import pytest
from pygmt import sphdistance
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="array")
def fixture_table():
    """
    Load the table data.
    """
    coords_list = [[85.5, 22.3], [82.3, 22.6], [85.8, 22.4], [86.5, 23.3]]
    return np.array(coords_list)


def test_sphdistance_outgrid(array):
    """
    Test sphdistance with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = sphdistance(
            table=array, outgrid=tmpfile.name, increment=1, region=[82, 87, 22, 24]
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_sphdistance_no_outgrid(array):
    """
    Test sphdistance with no set outgrid.
    """
    temp_grid = sphdistance(table=array, increment=[1, 2], region=[82, 87, 22, 24])
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 0  # Gridline registration
    npt.assert_allclose(temp_grid.max(), 232977.546875)
    npt.assert_allclose(temp_grid.min(), 0)
    npt.assert_allclose(temp_grid.median(), 0)
    npt.assert_allclose(temp_grid.mean(), 62469.17)


def test_sphdistance_fails(array):
    """
    Check that sphdistance fails correctly when neither increment nor region is
    given.
    """
    with pytest.raises(GMTInvalidInput):
        sphdistance(table=array)
