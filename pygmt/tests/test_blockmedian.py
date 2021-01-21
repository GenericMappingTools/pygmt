"""
Tests for blockmedian.
"""
import os

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import blockmedian
from pygmt.datasets import load_sample_bathymetry
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


def test_blockmedian_input_dataframe():
    """
    Run blockmedian by passing in a pandas.DataFrame as input.
    """
    dataframe = load_sample_bathymetry()
    output = blockmedian(table=dataframe, spacing="5m", region=[245, 255, 20, 30])
    assert isinstance(output, pd.DataFrame)
    assert all(dataframe.columns == output.columns)
    assert output.shape == (5849, 3)
    npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])

    return output


def test_blockmedian_wrong_kind_of_input_table_matrix():
    """
    Run blockmedian using table input that is not a pandas.DataFrame but still
    a matrix.
    """
    dataframe = load_sample_bathymetry()
    invalid_table = dataframe.values
    assert data_kind(invalid_table) == "matrix"
    with pytest.raises(GMTInvalidInput):
        blockmedian(table=invalid_table, spacing="5m", region=[245, 255, 20, 30])


def test_blockmedian_wrong_kind_of_input_table_grid():
    """
    Run blockmedian using table input that is not a pandas.DataFrame or file
    but a grid.
    """
    dataframe = load_sample_bathymetry()
    invalid_table = dataframe.bathymetry.to_xarray()
    assert data_kind(invalid_table) == "grid"
    with pytest.raises(GMTInvalidInput):
        blockmedian(table=invalid_table, spacing="5m", region=[245, 255, 20, 30])


def test_blockmedian_input_filename():
    """
    Run blockmedian by passing in an ASCII text file as input.
    """
    with GMTTempFile() as tmpfile:
        output = blockmedian(
            table="@tut_ship.xyz",
            spacing="5m",
            region=[245, 255, 20, 30],
            outfile=tmpfile.name,
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists at path
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (5849, 3)
        npt.assert_allclose(output.iloc[0], [245.88819, 29.97895, -385.0])

    return output


def test_blockmedian_without_outfile_setting():
    """
    Run blockmedian by not passing in outfile parameter setting.
    """
    with pytest.raises(GMTInvalidInput):
        blockmedian(table="@tut_ship.xyz", spacing="5m", region=[245, 255, 20, 30])
