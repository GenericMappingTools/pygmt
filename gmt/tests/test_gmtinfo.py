"""
Tests for gmtinfo
"""
import os

from .. import info

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_gmtinfo():
    "Test gmtinfo"
    data_fname = os.path.join(TEST_DATA_DIR, 'points.txt')
    output = info(fname=data_fname, C=True)
    assert output == '11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338\n'
