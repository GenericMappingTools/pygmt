"""
Tests for pscoast
"""
from .utils import figure_comparison_test
from .. import figure, pscoast


@figure_comparison_test
def test_pscoast():
    "Simple plot from the GMT docs"
    figure()
    pscoast(R='-30/30/-40/40', J='m0.1i', B=5, I='1/1p,blue', N='1/0.25p,-',
            W='0.25p,white', G='green', S='blue', D='c', A=10000, P=True)


@figure_comparison_test
def test_pscoast_iceland():
    "Test passing in R as a list"
    figure()
    pscoast(R=[-30, -10, 60, 65], J='m1c', B=True, G='p28+r100')


@figure_comparison_test
def test_pscoast_aliases():
    "Test that all aliases work"
    figure()
    pscoast(region='-30/30/-40/40', projection='m0.1i', frame='afg',
            rivers='1/1p,black', borders='1/0.5p,-',
            shorelines='0.25p,white', continents='moccasin', oceans='skyblue',
            resolution='i', area_thresh=1000, portrait=True)
