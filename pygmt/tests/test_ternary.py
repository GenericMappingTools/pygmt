"""
Tests ternary.
"""
import numpy as np
import pytest
from pygmt import Figure


@pytest.fixture(scope="module", name="array")
def fixture_table():
    """
    Load the table data.
    """
    ternary_list = [
        [0.51, 0.28, 0.21, 2.732],
        [0.6, 0.2, 0.2, 2.446],
        [0.86, 0.1, 0.04, 2.866],
        [0.99, 0.0, 0.01, 3.708],
        [0.21, 0.52, 0.27, 1.722],
        [0.29, 0.37, 0.34, 1.182],
        [0.2, 0.32, 0.48, 3.612],
        [0.88, 0.0, 0.12, 2.612],
        [0.41, 0.27, 0.32, 3.366],
        [0.61, 0.02, 0.37, 0.608],
        [0.2, 0.72, 0.08, 2.013],
        [0.88, 0.11, 0.01, 1.808],
        [0.08, 0.89, 0.03, 0.231],
        [0.91, 0.06, 0.03, 3.495],
        [0.46, 0.34, 0.2, 1.391],
        [0.49, 0.39, 0.12, 3.312],
        [0.05, 0.53, 0.42, 1.568],
        [0.92, 0.06, 0.02, 1.775],
        [0.33, 0.61, 0.06, 3.598],
        [0.47, 0.14, 0.39, 3.57],
        [0.61, 0.2, 0.19, 3.747],
        [0.52, 0.23, 0.25, 1.965],
        [0.59, 0.4, 0.01, 0.802],
        [0.64, 0.24, 0.12, 2.423],
        [0.0, 0.07, 0.93, 3.014],
        [0.8, 0.07, 0.13, 2.79],
        [0.04, 0.4, 0.56, 3.863],
        [0.71, 0.11, 0.18, 1.095],
        [0.22, 0.61, 0.17, 3.666],
        [0.43, 0.39, 0.18, 1.887],
    ]
    return np.array(ternary_list)


@pytest.mark.mpl_image_compare
def test_ternary(array):
    """
    Test plotting a ternary chart.
    """
    fig = Figure()
    fig.ternary(
        data=array,
        region=[0, 100, 0, 100, 0, 100],
        cmap="red,orange,yellow,green,blue,violet",
        width="10c",
        frame=["bafg+lAir", "cafg+lLimestone", "aafg+lWater"],
        style="c0.1c",
        pen="thinnest",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_ternary_3_labels(array):
    """
    Test plotting a ternary chart with 3 labels.
    """
    fig = Figure()
    fig.ternary(
        data=array,
        region=[0, 100, 0, 100, 0, 100],
        cmap="red,orange,yellow,green,blue,violet",
        width="10c",
        alabel="A",
        blabel="B",
        clabel="C",
        frame=["bafg+lAir", "cafg+lLimestone", "aafg+lWater"],
        style="c0.1c",
        pen="thinnest",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_ternary_1_label(array):
    """
    Test plotting a ternary chart with 1 label.
    """
    fig = Figure()
    fig.ternary(
        data=array,
        region=[0, 100, 0, 100, 0, 100],
        cmap="red,orange,yellow,green,blue,violet",
        width="10c",
        alabel="A",
        frame=["bafg+lAir", "cafg+lLimestone", "aafg+lWater"],
        style="c0.1c",
        pen="thinnest",
    )
    return fig
