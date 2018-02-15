"""
Test basic functionality for loading datasets.
"""
from ..datasets import load_japan_quakes


def test_japan_quakes():
    "Check that the dataset loads without errors"
    data = load_japan_quakes()
    assert data.shape == (115, 7)
    summary = data.describe()
    assert summary.loc['min', 'year'] == 1987
    assert summary.loc['max', 'year'] == 1988
    assert summary.loc['min', 'month'] == 1
    assert summary.loc['max', 'month'] == 12
    assert summary.loc['min', 'day'] == 1
    assert summary.loc['max', 'day'] == 31
