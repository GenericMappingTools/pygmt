"""
Test pygmt.fitcircle.
"""

from pathlib import Path

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import fitcircle
from pygmt.exceptions import GMTParameterError
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
def test_fitcircle_absolutes(data):
    """
    Test fitcircle with norm="absolutes".
    """
    result = fitcircle(data=data, norm="absolutes")
    assert isinstance(result, dict)
    assert set(result.keys()) == {"flat_mean", "mean", "north_pole", "south_pole"}
    npt.assert_allclose(result["flat_mean"], (330.243649573, -18.3910128205))
    npt.assert_allclose(result["mean"], (330.16313328, -18.4067771888))
    npt.assert_allclose(result["north_pole"], (52.7434273422, 21.2085369093))
    npt.assert_allclose(result["south_pole"], (232.743427342, -21.2085369093))


def test_fitcircle_squares(data):
    """
    Test fitcircle with norm="squares".
    """
    result = fitcircle(data=data, norm="squares")
    assert isinstance(result, dict)
    assert set(result.keys()) == {"flat_mean", "mean", "north_pole", "south_pole"}
    npt.assert_allclose(result["flat_mean"], (330.243649573, -18.3910128205))
    npt.assert_allclose(result["mean"], (330.163207808, -18.4067882988))
    npt.assert_allclose(result["north_pole"], (52.7449849947, 21.2046833116))
    npt.assert_allclose(result["south_pole"], (232.744984995, -21.2046833116))


def test_fitcircle_small_circle(data):
    """
    Test that fitcircle can fit a small circle instead of a great circle, and
    that the returned dict includes the small-circle keys.
    """
    result = fitcircle(data=data, norm="squares", small_circle=True)
    assert isinstance(result, dict)
    assert set(result.keys()) == {
        "flat_mean",
        "mean",
        "north_pole",
        "south_pole",
        "small_circle_pole",
        "small_circle_distance",
    }
    npt.assert_allclose(result["small_circle_distance"], 87.6072781238)


def test_fitcircle_input_xy(data):
    """
    Run fitcircle by passing in x/y as input.
    """
    result = fitcircle(x=data.longitude, y=data.latitude, norm="absolutes")
    assert isinstance(result, dict)
    npt.assert_allclose(result["flat_mean"], (330.243649573, -18.3910128205))


def test_fitcircle_outfile(data):
    """
    Test that fitcircle returns None and writes a file when outfile is set.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = fitcircle(data=data, norm="squares", outfile=tmpfile.name)
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists


def test_fitcircle_no_norm(data):
    """
    Test that fitcircle fails when the required "norm" parameter is missing.
    """
    with pytest.raises(GMTParameterError):
        fitcircle(data=data)
