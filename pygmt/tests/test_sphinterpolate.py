"""
Tests for sphinterpolate.
"""
import os

import numpy.testing as npt
from pygmt import sphinterpolate
from pygmt.helpers import GMTTempFile


def test_sphinterpolate_outgrid():
    """
    Test sphinterpolate with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = sphinterpolate(
            table="@mars370d.txt", outgrid=tmpfile.name, spacing=1, region="g"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_sphinterpolate_no_outgrid():
    """
    Test sphinterpolate with no set outgrid.
    """
    temp_grid = sphinterpolate(table="@mars370d.txt", spacing=1, region="g")
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype == 1  # Geographic grid
    assert temp_grid.gmt.registration == 0  # Gridline registration
    npt.assert_allclose(temp_grid.max(), 14628.144)
    npt.assert_allclose(temp_grid.min(), -6908.1987)
    npt.assert_allclose(temp_grid.median(), 118.96849)
    npt.assert_allclose(temp_grid.mean(), 272.60593)
