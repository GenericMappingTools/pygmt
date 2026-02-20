"""
Tests for fitcircle.
"""

import os

import numpy as np
import numpy.testing as npt
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
    result = fitcircle(data=data, norm=True)
    assert result.shape == (7, 3)
    # Test longitude results
    npt.assert_allclose(result.longitude.min(), 52.7434273422)
    npt.assert_allclose(result.longitude.max(), 330.243649573)
    npt.assert_allclose(result.longitude.mean(), 223.078116476)
    npt.assert_allclose(result.longitude.median(), 232.7449849)
    # Test latitude results
    npt.assert_allclose(result.latitude.min(), -21.2085369093)
    npt.assert_allclose(result.latitude.max(), 21.2085369093)
    npt.assert_allclose(result.latitude.mean(), -7.8863683297)
    npt.assert_allclose(result.latitude.median(), -18.406777)


def test_fitcircle_file_output(data):
    """
    Test that fitcircle returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = fitcircle(
            data=data, norm=True, outfile=tmpfile.name, output_type="file"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists


def test_fitcircle_invalid_format(data):
    """
    Test that fitcircle fails with an incorrect format for output_type.
    """
    with pytest.raises(GMTInvalidInput):
        fitcircle(data=data, norm=True, output_type="a")


def test_fitcircle_no_normalize(data):
    """
    Test that fitcircle fails with an argument is missing for normalize.
    """
    with pytest.raises(GMTInvalidInput):
        fitcircle(data=data)


def test_fitcircle_no_outfile_specified(data):
    """
    Test that fitcircle fails when outpput_type is set to 'file' but no output
    file name is specified.
    """
    with pytest.raises(GMTInvalidInput):
        fitcircle(data=data, norm=True, output_type="file")


def test_filter1d_outfile_incorrect_output_type(data):
    """
    Test that filter1d raises a warning when an outfile filename is set but the
    output_type is not set to 'file'.
    """
    with pytest.warns(RuntimeWarning):
        with GMTTempFile(suffix=".txt") as tmpfile:
            result = fitcircle(
                data=data, norm=True, outfile=tmpfile.name, output_type="numpy"
            )
            assert result is None  # return value is None
            assert os.path.exists(path=tmpfile.name)  # check that outfile exists


def test_fitcircle_format(data):
    """
    Test that correct formats are returned.
    """
    circle_default = fitcircle(data=data, norm=True)
    assert isinstance(circle_default, pd.DataFrame)
    circle_array = fitcircle(data=data, norm=True, output_type="numpy")
    assert isinstance(circle_array, np.ndarray)
    circle_df = fitcircle(data=data, norm=True, output_type="pandas")
    assert isinstance(circle_df, pd.DataFrame)
