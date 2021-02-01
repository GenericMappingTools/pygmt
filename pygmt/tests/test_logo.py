"""
Tests for fig.logo.
"""
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_logo():
    """
    Plot a GMT logo of a 2 inch width as a stand-alone plot.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.logo(D="x0/0+w2i")
    fig_test.logo(position="x0/0+w2i")
    return fig_ref, fig_test


@check_figures_equal()
def test_logo_on_a_map():
    """
    Plot a GMT logo in the upper right corner of a map.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="-90/-70/0/20", J="M6i", G="chocolate", B="")
    fig_ref.logo(D="jTR+o0.1i/0.1i+w3i", F="")

    fig_test.coast(
        region=[-90, -70, 0, 20], projection="M6i", land="chocolate", frame=True
    )
    fig_test.logo(position="jTR+o0.1i/0.1i+w3i", box=True)
    return fig_ref, fig_test
