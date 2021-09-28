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
