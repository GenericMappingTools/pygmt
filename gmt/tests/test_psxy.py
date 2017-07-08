"""
Tests psxy.
"""
import os

from .utils import figure_comparison_test
from .. import figure, psxy


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
POINTS_DATA = os.path.join(TEST_DATA_DIR, 'points.txt')


@figure_comparison_test
def test_psxy_red_circles():
    "Plot the data in red circles"
    figure()
    psxy(POINTS_DATA, R='10/70/-3/8', J='X4i', S='c0.2c', G='red', B='afg')


@figure_comparison_test
def test_psxy_projection():
    "Plot the data in green squares with a projection"
    figure()
    psxy(POINTS_DATA, R='g', J='R270/4i', S='s0.2c', G='green', B='ag')


@figure_comparison_test
def test_psxy_aliases():
    "Use aliases for the arguments and make sure they work"
    figure()
    psxy(POINTS_DATA, region=[10, 70, -3, 8], projection='X10i',
         style='d0.5c', color='yellow', frame=True, portrait=True)
