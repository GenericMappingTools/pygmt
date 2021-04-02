"""
Tests for the inset function.
"""
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@pytest.mark.mpl_image_compare
def test_inset_aliases():
    """
    Test the aliases for the inset function.
    """
    fig = Figure()
    fig.basemap(region="MG+r2", frame="afg")
    with fig.inset(position="jTL+w3.5c+o0.2c", margin=0, box="+pgreen"):
        fig.basemap(region="g", projection="G47/-20/4c", frame="afg")
    return fig


@check_figures_equal()
def test_inset_context_manager():
    """
    Test that the inset context manager works and, once closed, plotting
    elements are added to the larger figure.
    """
    fig_ref, fig_test = Figure(), Figure()

    fig_ref.basemap(region=[-74, -69.5, 41, 43], projection="M9c", frame=True)
    fig_ref.basemap(rose="jTR+w3c")  # Pass rose argument with basemap before the inset
    with fig_ref.inset(position="jBL+w3c+o0.2c", margin=0, box="+pblack"):
        fig_ref.basemap(region=[-80, -65, 35, 50], projection="M3c", frame="afg")

    fig_test.basemap(region=[-74, -69.5, 41, 43], projection="M9c", frame=True)
    with fig_test.inset(position="jBL+w3c+o0.2c", margin=0, box="+pblack"):
        fig_test.basemap(region=[-80, -65, 35, 50], projection="M3c", frame="afg")
    fig_test.basemap(rose="jTR+w3c")  # Pass rose argument with basemap after the inset

    return fig_ref, fig_test
