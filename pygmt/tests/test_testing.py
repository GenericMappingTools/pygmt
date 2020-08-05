"""
Test the testing functions for PyGMT
"""
from .. import Figure
from ..helpers.testing import check_figures_equal
from ..exceptions import GMTImageComparisonFailure
import pytest


def test_check_figures_equal():
    fig_ref = Figure()
    fig_ref.basemap(projection="X10c", region=[0, 10, 0, 10], frame=True)

    fig_test = Figure()
    fig_test.basemap(projection="X10c", region=[0, 10, 0, 10], frame=True)
    check_figures_equal(fig_ref, fig_test)


def test_check_figures_unequal():
    fig_ref = Figure()
    fig_ref.basemap(projection="X10c", region=[0, 10, 0, 10], frame=True)

    fig_test = Figure()
    fig_test.basemap(projection="X10c", region=[0, 15, 0, 15], frame=True)

    with pytest.raises(GMTImageComparisonFailure):
        check_figures_equal(fig_ref, fig_test)
