"""
Tests for pygmt.which.
"""
import os

import pytest
from pygmt import which
from pygmt.helpers import unique_name


def test_which():
    """
    Make sure which returns file paths for @files correctly without errors.
    """
    for fname in ["tut_quakes.ngdc", "tut_bathy.nc"]:
        cached_file = which(f"@{fname}", download="c")
        assert os.path.exists(cached_file)
        assert os.path.basename(cached_file) == fname


def test_which_fails():
    """
    which should fail with a FileNotFoundError.
    """
    bogus_file = unique_name()
    with pytest.raises(FileNotFoundError):
        which(bogus_file)
