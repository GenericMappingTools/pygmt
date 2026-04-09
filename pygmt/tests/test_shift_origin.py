"""
Test Figure.shift_origin.
"""

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError


def _numbered_basemap(fig, number, size=3):
    """
    A utility function to create a basemap with a number in the center.
    """
    fig.basemap(region=[0, 1, 0, 1], projection=f"X{size}c", frame=0)
    fig.text(position="MC", text=number, font="24p")


@pytest.mark.mpl_image_compare
def test_shift_origin():
    """
    Test if fig.shift_origin works.
    """
    kwargs = {"region": [0, 3, 0, 5], "projection": "X3c/5c", "frame": 0}
    fig = Figure()
    # First call shift_origin without projection and region.
    # Test issue https://github.com/GenericMappingTools/pygmt/issues/514
    fig.shift_origin(xshift="2c", yshift="3c")
    fig.basemap(**kwargs)
    fig.shift_origin(xshift="4c")
    fig.basemap(**kwargs)
    fig.shift_origin(yshift="6c")
    fig.basemap(**kwargs)
    fig.shift_origin(xshift="-4c", yshift="6c")
    fig.basemap(**kwargs)
    return fig


@pytest.mark.mpl_image_compare
def test_shift_origin_context_manager():
    """
    Test if Figure.shift_origin as a context manager shifts origin temporarily.

    Expected output is:
    | 3 | 4 |
    | 1 | 2 |
    """
    fig = Figure()
    _numbered_basemap(fig, 1, size=2.5)
    with fig.shift_origin(xshift=3):
        _numbered_basemap(fig, 2, size=2.5)
    with fig.shift_origin(yshift=3):
        _numbered_basemap(fig, 3, size=2.5)
    with fig.shift_origin(xshift=3, yshift=3):
        _numbered_basemap(fig, 4, size=2.5)
    return fig


@pytest.mark.mpl_image_compare
def test_shift_origin_nested_context_manager():
    """
    Test if Figure.shift_origin shifts origin correctly when used in a nested context
    manager.

    Expected output is:
    | 4 | 3 |
    | 1 | 2 |
    """
    fig = Figure()
    _numbered_basemap(fig, 1, size=2.5)
    with fig.shift_origin(xshift=3):
        _numbered_basemap(fig, 2, size=2.5)
        with fig.shift_origin(yshift=3):
            _numbered_basemap(fig, 3, size=2.5)
    with fig.shift_origin(yshift=3):
        _numbered_basemap(fig, 4, size=2.5)
    return fig


@pytest.mark.mpl_image_compare
def test_shift_origin_mixed_modes():
    """
    Test if Figure.shift_origin works when used as a context manager and as a
    method at the same time.

    Expected output is:
    |   | 3 | 4 |
    | 1 | 2 |   |
    """
    fig = Figure()
    _numbered_basemap(fig, 1, size=2.5)
    with fig.shift_origin(xshift=3):
        _numbered_basemap(fig, 2, size=2.5)
    fig.shift_origin(xshift=3)
    with fig.shift_origin(yshift=3):
        _numbered_basemap(fig, 3, size=2.5)
    fig.shift_origin(xshift=3, yshift=3)
    _numbered_basemap(fig, 4, size=2.5)
    return fig


def test_shift_origin_unsupported_xshift_yshift():
    """
    Raise an exception if X/Y/xshift/yshift is used.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    with pytest.raises(GMTParameterError):
        fig.plot(x=1, y=1, style="c3c", xshift="3c")
    with pytest.raises(GMTParameterError):
        fig.plot(x=1, y=1, style="c3c", X="3c")
    with pytest.raises(GMTParameterError):
        fig.plot(x=1, y=1, style="c3c", yshift="3c")
    with pytest.raises(GMTParameterError):
        fig.plot(x=1, y=1, style="c3c", Y="3c")
