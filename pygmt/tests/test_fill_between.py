"""
Tests for Figure.fill_between.
"""

import numpy as np
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTValueError


@pytest.fixture(scope="module", name="x")
def fixture_x():
    """
    X-coordinates of the primary curve.
    """
    return np.linspace(0, 4, 100)


@pytest.fixture(scope="module", name="y")
def fixture_y(x):
    """
    Y-coordinates of the primary curve.
    """
    return np.sin(5 * x)


@pytest.fixture(scope="module", name="y2")
def fixture_y2(x):
    """
    Y-coordinates of the secondary curve.
    """
    return 0.5 * np.cos(3 * x)


@pytest.fixture(scope="module", name="x3")
def fixture_x3():
    """
    X-coordinates of the secondary curve with non-co-registered sampling.
    """
    return np.array(
        [0, 0.21, 0.4, 0.63, 0.89, 1.18, 1.45, 1.69, 1.96, 2.26, 2.61, 3.23, 3.49, 4.0]
    )


@pytest.fixture(scope="module", name="y3")
def fixture_y3(x3):
    """
    Y-coordinates of the secondary curve with non-co-registered sampling.
    """
    return 0.5 * np.cos(3 * x3)


@pytest.mark.mpl_image_compare
def test_fill_between_y2_scalar(x, y):
    """
    Fill between a curve and a horizontal reference level.
    """
    fig = Figure()
    fig.basemap(region=[0, 4, -1.2, 1.2], projection="X10c/5c", frame=True)
    fig.fill_between(
        x=x,
        y=y,
        y2=0,
        fill="lightblue",
        fill2="lightred",
        pen="1p,blue",
        pen2="1p,red",
        label="y=sin(5x)",
        label2="y=0",
    )
    fig.plot(x=x, y=y, style="c0.06c", fill="blue", pen="blue")
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_fill_between_coregistered(x, y, y2):
    """
    Fill between two co-registered curves.
    """
    fig = Figure()
    fig.basemap(region=[0, 4, -1.2, 1.2], projection="X10c/5c", frame=True)
    fig.fill_between(
        x=x,
        y=y,
        y2=y2,
        fill="lightgreen",
        fill2="lightbrown",
        pen="1p,green",
        pen2="1p,brown",
        label="y=sin(5x)",
        label2="y=0.5*cos(3x)",
    )
    fig.plot(x=x, y=y, style="c0.06c", fill="green", pen="green")
    fig.plot(x=x, y=y2, style="c0.06c", fill="brown", pen="brown")
    fig.legend()
    return fig


@pytest.mark.mpl_image_compare
def test_fill_between_noncoregistered(x, y, x3, y3):
    """
    Fill between two curves that do not share the same x-coordinates.
    """
    fig = Figure()
    fig.basemap(region=[0, 4, -1.2, 1.2], projection="X10c/5c", frame=True)
    fig.fill_between(
        x=x,
        y=y,
        x2=x3,
        y2=y3,
        fill="lightgreen",
        fill2="lightbrown",
        pen="1p,green",
        pen2="1p,brown",
        label="y=sin(5x)",
        label2="y=0.5*cos(3x)",
    )
    fig.plot(x=x, y=y, style="c0.06c", fill="green", pen="green")
    fig.plot(x=x3, y=y3, style="c0.06c", fill="brown", pen="brown")
    fig.legend()
    return fig


def test_fill_between_invalid_input():
    """
    Test invalid input for fill_between.
    """
    fig = Figure()
    with pytest.raises(GMTValueError):
        fig.fill_between(x=0, y=[1, 2])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=1)
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0], y=[1])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=[1])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=[1, 2], y2=[0])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=[1, 2], y2=[0, 1, 2])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=[1, 2], y2=0, x2=[0, 1])
    with pytest.raises(GMTValueError):
        fig.fill_between(x=[0, 1], y=[1, 2], y2=[0, 1], x2=[0])
