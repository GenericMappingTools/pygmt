"""
Test Figure.magnetic_rose.
"""

import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare(filename="test_basemap_compass.png")
def test_magnetic_rose():
    """
    Create a map with a compass. Modified from the test_basemap_compass test.
    """
    fig = Figure()
    fig.basemap(region=[127.5, 128.5, 26, 27], projection="H15c", frame=True)
    fig.magnetic_rose(
        position_type="inside", position="MC", width="5c", declination=11.5
    )
    return fig
