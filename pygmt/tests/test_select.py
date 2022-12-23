"""
Tests for select.
"""
from pathlib import Path

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import select
from pygmt.datasets import load_sample_data
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return load_sample_data(name="bathymetry")


def test_select_input_dataframe(dataframe):
    """
    Run select by passing in a pandas.DataFrame as input.
    """
    output = select(data=dataframe, region=[250, 251, 26, 27])
    assert isinstance(output, pd.DataFrame)
    assert all(dataframe.columns == output.columns)
    assert output.shape == (65, 3)
    npt.assert_allclose(output.median(), [250.31464, 26.33893, -270.0])


def test_select_input_table_matrix(dataframe):
    """
    Run select using table input that is not a pandas.DataFrame but still a
    matrix.

    Also testing the reverse (I) alias.
    """
    data = dataframe.values
    output = select(data=data, region=[245.5, 254.5, 20.5, 29.5], reverse="r")
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (9177, 3)
    npt.assert_allclose(output.median(), [247.235, 20.48624, -3241.0])


def test_select_input_filename():
    """
    Run select by passing in an ASCII text file as input.

    Also testing the z_subregion (Z) alias.
    """
    with GMTTempFile() as tmpfile:
        output = select(
            data="@tut_ship.xyz",
            region=[250, 251, 26, 27],
            z_subregion=["-/-630", "-120/0+a"],
            outfile=tmpfile.name,
        )
        assert output is None  # check that output is None since outfile is set
        assert Path(tmpfile.name).stat().st_size > 0
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (5, 3)
        npt.assert_allclose(output.median(), [250.12149, 26.04296, -674.0])
