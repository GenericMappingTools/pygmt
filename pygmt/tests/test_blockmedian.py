"""
Tests for blockmedian.
"""
from pathlib import Path

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import blockmedian
from pygmt.datasets import load_sample_data
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    return load_sample_data(name="bathymetry")


def test_blockmedian_input_dataframe(dataframe):
    """
    Run blockmedian by passing in a pandas.DataFrame as input.
    """
    output = blockmedian(data=dataframe, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert all(dataframe.columns == output.columns)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])


def test_blockmedian_input_table_matrix(dataframe):
    """
    Run blockmedian using table input that is not a pandas.DataFrame but still
    a matrix.
    """
    table = dataframe.values
    output = blockmedian(data=table, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])


def test_blockmedian_input_xyz(dataframe):
    """
    Run blockmedian by passing in x/y/z as input.
    """
    output = blockmedian(
        x=dataframe.longitude,
        y=dataframe.latitude,
        z=dataframe.bathymetry,
        spacing="5m",
        region=[245, 255, 20, 30],
    )
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])


def test_blockmedian_wrong_kind_of_input_table_grid(dataframe):
    """
    Run blockmedian using table input that is not a pandas.DataFrame or file
    but a grid.
    """
    invalid_table = dataframe.bathymetry.to_xarray()
    assert data_kind(invalid_table) == "grid"
    with pytest.raises(GMTInvalidInput):
        blockmedian(data=invalid_table, spacing="5m", region=[245, 255, 20, 30])


def test_blockmedian_input_filename():
    """
    Run blockmedian by passing in an ASCII text file as input.
    """
    with GMTTempFile() as tmpfile:
        output = blockmedian(
            data="@tut_ship.xyz",
            spacing="5m",
            region=[245, 255, 20, 30],
            outfile=tmpfile.name,
        )
        assert output is None  # check that output is None since outfile is set
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (5849, 3)
        npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])


def test_blockmedian_without_outfile_setting():
    """
    Run blockmedian by not passing in outfile parameter setting.
    """
    output = blockmedian(data="@tut_ship.xyz", spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])
