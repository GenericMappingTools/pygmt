"""
Tests for the inset function.
"""
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_inset_aliases():
    """
    Test the aliases for the inset function.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    with fig_ref.inset(D="jTL+w3.5c+o0.2c", M=0, F="+pgreen"):
        fig_ref.coast(
            region="g",
            projection="G47/-20/4c",
            land="gray",
            water="white",
            dcw="MG+gred",
        )
    fig_test.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    with fig_test.inset(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen"):
        fig_test.coast(
            region="g",
            projection="G47/-20/4c",
            land="gray",
            water="white",
            dcw="MG+gred",
        )
    return fig_ref, fig_test
