"""
Tests for project.
"""
from pathlib import Path

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
    Run project by passing in center and endpoint as input.
    """
    output = project(center=[0, -1], endpoint=[0, 1], flat_earth=True, generate=0.5)
    assert isinstance(output, pd.DataFrame)
    assert output.shape == (5, 3)
    npt.assert_allclose(output.iloc[1], [3.061617e-17, -0.5, 0.5])
    pd.testing.assert_index_equal(
        left=output.columns, right=pd.Index(data=["r", "s", "p"])
    )


@pytest.mark.parametrize("array_func", [np.array, pd.DataFrame, xr.Dataset])
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
    Run project by passing in a pandas.DataFrame, and output to an ASCII txt
    file.
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
        assert Path(tmpfile.name).stat().st_size > 0  # check that outfile exists
        output = pd.read_csv(tmpfile.name, sep="\t", header=None)
        assert output.shape == (1, 6)
        npt.assert_allclose(
            output.iloc[0],
            [0.000000, 0.000000, 0.707107, 0.707107, 0.500000, -0.500000],
            rtol=1e-5,
        )


def test_project_incorrect_parameters():
    """
    Run project by providing incorrect parameters such as 1) no `center`; 2) no
    `data` or `generate`; and 3) `generate` with `convention`.
    """
    with pytest.raises(GMTInvalidInput):
        # No `center`
        project(azimuth=45)
    with pytest.raises(GMTInvalidInput):
        # No `data` or `generate`
        project(center=[0, -1], azimuth=45, flat_earth=True)
    with pytest.raises(GMTInvalidInput):
        # Using `generate` with `convention`
        project(center=[0, -1], generate=0.5, convention="xypqrsz")
