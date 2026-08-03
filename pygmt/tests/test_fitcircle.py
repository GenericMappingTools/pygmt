"""
Test pygmt.fitcircle.
"""

from pathlib import Path

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import fitcircle
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import GMTTempFile
from pygmt.src import which


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the sample data from the @sat_03 remote file.
    """
    fname = which("@sat_03.txt", download="c")
    return pd.read_csv(
        fname, header=None, skiprows=1, sep="\t", names=["longitude", "latitude", "z"]
    )


@pytest.mark.benchmark
def test_fitcircle_no_outfile(data):
    """
    Test fitcircle with no set outfile.
    """
    result = fitcircle(data=data, norm=2)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (4, 3)
    # Test longitude results
    npt.assert_allclose(result.longitude.min(), 52.7449849947)
    npt.assert_allclose(result.longitude.max(), 330.243649573)
    # Test latitude results
    npt.assert_allclose(result.latitude.min(), -21.2046833116)
    npt.assert_allclose(result.latitude.max(), 21.2046833116)


def test_fitcircle_file_output(data):
    """
    Test that fitcircle returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = fitcircle(
            data=data, norm=True, outfile=tmpfile.name, output_type="file"
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists


def test_fitcircle_invalid_format(data):
    """
    Test that fitcircle fails with an incorrect format for output_type.
    """
    with pytest.raises(GMTValueError):
        fitcircle(data=data, norm=True, output_type="a")


def test_fitcircle_no_norm(data):
    """
    Test that fitcircle fails when the required "norm" parameter is missing.
    """
    with pytest.raises(GMTParameterError):
        fitcircle(data=data)


def test_fitcircle_no_outfile_specified(data):
    """
    Test that fitcircle fails when output_type is set to "file" but no outfile
    is specified.
    """
    with pytest.raises(GMTParameterError):
        fitcircle(data=data, norm=True, output_type="file")


def test_fitcircle_outfile_incorrect_output_type(data):
    """
    Test that fitcircle raises a warning when an outfile filename is set but the
    output_type is not set to "file".
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with pytest.warns(RuntimeWarning) as record:
            result = fitcircle(
                data=data, norm=True, outfile=tmpfile.name, output_type="numpy"
            )
        assert len(record) == 1  # check that only one warning was raised
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists


def test_fitcircle_format(data):
    """
    Test that correct formats are returned.
    """
    circle_default = fitcircle(data=data, norm=2)
    assert isinstance(circle_default, pd.DataFrame)
    circle_array = fitcircle(data=data, norm=2, output_type="numpy")
    assert isinstance(circle_array, np.ndarray)
    circle_df = fitcircle(data=data, norm=2, output_type="pandas")
    assert isinstance(circle_df, pd.DataFrame)


@pytest.mark.parametrize("norm", [True, 3])
def test_fitcircle_pandas_unsupported_for_both_norms(data, norm):
    """
    Test that fitcircle raises an exception when output_type is "pandas" (the
    default) and norm is True or 3, since the L1 and L2 solutions are stacked
    in the same rows and can't be represented as a single pandas.DataFrame.
    """
    with pytest.raises(GMTValueError):
        fitcircle(data=data, norm=norm)
    with pytest.raises(GMTValueError):
        fitcircle(data=data, norm=norm, output_type="pandas")
    result = fitcircle(data=data, norm=norm, output_type="numpy")
    assert isinstance(result, np.ndarray)


def test_fitcircle_small_circle(data):
    """
    Test that fitcircle can fit a small circle instead of a great circle.
    """
    result = fitcircle(data=data, norm=2, small_circle=True)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (5, 3)
    assert "Small Circle Pole" in result.method.iloc[-1]
