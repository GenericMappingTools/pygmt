"""
Tests for sph2grd.
"""
import os

import numpy.testing as npt
from pygmt import grdinfo, sph2grd
from pygmt.helpers import GMTTempFile


def test_sph2grd_outgrid():
    """
    Test sph2grd with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = sph2grd(
            table="@EGM96_to_36.txt", outgrid=tmpfile.name, increment=1, region="g"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outgrid exists


def test_sph2grd_no_outgrid():
    """
    Test sph2grd with no set outgrid.
    """
    temp_grid = sph2grd(table="@EGM96_to_36.txt", increment=1, region="g")
    assert temp_grid.dims == ("y", "x")
    assert temp_grid.gmt.gtype == 0  # Cartesian grid
    assert temp_grid.gmt.registration == 0  # Gridline registration
    npt.assert_allclose(temp_grid.max(), 0.00021961)
    npt.assert_allclose(temp_grid.min(), -0.0004326)
    npt.assert_allclose(temp_grid.median(), -0.00010894)
    npt.assert_allclose(temp_grid.mean(), -0.00010968)
