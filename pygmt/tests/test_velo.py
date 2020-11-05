"""
Tests velo.
"""
import pandas as pd
import pytest

from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_velo_pandas_dataframe():
    """
    Plot velocity vectors, crosses, and wedges from a pandas.DataFrame
    """
    fig = Figure()
    df = pd.DataFrame(
        data={
            "Long.": [0, -8, 0, -5, 5, 0],
            "Lat.": [-8, 5, 0, -5, 0, -5],
            "Evel": [0, 3, 4, 6, -6, 6],
            "Nvel": [0, 3, 6, 4, 4, -4],
            "Esig": [4, 0, 4, 6, 6, 6],
            "Nsig": [6, 0, 6, 4, 4, 4],
            "CorEN": [0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
            # "SITE": ["4x6", "3x3", "NaN", "6x4", "-6x4", "6x-4"],
        }
    )
    fig.velo(
        data=df.to_numpy(),
        region=[-10, 10, -10, 10],
        pen="0.25p,red",
        facecolor="green",
        line=True,
        scaling="e0.2/0.39/18",
        frame="1g1",
        projection="x0.4/0.4",
        vector="0.3p",
        verbose=True,
    )
    return fig
