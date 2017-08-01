"""
Tests psxy.
"""
import os

import pytest

from .. import Figure


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
POINTS_DATA = os.path.join(TEST_DATA_DIR, 'points.txt')


@pytest.mark.mpl_image_compare
def test_psxy_red_circles():
    "Plot the data in red circles"
    fig = Figure()
    fig.psxy(POINTS_DATA, R='10/70/-3/8', J='X4i', S='c0.2c', G='red', B='afg')
    return fig


@pytest.mark.mpl_image_compare
def test_psxy_projection():
    "Plot the data in green squares with a projection"
    fig = Figure()
    fig.psxy(POINTS_DATA, R='g', J='R270/4i', S='s0.2c', G='green', B='ag')
    return fig


@pytest.mark.mpl_image_compare
def test_psxy_aliases():
    "Use aliases for the arguments and make sure they work"
    fig = Figure()
    fig.psxy(POINTS_DATA, region=[10, 70, -3, 8], projection='X10i',
             style='d0.5c', color='yellow', frame=True, portrait=True,
             columns=[0, 1])
    return fig
