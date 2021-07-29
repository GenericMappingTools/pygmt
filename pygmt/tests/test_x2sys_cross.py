# pylint: disable=unused-argument
"""
Tests for x2sys_cross.
"""
import os
from tempfile import TemporaryDirectory

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import x2sys_cross, x2sys_init
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import data_kind


@pytest.fixture(name="mock_x2sys_home")
def fixture_mock_x2sys_home(monkeypatch):
    """
    Set the X2SYS_HOME environment variable to the current working directory
    for the test session.
    """
    monkeypatch.setenv("X2SYS_HOME", os.getcwd())


@pytest.fixture(scope="module", name="tracks")
def fixture_tracks():
    """
    Load track data from the sample bathymetry file.
    """
    dataframe = load_sample_bathymetry()
    dataframe.columns = ["x", "y", "z"]  # longitude, latitude, bathymetry
    return [dataframe.query(expr="z > -20")]  # reduce size of dataset


def test_x2sys_cross_input_file_output_file(mock_x2sys_home):
    """
    Run x2sys_cross by passing in a filename, and output internal crossovers to
    an ASCII txt file.
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
    a pandas.DataFrame.
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
    Run x2sys_cross by passing in one dataframe, and output internal crossovers
    to a pandas.DataFrame.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)

        output = x2sys_cross(tracks=tracks, tag=tag, coe="i", verbose="i")

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (14, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "i_1", "i_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]
        assert output.dtypes["i_1"].type == np.object_
        assert output.dtypes["i_2"].type == np.object_

    return output


def test_x2sys_cross_input_two_dataframes(mock_x2sys_home):
    """
    Run x2sys_cross by passing in two pandas.DataFrame tables with a time
    column, and output external crossovers to a pandas.DataFrame.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(
            tag=tag, fmtfile="xyz", suffix="xyzt", units=["de", "se"], force=True
        )

        # Add a time row to the x2sys fmtfile
        with open(file=os.path.join(tmpdir, "xyz.fmt"), mode="a") as fmtfile:
            fmtfile.write("time\ta\tN\t0\t1\t0\t%g\n")

        # Create pandas.DataFrame track tables
        tracks = []
        for i in range(2):
            np.random.seed(seed=i)
            track = pd.DataFrame(data=np.random.rand(10, 3), columns=("x", "y", "z"))
            track["time"] = pd.date_range(start=f"2020-{i}1-01", periods=10, freq="ms")
            tracks.append(track)

        output = x2sys_cross(tracks=tracks, tag=tag, coe="e", verbose="i")

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (30, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "t_1", "t_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]
        assert output.dtypes["t_1"].type == np.datetime64
        assert output.dtypes["t_2"].type == np.datetime64


def test_x2sys_cross_input_dataframe_with_nan(mock_x2sys_home, tracks):
    """
    Run x2sys_cross by passing in one dataframe with NaN values, and output
    internal crossovers to a pandas.DataFrame.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(
            tag=tag, fmtfile="xyz", suffix="xyzt", units=["de", "se"], force=True
        )

        tracks[0].loc[tracks[0]["z"] < -15, "z"] = np.nan  # set some values to NaN
        output = x2sys_cross(tracks=tracks, tag=tag, coe="i")

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (3, 12)
        columns = list(output.columns)
        assert columns[:6] == ["x", "y", "i_1", "i_2", "dist_1", "dist_2"]
        assert columns[6:] == ["head_1", "head_2", "vel_1", "vel_2", "z_X", "z_M"]
        assert output.dtypes["i_1"].type == np.object_
        assert output.dtypes["i_2"].type == np.object_


def test_x2sys_cross_input_two_filenames(mock_x2sys_home):
    """
    Run x2sys_cross by passing in two filenames, and output external crossovers
    to a pandas.DataFrame.
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
        _ = [os.remove(f"track_{i}.xyz") for i in range(2)]  # cleanup track files

    return output


def test_x2sys_cross_invalid_tracks_input_type(tracks):
    """
    Run x2sys_cross using tracks input that is not a pandas.DataFrame (matrix)
    or str (file) type, which would raise a GMTInvalidInput error.
    """
    invalid_tracks = tracks[0].to_xarray().z
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


def test_x2sys_cross_trackvalues(mock_x2sys_home):
    """
    Test that x2sys_cross's trackvalues (Z) argument work.
    """
    with TemporaryDirectory(prefix="X2SYS", dir=os.getcwd()) as tmpdir:
        tag = os.path.basename(tmpdir)
        x2sys_init(tag=tag, fmtfile="xyz", force=True)
        output = x2sys_cross(tracks=["@tut_ship.xyz"], tag=tag, trackvalues=True)

        assert isinstance(output, pd.DataFrame)
        assert output.shape == (14294, 12)
        # Check mean of track 1 values (z_1) and track 2 values (z_2)
        npt.assert_allclose(output.z_1.mean(), -2420.569767)
        npt.assert_allclose(output.z_2.mean(), -2400.357549)
