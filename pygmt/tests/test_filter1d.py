"""
Test pygmt.filter1d.
"""

import numpy as np
import pandas as pd
import pytest
from pygmt import filter1d
from pygmt.datasets import load_sample_data


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the @MaunaLoa_CO2.txt dataset as a pandas dataframe.
    """
    return load_sample_data(name="maunaloa_co2")


def test_filter1d_no_outfile(data):
    """
    Test filter1d with no set outfile.
    """
    result = filter1d(data=data, filter_type="g5")
    assert result.shape == (671, 2)


@pytest.mark.benchmark
def test_filter1d_format(data):
    """
    Test that correct formats are returned.
    """
    time_series_default = filter1d(data=data, filter_type="g5")
    assert isinstance(time_series_default, pd.DataFrame)
    assert time_series_default.shape == (671, 2)
    time_series_array = filter1d(data=data, filter_type="g5", output_type="numpy")
    assert isinstance(time_series_array, np.ndarray)
    assert time_series_array.shape == (671, 2)
    time_series_df = filter1d(data=data, filter_type="g5", output_type="pandas")
    assert isinstance(time_series_df, pd.DataFrame)
    assert time_series_df.shape == (671, 2)
