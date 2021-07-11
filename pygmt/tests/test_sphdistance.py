"""
Tests for sphdistance.
"""
import os

import numpy as np
import pytest
from pygmt import grdinfo, sphdistance
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
    result = grdinfo(grid=temp_grid, force_scan="a", per_column="n").strip().split()
    assert int(result[0]) == 82  # x minimum
    assert int(result[1]) == 87  # x maximum
    assert int(result[2]) == 22  # y minimum
    assert int(result[3]) == 24  # y maximum
    assert int(result[6]) == 1  # x increment
    assert int(result[7]) == 2  # y increment


def test_sphdistance_fails(array):
    """
    Check that sphdistance fails correctly when neither increment nor region is
    given.
    """
    with pytest.raises(GMTInvalidInput):
        sphdistance(table=array)
