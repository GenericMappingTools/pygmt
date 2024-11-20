"""
Tests for hline.
"""

from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_hlines_value_sets():
    """
    Passing sets of y, xmin and xmax.
    """

    fig_ref, fig_test = Figure(), Figure()

    fig_ref.basemap(region=[0, 10, 0, 20], projection="X10c/10c", frame=True)
    fig_ref.hlines(
        y=[5.5, 10, 6, 11],
        xmin=[3.1, 6, 0, 1],
        xmax=[5.5, 7.8, 10, 9],
        label="test2",
        pen="4p,green",
    )

    fig_test.basemap(region="0/10/0/20", projection="X10c/10c", frame=True)
    fig_test.hlines(
        y=[5.5, 10, 6, 11],
        xmin=[3.1, 6, 0, 1],
        xmax=[5.5, 7.8, 10, 9],
        label="test2",
        pen="4p,green",
    )

    return fig_ref, fig_test
