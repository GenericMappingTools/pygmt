"""
Tests for filter1d.
"""

import pandas as pd
import pytest
from pygmt import filter1d
from pygmt.src import which


@pytest.fixture(scope="module", name="table")
def fixture_table():
    """
    Load the grid data from the sample earth_relief file.
    """
    fname = which("@MaunaLoa_CO2.txt", download="c")
    data = pd.read_csv(
        fname, header=None, skiprows=1, sep="\s+", names=["date", "co2_ppm"]
    )
    return data

def test_filter1d_no_outfile(table):
    """
    Test the azimuth and direction parameters for grdgradient with no set
    outgrid.
    """
    result = filter1d(table=table, filter="g5")
    assert result.shape == (670, 2)