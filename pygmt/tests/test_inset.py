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
    with fig_test.inset(location="jTL+w3.5c+o0.2c", margin=0, box="+pgreen"):
        fig_test.coast(
            region="g",
            projection="G47/-20/4c",
            land="gray",
            water="white",
            dcw="MG+gred",
        )
    return fig_ref, fig_test


@check_figures_equal()
def test_inset_context_manager():
    """
    Test that the inset context manager works and, once closed, plotting
    elements are added to the larger figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    fig_ref.coast(
        region=[-74, -69.5, 41, 43],
        borders="2/thin",
        shorelines="thin",
        projection="M15c",
        land="lightyellow",
        water="lightblue",
    )
    # Test passing the frame argument with basemap before the inset
    fig_ref.basemap(frame="a")
    with fig_ref.inset(location="jBL+w3c+o0.2c", margin=0, box="+pblack"):
        fig_ref.coast(
            region=[-80, -65, 35, 50],
            projection="M3c",
            land="gray",
            borders=[1, 2],
            shorelines="1/thin",
            water="white",
            dcw="US.MA+gred",
        )
    fig_test.coast(
        region=[-74, -69.5, 41, 43],
        borders="2/thin",
        shorelines="thin",
        projection="M15c",
        land="lightyellow",
        water="lightblue",
    )

    with fig_test.inset(location="jBL+w3c+o0.2c", margin=0, box="+pblack"):
        fig_test.coast(
            region=[-80, -65, 35, 50],
            projection="M3c",
            land="gray",
            borders=[1, 2],
            shorelines="1/thin",
            water="white",
            dcw="US.MA+gred",
        )
    # Test passing the frame argument with basemap after the inset
    fig_test.basemap(frame="a")
    return fig_ref, fig_test
