"""
Tests for fitcircle.
"""

import os

import numpy as np
import pandas as pd
import pytest
from pygmt import fitcircle
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.src import which


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the sample data from the sat_03 remote file.
    """
    fname = which("@sat_03.txt", download="c")
    data = pd.read_csv(
        fname,
        header=None,
        skiprows=1,
        sep="\t",
        names=["longitutde", "latitude", "z"],
    )
    return data


def test_fitcircle_no_outfile(data):
    """
    Test fitcircle with no set outfile.
    """
    result = fitcircle(data=data, normalize=True)
    assert result.shape == (7, 3)


def test_fitcircle_file_output(data):
    """
    Test that fitcircle returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = fitcircle(
            data=data, normalize=True, outfile=tmpfile.name, output_type="file"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists
