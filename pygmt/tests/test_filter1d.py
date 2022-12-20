"""
Tests for filter1d.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pygmt import filter1d
from pygmt.datasets import load_sample_data
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the @MaunaLoa_CO2.txt dataset as a pandas dataframe.
    """
    return load_sample_data(name="maunaloa_co2")


def test_filter1d_no_outfile(data):
    """
    Test filter1d with no set outgrid.
    """
    result = filter1d(data=data, filter_type="g5")
    assert result.shape == (670, 2)


def test_filter1d_file_output(data):
    """
    Test that filter1d returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = filter1d(
            data=data, filter_type="g5", outfile=tmpfile.name, output_type="file"
        )
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists


def test_filter1d_invalid_format(data):
    """
    Test that filter1d fails with an incorrect format for output_type.
    """
    with pytest.raises(GMTInvalidInput):
        filter1d(data=data, filter_type="g5", output_type="a")


def test_filter1d_no_filter(data):
    """
    Test that filter1d fails with an argument is missing for filter.
    """
    with pytest.raises(GMTInvalidInput):
        filter1d(data=data)


def test_filter1d_no_outfile_specified(data):
    """
    Test that filter1d fails when outpput_type is set to 'file' but no output
    file name is specified.
    """
    with pytest.raises(GMTInvalidInput):
        filter1d(data=data, filter_type="g5", output_type="file")


def test_filter1d_outfile_incorrect_output_type(data):
    """
    Test that filter1d raises a warning when an outfile filename is set but the
    output_type is not set to 'file'.
    """
    with pytest.warns(RuntimeWarning):
        with GMTTempFile(suffix=".txt") as tmpfile:
            result = filter1d(
                data=data, filter_type="g5", outfile=tmpfile.name, output_type="numpy"
            )
            assert result is None  # return value is None
            assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists


def test_filter1d_format(data):
    """
    Test that correct formats are returned.
    """
    time_series_default = filter1d(data=data, filter_type="g5")
    assert isinstance(time_series_default, pd.DataFrame)
    time_series_array = filter1d(data=data, filter_type="g5", output_type="numpy")
    assert isinstance(time_series_array, np.ndarray)
    time_series_df = filter1d(data=data, filter_type="g5", output_type="pandas")
    assert isinstance(time_series_df, pd.DataFrame)
