"""
Tests for grdlandmask.
"""
import os

import pytest
from pygmt import grdinfo, grdlandmask
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


def test_grdlandmask_outgrid():
    """
    Creates a grid land mask with an outgrid argument.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = grdlandmask(outgrid=tmpfile.name, spacing=1, region=[-5, 5, -5, 5])
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists
        result = (
            grdinfo(grid=tmpfile.name, force_scan=0, per_column="n").strip().split()
        )
    assert result == ["-5", "5", "-5", "5", "0", "1", "1", "1", "11", "11", "0", "1"]


def test_grdlandmask_no_outgrid():
    """
    Test grdlandmask with no set outgrid.
    """
    temp_grid = grdlandmask(spacing=1, region=[-5, 5, -5, 5])
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 0  # Pixel registration
    assert temp_grid.min() == 0
    assert temp_grid.max() == 1


def test_grdlandmask_fails():
    """
    Check that grdlandmask fails correctly when region and spacing are not
    given.
    """
    with pytest.raises(GMTInvalidInput):
        grdlandmask()
