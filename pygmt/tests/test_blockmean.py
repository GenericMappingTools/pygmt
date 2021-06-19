"""
Tests for blockmean.
"""
import os

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import blockmean
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the grid data from the sample earth_relief file.
    """
    return load_sample_bathymetry()


def test_blockmean_input_dataframe(dataframe):
    """
    Run blockmean by passing in a pandas.DataFrame as input.
    """
    output = blockmean(table=dataframe, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert all(dataframe.columns == output.columns)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.888877, 29.978707, -384.0])


def test_blockmean_input_table_matrix(dataframe):
    """
    Run blockmean using table input that is not a pandas.DataFrame but still a
    matrix.
    """
    table = dataframe.values
    output = blockmean(table=table, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.888877, 29.978707, -384.0])


def test_blockmean_input_xyz(dataframe):
    """
    Run blockmean by passing in x/y/z as input.
    """
    output = blockmean(
        x=dataframe.longitude,
        y=dataframe.latitude,
        z=dataframe.bathymetry,
        spacing="5m",
        region=[245, 255, 20, 30],
    )
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.888877, 29.978707, -384.0])


def test_blockmean_wrong_kind_of_input_table_grid(dataframe):
    """
    Run blockmean using table input that is not a pandas.DataFrame or file but
    a grid.
    """
    invalid_table = dataframe.bathymetry.to_xarray()
    assert data_kind(invalid_table) == "grid"
    with pytest.raises(GMTInvalidInput):
        blockmean(table=invalid_table, spacing="5m", region=[245, 255, 20, 30])


def test_blockmean_input_filename():
    """
    Run blockmean by passing in an ASCII text file as input.
    """
    with GMTTempFile() as tmpfile:
        output = blockmean(
            table="@tut_ship.xyz",
            spacing="5m",
            region=[245, 255, 20, 30],
            outfile=tmpfile.name,
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists at path
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (5849, 3)
        npt.assert_allclose(output.iloc[0], [245.888877, 29.978707, -384.0])


def test_blockmean_without_outfile_setting():
    """
    Run blockmean by not passing in outfile parameter setting.
    """
    output = blockmean(table="@tut_ship.xyz", spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.888877, 29.978707, -384.0])
