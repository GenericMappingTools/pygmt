"""
Tests for pygmt.which.
"""
import os

import pytest
from pygmt import which
from pygmt.helpers import unique_name


def test_which():
    """
    Make sure `which` returns file paths for @files correctly without errors.
    """
    for fname in ["tut_quakes.ngdc", "tut_bathy.nc"]:
        cached_file = which(f"@{fname}", download="c")
        assert os.path.exists(cached_file)
        assert os.path.basename(cached_file) == fname


def test_which_multiple():
    """
    Make sure `which` returns file paths for multiple @files correctly.
    """
    filenames = ["ridge.txt", "tut_ship.xyz"]
    cached_files = which(fname=[f"@{fname}" for fname in filenames], download="c")
    for cached_file in cached_files:
        assert os.path.exists(cached_file)
        assert os.path.basename(cached_file) in filenames


def test_which_fails():
    """
    Make sure `which` will fail with a FileNotFoundError.
    """
    bogus_file = unique_name()
    with pytest.raises(FileNotFoundError):
        which(bogus_file)
    with pytest.raises(FileNotFoundError):
        which(fname=[f"{bogus_file}.nc", f"{bogus_file}.txt"])
