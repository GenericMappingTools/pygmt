"""
Tests for inset_begin and inset_end
"""
import pytest
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@pytest.mark.mpl_image_compare
def test_inset_aliases():
    "Test the aliases for the inset functions."
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_ref.inset_begin(D="jTL+w3.5c+o0.2c", M=0, F="+pgreen")
    fig_ref.coast(region="g", projection="G47/-20/4c", G="gray", S="white", E="MG+gred")
    fig_ref.inset_end()
    fig_test.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_test.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_test.coast(
        region="g", projection="G47/-20/4c", G="gray", S="white", E="MG+gred"
    )
    fig_test.inset_end()
    return fig_ref, fig_test
