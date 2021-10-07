"""
Tests for project.
"""

import numpy.testing as npt
import pandas as pd
import pytest
from pygmt import project


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Create a DataFrame for the surface tests.
    """
    return pd.DataFrame(data={"x": [0], "y": [0]})


def test_surface_input_dataframe(dataframe):
    """
    Run surface by passing in a pandas.DataFrame as input.
    """
    output = project(points=dataframe, center=[0, -1], azimuth=45, flatearth=True)
    assert isinstance(output, pd.DataFrame)
    assert all(output.columns == ["x", "y", "p", "q", "r", "s"])
    assert output.shape == (1, 6)
    npt.assert_allclose(
        output.iloc[0],
        [0.000000, 0.000000, 0.707107, 0.707107, 0.500000, -0.500000],
        rtol=1e-5,
    )
