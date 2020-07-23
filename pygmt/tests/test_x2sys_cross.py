"""
Tests for x2sys_cross
"""
import os
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
import xarray as xr

from .. import which, x2sys_cross, x2sys_init
from ..datasets import load_sample_bathymetry
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind


@pytest.fixture
def mock_x2sys_home(monkeypatch):
    monkeypatch.setenv("X2SYS_HOME", os.getcwd())


def test_x2sys_cross_input_file(mock_x2sys_home):
    """
    Run x2sys_cross by passing in a filename
    """
    fname = which("@tut_ship.xyz", download="a")
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)
        output = x2sys_cross(tracks=[fname], tag=tag, coe="i")

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (14294, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "i_1", "i_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]

    return output
