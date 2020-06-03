"""
Tests for gmtinfo
"""
import os

import numpy as np
import pytest

from .. import info
from ..exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


def test_info():
    "Make sure info works"
    output = info(fname=POINTS_DATA)
    expected_output = (
        f"{POINTS_DATA}: N = 20 "
        "<11.5309/61.7074> "
        "<-2.9289/7.8648> "
        "<0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_per_column():
    "Make sure the per_column option works"
    output = info(fname=POINTS_DATA, per_column=True)
    assert output == "11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338\n"


def test_info_spacing():
    "Make sure the spacing option works"
    output = info(fname=POINTS_DATA, spacing=0.1)
    assert output == "-R11.5/61.8/-3/7.9\n"


def test_info_per_column_spacing():
    "Make sure the per_column and spacing options work together"
    output = info(fname=POINTS_DATA, per_column=True, spacing=0.1)
    assert output == "11.5 61.8 -3 7.9 0.1412 0.9338\n"


def test_info_nearest_multiple():
    "Make sure the nearest_multiple option works"
    output = info(fname=POINTS_DATA, nearest_multiple=0.1)
    assert output == "-T11.5/61.8/0.1\n"


def test_info_fails():
    "Make sure info raises an exception if not given a file name"
    with pytest.raises(GMTInvalidInput):
        info(fname=21)
    with pytest.raises(GMTInvalidInput):
        info(fname=np.arange(20))
