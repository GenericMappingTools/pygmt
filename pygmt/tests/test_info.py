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
        "{}: N = 20 " "<11.5309/61.7074> " "<-2.9289/7.8648> " "<0.1412/0.9338>\n"
    ).format(POINTS_DATA)
    assert output == expected_output


def test_info_c():
    "Make sure the C option works"
    output = info(fname=POINTS_DATA, C=True)
    assert output == "11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338\n"


def test_info_i():
    "Make sure the I option works"
    output = info(fname=POINTS_DATA, I=0.1)
    assert output == "-R11.5/61.8/-3/7.9\n"


def test_info_c_i():
    "Make sure the C and I options work together"
    output = info(fname=POINTS_DATA, C=True, I=0.1)
    assert output == "11.5 61.8 -3 7.9 0.1412 0.9338\n"


def test_info_t():
    "Make sure the T option works"
    output = info(fname=POINTS_DATA, T=0.1)
    assert output == "-T11.5/61.8/0.1\n"


def test_info_fails():
    "Make sure info raises an exception if not given a file name"
    with pytest.raises(GMTInvalidInput):
        info(fname=21)
    with pytest.raises(GMTInvalidInput):
        info(fname=np.arange(20))
