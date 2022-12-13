"""
Tests for sph2grd.
"""
from pathlib import Path

import numpy.testing as npt
from pygmt import sph2grd
from pygmt.helpers import GMTTempFile


def test_sph2grd_outgrid():
    """
    Test sph2grd with a set outgrid.
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        result = sph2grd(
            data="@EGM96_to_36.txt", outgrid=tmpfile.name, spacing=1, region="g"
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists


def test_sph2grd_no_outgrid():
    """
    Test sph2grd with no set outgrid.
    """
    temp_grid = sph2grd(data="@EGM96_to_36.txt", spacing=1, region="g")
    assert temp_grid.dims == ("y", "x")
    assert temp_grid.gmt.gtype == 0  # Cartesian grid
    assert temp_grid.gmt.registration == 0  # Gridline registration
    npt.assert_allclose(temp_grid.max(), 0.00021961, rtol=1e-4)
    npt.assert_allclose(temp_grid.min(), -0.0004326, rtol=1e-4)
    npt.assert_allclose(temp_grid.median(), -0.00010894, rtol=1e-4)
    npt.assert_allclose(temp_grid.mean(), -0.00010968, rtol=1e-4)
