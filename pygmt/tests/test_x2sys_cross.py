# pylint: disable=unused-argument
"""
Tests for x2sys_cross
"""
import os
from tempfile import TemporaryDirectory

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest

from .. import x2sys_cross, x2sys_init
from ..datasets import load_sample_bathymetry
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind


@pytest.fixture(name="mock_x2sys_home")
def fixture_mock_x2sys_home(monkeypatch):
    """
    Set the X2SYS_HOME environment variable to the current working directory
    for the test session
    """
    monkeypatch.setenv("X2SYS_HOME", os.getcwd())


@pytest.fixture(scope="module", name="tracks")
def fixture_tracks():
    """
    Load track data from the sample bathymetry file
    """
    df = load_sample_bathymetry()
    return [df.query(expr="bathymetry > -20")]  # reduce size of dataset


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


def test_x2sys_cross_input_dataframe_output_dataframe(mock_x2sys_home, tracks):
    """
    Run x2sys_cross by passing in one dataframe, and output external crossovers
    to a pandas.DataFrame. Not actually implemented yet, wait for
    https://github.com/GenericMappingTools/gmt/issues/3717
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)

        with pytest.raises(NotImplementedError):
            _ = x2sys_cross(tracks=tracks, tag=tag, coe="i", verbose="i")

        # assert isinstance(output, pd.DataFrame)
        # assert output.shape == (4, 12)
        # columns = list(output.columns)
        # assert columns[:6] == ["x", "y", "t_1", "t_2", "dist_1", "dist_2"]
        # assert columns[6:] == ["head_1","head_2","vel_1","vel_2","z_X","z_M"]
        # assert output.dtypes["t_1"].type == np.datetime64
        # assert output.dtypes["t_2"].type == np.datetime64

    # return output


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


def test_x2sys_cross_invalid_tracks_input_type(tracks):
    """
    Run x2sys_cross using tracks input that is not a pandas.DataFrame (matrix)
    or str (file) type, which would raise a GMTInvalidInput error.
    """
    invalid_tracks = tracks[0].to_xarray().bathymetry
    assert data_kind(invalid_tracks) == "grid"
    with pytest.raises(GMTInvalidInput):
        x2sys_cross(tracks=[invalid_tracks])


def test_x2sys_cross_region_interpolation_numpoints(mock_x2sys_home):
    """
    Test that x2sys_cross's region (R), interpolation (l) and numpoints (W)
    arguments work.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)
        output = x2sys_cross(
            tracks=["@tut_ship.xyz"],
            tag=tag,
            coe="i",
            region=[245, 250, 20, 25],
            interpolation="a",  # Akima spline interpolation
            numpoints=5,  # Use up to 5 data points in interpolation
        )

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (3867, 12)
        # Check crossover errors (z_X) and mean value of observables (z_M)
        npt.assert_allclose(output.z_X.mean(), -139.2, rtol=1e-4)
        npt.assert_allclose(output.z_M.mean(), -2890.465813)
