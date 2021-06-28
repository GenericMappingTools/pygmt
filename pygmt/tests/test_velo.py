"""
Tests velo.
"""
import pandas as pd
import pytest
from packaging.version import Version
from pygmt import Figure, clib
from pygmt.exceptions import GMTInvalidInput

with clib.Session() as _lib:
    gmt_version = Version(_lib.info["version"])


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Sample pandas.DataFrame for plotting velocity vectors.
    """
    return pd.DataFrame(
        data={
            "Long.": [0, -8, 0, -5, 5, 0],
            "Lat.": [-8, 5, 0, -5, 0, -5],
            "Evel": [0, 3, 4, 6, -6, 6],
            "Nvel": [0, 3, 6, 4, 4, -4],
            "Esig": [4, 0, 4, 6, 6, 6],
            "Nsig": [6, 0, 6, 4, 4, 4],
            "CorEN": [0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
            "SITE": ["4x6", "3x3", "NaN", "6x4", "-6x4", "6x-4"],
        }
    )


@pytest.mark.xfail(
    condition=gmt_version > Version("6.2.0"),
    reason="Upstream bug fixed by https://github.com/GenericMappingTools/gmt/pull/5360.",
)
@pytest.mark.mpl_image_compare
def test_velo_numpy_array_numeric_only(dataframe):
    """
    Plot velocity arrow and confidence ellipse from a numpy.ndarray.
    """
    fig = Figure()
    fig.velo(
        data=dataframe.iloc[:, :-1].to_numpy(),
        spec="e0.2/0.39/18",
        vector="0.3c+p1p+e+gred",
        frame="1g1",
    )
    return fig


def test_velo_numpy_array_text_column(dataframe):
    """
    Check that velo fails when plotting a numpy.ndarray with a text column.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.velo(
            data=dataframe.to_numpy(),
            spec="e0.2/0.39/18",
            vector="0.3c+p1p+e+gred",
        )


def test_velo_without_spec(dataframe):
    """
    Check that velo fails when the spec parameter is not given.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.velo(data=dataframe)


@pytest.mark.xfail(
    condition=gmt_version > Version("6.2.0"),
    reason="Upstream bug fixed by https://github.com/GenericMappingTools/gmt/pull/5360.",
)
@pytest.mark.mpl_image_compare
def test_velo_pandas_dataframe(dataframe):
    """
    Plot velocity arrow and confidence ellipse from a pandas.DataFrame.
    """
    fig = Figure()
    fig.velo(
        data=dataframe,
        spec="e0.2/0.39/18",
        vector="0.3c+p1p+e+gred",
        frame=["WSne", "2g2f"],
        region=[-10, 8, -10, 6],
        projection="x0.8c",
        pen="0.6p,red",
        uncertaintycolor="lightblue1",
        line=True,
    )
    return fig
