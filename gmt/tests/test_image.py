"""
Tests image.
"""
import os

import pytest

from .. import Figure


TEST_IMG = os.path.join(os.path.dirname(__file__), "baseline", "test_logo.png")


@pytest.mark.mpl_image_compare
def test_image():
    "Place images on map"
    fig = Figure()
    fig.image(TEST_IMG, D="x0/0+w1i", F="+pthin,blue")
    return fig
