"""
Test Figure.shift_origin.
"""

import pytest
from pygmt.exceptions import GMTInvalidInput
from pygmt.figure import Figure


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


def test_shift_origin_unsupported_xshift_yshift():
    """
    Raise an exception if X/Y/xshift/yshift is used.
    """
    fig = Figure()
    fig.basemap(region=[0, 1, 0, 1], projection="X1c/1c", frame=True)
    with pytest.raises(GMTInvalidInput):
        fig.plot(x=1, y=1, style="c3c", xshift="3c")
    with pytest.raises(GMTInvalidInput):
        fig.plot(x=1, y=1, style="c3c", X="3c")
    with pytest.raises(GMTInvalidInput):
        fig.plot(x=1, y=1, style="c3c", yshift="3c")
    with pytest.raises(GMTInvalidInput):
        fig.plot(x=1, y=1, style="c3c", Y="3c")
