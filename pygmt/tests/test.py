from matplotlib.testing.decorators import check_figures_equal

import pygmt


@check_figures_equal(extensions=["png"])
def test_plot(fig_test, fig_ref):
    fig_test.subplots().plot([1, 3, 5])
    fig_ref.subplots().plot([0, 1, 2], [1, 3, 5])
