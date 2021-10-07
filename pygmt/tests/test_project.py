"""
Tests for project.
"""
import os

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
import xarray as xr
from pygmt import project
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Create a DataFrame for the project tests.
    """
    return pd.DataFrame(data={"x": [0], "y": [0]})


def test_project_generate():
    """
    Run project by passing in a pandas.DataFrame as input.
    """
    output = project(center=[0, -1], endpoint=[0, 1], flat_earth=True, generate=0.5)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5, 3)
    npt.assert_allclose(output.iloc[1], [3.061617e-17, -0.5, 0.5])


def test_project_input_dataframe(dataframe):
    """
    Run project by passing in a pandas.DataFrame as input.
    """
    output = project(data=dataframe, center=[0, -1], azimuth=45, flat_earth=True)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (1, 6)
    npt.assert_allclose(
        output.iloc[0],
        [0.000000, 0.000000, 0.707107, 0.707107, 0.500000, -0.500000],
        rtol=1e-5,
    )


@pytest.mark.parametrize("array_func", [np.array, xr.Dataset])
def test_project_input_matrix(array_func, dataframe):
    """
    Run project by passing in a matrix as input.
    """
    table = array_func(dataframe)
    output = project(data=table, center=[0, -1], azimuth=45, flat_earth=True)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (1, 6)
    npt.assert_allclose(
        output.iloc[0],
        [0.000000, 0.000000, 0.707107, 0.707107, 0.500000, -0.500000],
        rtol=1e-5,
    )


def test_project_output_filename(dataframe):
    """
    Run project by passing in an ASCII text file as input.
    """
    with GMTTempFile() as tmpfile:
        output = project(
            data=dataframe,
            center=[0, -1],
            azimuth=45,
            flat_earth=True,
            outfile=tmpfile.name,
        )
        assert output is None  # check that output is None since outfile is set
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists at path
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (1, 6)
        npt.assert_allclose(
            output.iloc[0],
            [0.000000, 0.000000, 0.707107, 0.707107, 0.500000, -0.500000],
            rtol=1e-5,
        )


def test_project_no_data():
    """
    Run project without providing `data` or `generate`.
    """
    with pytest.raises(GMTInvalidInput):
        project(center=[0, -1], azimuth=45, flat_earth=True)
