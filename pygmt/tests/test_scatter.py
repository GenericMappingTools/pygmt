"""
Test Figure.scatter.
"""

import numpy as np
import pytest
from pygmt import Figure, makecpt


#
#  Fixtures that are used in tests.
#
@pytest.fixture(scope="module", name="region")
def fixture_region():
    """
    The region of sample data.
    """
    return [0, 5, 5, 10]


@pytest.fixture(scope="module", name="x")
def fixture_x():
    """
    The x coordinates of sample data.
    """
    return [1, 2, 3, 4]


@pytest.fixture(scope="module", name="y")
def fixture_y():
    """
    The y coordinates of sample data.
    """
    return [6, 7, 8, 9]


@pytest.fixture(scope="module", name="size")
def fixture_size():
    """
    The size of sample data.
    """
    return [0.2, 0.4, 0.6, 0.8]


@pytest.fixture(scope="module", name="symbol")
def fixture_symbol():
    """
    The symbol of sample data.
    """
    return ["a", "c", "i", "t"]


@pytest.fixture(scope="module", name="fill")
def fixture_fill():
    """
    The z value of sample data for fill.
    """
    return [1, 2, 3, 4]


@pytest.fixture(scope="module", name="transparency")
def fixture_transparency():
    """
    The transparency of sample data.
    """
    return [20, 40, 60, 80]


@pytest.fixture(scope="module", name="intensity")
def fixture_intensity():
    """
    The intensity of sample data.
    """
    return [-0.8, -0.3, 0.3, 0.8]


#
# Tests for the simplest scatter plot with constant size and symbol.
#
@pytest.mark.mpl_image_compare
def test_scatter(region, x, y):
    """
    Test the simplest scatter plot with constant size and symbol.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    fig.scatter(x=x, y=y, symbol="c", size=0.2)
    return fig


#
# Tests for scatter plots with one parameter given as a sequence.
#
@pytest.mark.mpl_image_compare
def test_scatter_sizes(region, x, y, size):
    """
    Test the scatter plot with different sizes.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    fig.scatter(x=x, y=y, symbol="c", size=size)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_symbols(region, x, y, symbol):
    """
    Test the scatter plot with different symbols.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    fig.scatter(x=x, y=y, symbol=symbol, size=0.2)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_fills(region, x, y, fill):
    """
    Test the scatter plot with different colors.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[0, 5])
    fig.scatter(x=x, y=y, symbol="c", size=0.5, fill=fill)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_transparencies(region, x, y, transparency):
    """
    Test the scatter plot with different transparency.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[1, 4])
    fig.scatter(x=x, y=y, symbol="c", size=0.5, fill="red", transparency=transparency)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_intensity(region, x, y, intensity):
    """
    Test the scatter plot with different intensity.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    fig.scatter(x=x, y=y, symbol="c", size=0.5, fill="red", intensity=intensity)
    return fig


#
# Tests for scatter plots with multiple parameters given as sequences.
#
@pytest.mark.mpl_image_compare
def test_scatter_symbols_sizes(region, x, y, symbol, size):
    """
    Test the scatter plot with different symbols and sizes.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    fig.scatter(x=x, y=y, symbol=symbol, size=size)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_sizes_fills(region, x, y, size, fill):
    """
    Test the scatter plot with different sizes and colors.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[0, 5])
    fig.scatter(x=x, y=y, symbol="c", size=size, fill=fill)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_sizes_fills_transparencies(region, x, y, size, fill, transparency):
    """
    Test the scatter plot with different sizes and colors.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[0, 5])
    fig.scatter(x=x, y=y, symbol="c", size=size, fill=fill, transparency=transparency)
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_sizes_fills_transparencies_intensity(
    region, x, y, size, fill, transparency, intensity
):
    """
    Test the scatter plot with different sizes and colors.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[0, 5])
    fig.scatter(
        x=x,
        y=y,
        symbol="c",
        size=size,
        fill=fill,
        transparency=transparency,
        intensity=intensity,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_scatter_symbols_sizes_fills_transparencies_intensity(
    region, x, y, symbol, size, fill, transparency, intensity
):
    """
    Test the scatter plot with different sizes and colors.
    """
    fig = Figure()
    fig.basemap(region=region, frame=True)
    makecpt(cmap="viridis", series=[0, 5])
    fig.scatter(
        x=x,
        y=y,
        symbol=symbol,
        size=size,
        fill=fill,
        transparency=transparency,
        intensity=intensity,
    )
    return fig


#
# Other tests for scatter plots.
#
@pytest.mark.mpl_image_compare
def test_scatter_valid_symbols():
    """
    Test the scatter plot with data.
    """
    symbols = ["-", "+", "a", "c", "d", "g", "h", "i", "n", "s", "t", "x", "y"]
    x = np.arange(len(symbols))
    y = [1.0] * len(symbols)
    fig = Figure()
    fig.basemap(region=[-1, len(symbols), 0, 2], frame=True)
    fig.scatter(x=x, y=y, symbol=symbols, size=0.5, pen="1p,black")
    return fig
