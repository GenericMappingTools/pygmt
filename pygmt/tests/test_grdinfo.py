"""
Tests for grdinfo.
"""
import numpy as np
import pytest
from pygmt import grdinfo
from pygmt.datasets import load_earth_relief
from pygmt.exceptions import GMTInvalidInput


def test_grdinfo():
    """
    Make sure grdinfo works as expected.
    """
    grid = load_earth_relief(registration="gridline")
    result = grdinfo(grid=grid, force_scan=0, per_column="n")
    assert result.strip() == "-180 180 -90 90 -8592.5 5559 1 1 361 181 0 1"


def test_grdinfo_file():
    """
    Test grdinfo with file input.
    """
    result = grdinfo(grid="@earth_relief_01d", force_scan=0, per_column="n")
    assert result.strip() == "-180 180 -90 90 -8182 5651.5 1 1 360 180 1 1"


def test_grdinfo_fails():
    """
    Check that grdinfo fails correctly.
    """
    with pytest.raises(GMTInvalidInput):
        grdinfo(np.arange(10).reshape((5, 2)))


def test_grdinfo_region():
    """
    Check that the region argument works in grdinfo.
    """
    result = grdinfo(
        grid="@earth_relief_01d",
        force_scan=0,
        per_column="n",
        region=[-170, 170, -80, 80],
    )
    assert result.strip() == "-170 170 -80 80 -8182 5651.5 1 1 340 160 1 1"
