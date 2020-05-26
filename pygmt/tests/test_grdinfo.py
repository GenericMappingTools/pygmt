"""
Tests for grdinfo
"""
import numpy as np
import pytest

from .. import grdinfo
from ..datasets import load_earth_relief
from ..exceptions import GMTInvalidInput


def test_grdinfo():
    "Make sure grd info works as expected"
    grid = load_earth_relief()
    result = grdinfo(grid, L=0, C="n")
    assert result.strip() == "-180 180 -90 90 -8592.14453125 5558.79248047 1 1 361 181"


def test_grdinfo_file():
    "Test grdinfo with file input"
    result = grdinfo("@earth_relief_60m", L=0, C="n")
    assert result.strip() == "-180 180 -90 90 -8592.14465255 5558.79248047 1 1 361 181"


def test_grdinfo_fails():
    "Check that grdinfo fails correctly"
    with pytest.raises(GMTInvalidInput):
        grdinfo(np.arange(10).reshape((5, 2)))
