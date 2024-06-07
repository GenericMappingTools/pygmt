"""
Test pygmt.which.
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pygmt import which
from pygmt.helpers import unique_name
from pygmt.session_management import begin, end


def test_which():
    """
    Make sure `which` returns file paths for @files correctly without errors.
    """
    for fname in ["tut_quakes.ngdc", "tut_bathy.nc"]:
        cached_file = which(fname=f"@{fname}", download="c")
        assert Path(cached_file).exists()
        assert Path(cached_file).name == fname


@pytest.mark.benchmark
def test_which_multiple():
    """
    Make sure `which` returns file paths for multiple @files correctly.
    """
    filenames = ["ridge.txt", "tut_ship.xyz"]
    cached_files = which([f"@{fname}" for fname in filenames], download="c")
    for cached_file in cached_files:
        assert Path(cached_file).exists()
        assert Path(cached_file).name in filenames


def test_which_fails():
    """
    Make sure `which` will fail with a FileNotFoundError.
    """
    bogus_file = unique_name()
    with pytest.raises(FileNotFoundError):
        which(bogus_file)
    with pytest.raises(FileNotFoundError):
        which(fname=[f"{bogus_file}.nc", f"{bogus_file}.txt"])


def test_which_nonascii_path(monkeypatch):
    """
    Make sure PyGMT works with paths that contain non-ascii characters (e.g., Chinese).
    """
    # Create a temporary directory with a Chinese suffix as a fake home directory.
    with TemporaryDirectory(suffix="中文") as fakehome:
        (Path(fakehome) / ".gmt").mkdir()  # Create the ~/.gmt directory.
        assert fakehome.endswith("中文")  # Make sure fakename contains Chinese.
        with monkeypatch.context() as mpatch:
            # Set HOME to the fake home directory and GMT will use it.
            mpatch.setenv("HOME", fakehome)
            # Check if HOME is set correctly
            assert os.getenv("HOME") == fakehome
            assert os.environ["HOME"] == fakehome
            # assert str(Path.home().resolve()) == fakehome
            end()

            # GMT should download the remote file under the new home directory.
            fname = which(fname="@static_earth_relief.nc", download="c", verbose="d")
            print(os.environ["HOME"])
            print(fname)
            assert fname.startswith(fakehome)
            assert fname.endswith("static_earth_relief.nc")
            begin()

    # Make sure HOME is reverted correctly.
    assert os.getenv("HOME") != fakehome
    assert os.environ["HOME"] != fakehome
    # assert str(Path.home().resolve()) != fakehome
