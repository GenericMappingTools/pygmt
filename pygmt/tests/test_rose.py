"""
Tests for rose
"""
import numpy as np
import pytest
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_rose_fig_equal():
    """
    Test supplying a data file containing a list of
    fracture lengths and directions as digitized
    from geological maps to the data argument
    (lengths are stored in the second column,
    directions in the first, specify via columns).
    Passing in R as list and string.
    """

    fig_ref, fig_test = Figure(), Figure()

    fig_ref.rose(
        data="@fractures_06.txt",
        region="0/1/0/360",
        sector_width=15,
        diameter="5.5c",
        color="blue",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        columns=[1, 0],
        pen="1p",
        norm="",
        scale=0.4,
    )

    fig_test.rose(
        data="@fractures_06.txt",
        R=[0, 1, 0, 360],
        A=15,
        JX="5.5c",
        G="blue",
        B=["x0.2g0.2", "y30g30", "+glightgray"],
        i=[1, 0],
        W="1p",
        S=True,
        Z=0.4,
    )

    return fig_ref, fig_test


@pytest.mark.mpl_image_compare
def test_rose_data_file():
    """
    Test supplying a data file containing a list of
    fracture lengths and directions as digitized
    from geological maps to the data argument
    (lengths are stored in the second column,
    directions in the first, specify via columns).
    """

    fig = Figure()

    fig.rose(
        data="@fractures_06.txt",
        region="0/1/0/360",
        sector_width=15,
        diameter="5.5c",
        color="blue",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        columns=[1, 0],
        pen="1p",
        norm=True,
        scale=0.4,
    )

    return fig


@pytest.mark.mpl_image_compare
def test_rose_2d_array_single():
    """
    Test supplying a 2D numpy array containing a
    single pair of lengths and directions.
    """

    fig = Figure()

    data = np.array([[40, 60]])

    fig.rose(
        data=data,
        region="0/1/0/360",
        sector_width=10,
        diameter="5.5c",
        color="cyan",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        pen="1p",
        norm=True,
        scale=0.4,
    )

    return fig


@pytest.mark.mpl_image_compare
def test_rose_2d_array_multiple():
    """
    Test supplying a 2D numpy array containing a
    list of lengths and directions.
    """

    fig = Figure()

    data = np.array(
        [[40, 60], [60, 300], [20, 180], [30, 190], [60, 90], [40, 110], [80, 125]]
    )

    fig.rose(
        data=data,
        region="0/1/0/360",
        sector_width=10,
        diameter="5.5c",
        color="blue",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        pen="1p",
        norm=True,
        scale=0.4,
    )

    return fig


@pytest.mark.mpl_image_compare
def test_rose_plot_data_using_cpt():
    """
    Test supplying a 2D numpy array containing a list of
    lengths and directions. Use a cmap to color sectors.
    """

    fig = Figure()

    data = np.array(
        [[40, 60], [60, 300], [20, 180], [30, 190], [60, 90], [40, 110], [80, 125]]
    )

    fig.rose(
        data=data,
        region="0/1/0/360",
        sector_width=15,
        diameter="5.5c",
        cmap="batlow",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        pen="1p",
        norm=True,
        scale=0.4,
    )

    return fig


@pytest.mark.mpl_image_compare
def test_rose_plot_with_transparency():
    """
    Test supplying a data file containing a list of
    fracture lengths and directions as digitized
    from geological maps to the data argument
    (lengths are stored in the second column,
    directions in the first, specify via columns).
    Use transparency.
    """

    fig = Figure()

    fig.rose(
        data="@fractures_06.txt",
        region="0/1/0/360",
        sector_width=15,
        diameter="5.5c",
        color="blue",
        frame=["x0.2g0.2", "y30g30", "+glightgray"],
        columns=[1, 0],
        pen="1p",
        norm=True,
        scale=0.4,
        transparency=50,
    )

    return fig


@pytest.mark.mpl_image_compare
def test_rose_no_sectors():
    """
    Test supplying a data file containing a list of
    fracture lengths and directions as digitized
    from geological maps to the data argument
    (lengths are stored in the second column,
    directions in the first, specify via columns).
    Plot data without defining a sector width,
    add a title and rename labels.
    """

    fig = Figure()

    fig.rose(
        data="@fractures_06.txt",
        region="0/500/0/360",
        columns="1,0",
        diameter="10c",
        labels="180/0/90/270",
        frame=["xg100", "yg45", "+t'Windrose diagram'"],
        pen="1.5p,red3",
        transparency=40,
        scale=0.5,
    )

    return fig
