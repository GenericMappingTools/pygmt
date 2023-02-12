"""
Tests for Figure.timestamp.
"""
import pytest
from pygmt import Figure


@pytest.fixture(scope="module", name="faketime")
def fixture_faketime():
    """
    Fake datetime passed to the "timefmt" parameter so that the timestamp is
    fixed.
    """
    return "1970-01-01T00:00:00"


@pytest.mark.mpl_image_compare
def test_timestamp(faketime):
    """
    Test that the simplest timestamp() call works.
    """
    fig = Figure()
    fig.timestamp(timefmt=faketime)
    return fig
