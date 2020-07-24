# pylint: disable=unused-argument
"""
Tests for x2sys_cross
"""
import os
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import pytest

from .. import x2sys_cross, x2sys_init

# from ..datasets import load_sample_bathymetry
# from ..exceptions import GMTInvalidInput


@pytest.fixture(name="mock_x2sys_home")
def fixture_mock_x2sys_home(monkeypatch):
    """
    Set the X2SYS_HOME environment variable to the current working directory
    for the test session
    """
    monkeypatch.setenv("X2SYS_HOME", os.getcwd())


def test_x2sys_cross_input_file_output_file(mock_x2sys_home):
    """
    Run x2sys_cross by passing in a filename, and output internal crossovers to
    an ASCII txt file
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)
        outfile = os.path.join(tmpdir, "tmp_coe.txt")
        output = x2sys_cross(
            tracks=["@tut_ship.xyz"], tag=tag, coe="i", outfile=outfile, verbose="i"
        )

        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=outfile)  # check that outfile exists at path
        _ = pd.read_csv(outfile, sep="\t", header=2)  # ensure ASCII text file loads ok

    return output


def test_x2sys_cross_input_file_output_dataframe(mock_x2sys_home):
    """
    Run x2sys_cross by passing in a filename, and output internal crossovers to
    a pandas.DataFrame
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)
        output = x2sys_cross(tracks=["@tut_ship.xyz"], tag=tag, coe="i", verbose="i")

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (14294, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "i_1", "i_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]

    return output


def test_x2sys_cross_input_two_filenames(mock_x2sys_home):
    """
    Run x2sys_cross by passing in two filenames, and output external crossovers
    to a pandas.DataFrame
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)

        # Create temporary xyz files
        for i in range(2):
            np.random.seed(seed=i)
            with open(os.path.join(os.getcwd(), f"track_{i}.xyz"), mode="w") as fname:
                np.savetxt(fname=fname, X=np.random.rand(10, 3))

        output = x2sys_cross(
            tracks=["track_0.xyz", "track_1.xyz"], tag=tag, coe="e", verbose="i"
        )

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (24, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "i_1", "i_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]

    return output
