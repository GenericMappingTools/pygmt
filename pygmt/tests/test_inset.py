"""
Tests for inset_begin and inset_end
"""
import pytest
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_inset_aliases():
    "Test the aliases for the inset functions."
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_ref.inset_begin(D="jTL+w3.5c+o0.2c", M=0, F="+pgreen")
    fig_ref.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    fig_ref.inset_end()
    fig_test.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_test.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_test.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    fig_test.inset_end()
    return fig_ref, fig_test


@check_figures_equal()
def test_inset_end():
    "Test that plotting functions called after inset_end() affect the larger plot."
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    # Add a title before calling inset_begin()
    fig_ref.basemap(frame="+tTest")
    fig_ref.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_ref.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    fig_ref.inset_end()
    fig_test.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_test.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_test.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    fig_test.inset_end()
    # Add a title after calling inset_end()
    fig_test.basemap(frame="+tTest")
    return fig_ref, fig_test


@check_figures_equal()
def test_inset_end_requirement():
    """Test that inset_end() does not need to be called if inset is added at
    the end of the figure."""
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_ref.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_ref.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    # fig_ref includes calling inset_end()
    fig_ref.inset_end()
    fig_test.coast(
        region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a"
    )
    fig_test.inset_begin(location="jTL+w3.5c+o0.2c", margin=0, border="+pgreen")
    fig_test.coast(
        region="g", projection="G47/-20/4c", land="gray", water="white", E="MG+gred"
    )
    # fig_test does not include calling inset_end()
    return fig_ref, fig_test
