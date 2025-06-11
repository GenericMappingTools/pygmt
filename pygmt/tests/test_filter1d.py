"""
Test pygmt.filter1d.
"""

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


@pytest.mark.benchmark
def test_filter1d(data):
    """
    Test the basic functionality of filter1d.
    """
    result = filter1d(data=data, filter_type="g5")
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (671, 2)
