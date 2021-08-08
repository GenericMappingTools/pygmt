"""
Tests for sphinterpolate.
"""
import os

import numpy as np
import numpy.testing as npt
from pygmt import grdinfo, sphinterpolate
from pygmt.helpers import GMTTempFile


def test_sphinterpolate_outgrid():
    """
    Test sphinterpolate with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = sphinterpolate(
            table="@mars370d.txt", outgrid=tmpfile.name, increment=1, region="g"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_sphinterpolate_no_outgrid():
    """
    Test sphinterpolate with no set outgrid.
    """
    temp_grid = sphinterpolate(table="@mars370d.txt", increment=1, region="g")
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 0  # Gridline registration
    result = grdinfo(grid=temp_grid, force_scan="a", per_column="n").strip().split()
    assert int(result[0]) == 0  # x minimum
    assert int(result[1]) == 360  # x maximum
    assert int(result[2]) == -90  # y minimum
    assert int(result[3]) == 90  # y maximum
    npt.assert_approx_equal(float(result[4]), -6908.19873047)  # v minimum
    npt.assert_approx_equal(float(result[5]), 14628.1435547)  # v maximum
