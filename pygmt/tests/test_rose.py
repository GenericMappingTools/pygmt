"""
Test Figure.rose.
"""

import numpy as np
import pytest
from pygmt import Figure
from pygmt.datasets import load_sample_data
from pygmt.params import Axis, Frame


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the sample numpy array data.
    """
    return np.array(
        [[40, 60], [60, 300], [20, 180], [30, 190], [60, 90], [40, 110], [80, 125]]
    )


@pytest.fixture(scope="module", name="data_fractures_compilation")
def fixture_data_fractures_compilation():
    """
    Load the sample fractures compilation dataset which contains fracture lengths and
    azimuths as hypothetically digitized from geological maps.

    Lengths are stored in the first column, azimuths in the second.
    """
    return load_sample_data(name="fractures")


@pytest.mark.mpl_image_compare
def test_rose_data_file(data_fractures_compilation):
    """
    Test supplying data from sample dataset.
    """
    fig = Figure()
    fig.rose(
        data=data_fractures_compilation,
        region=[0, 1, 0, 360],
        sector=15,
        diameter="5.5c",
        fill="blue",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="lightgray",
        ),
        pen="1p",
        norm="",
        scale=0.4,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_rose_2d_array_single():
    """
    Test supplying a 2-D numpy array containing a single pair of lengths and directions.
    """
    data = np.array([[40, 60]])
    fig = Figure()
    fig.rose(
        data=data,
        region=[0, 1, 0, 360],
        sector=10,
        diameter="5.5c",
        fill="cyan",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="lightgray",
        ),
        pen="1p",
        norm=True,
        scale=0.4,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_rose_2d_array_multiple(data):
    """
    Test supplying a 2-D numpy array containing a list of lengths and directions.
    """
    fig = Figure()
    fig.rose(
        data=data,
        region=[0, 1, 0, 360],
        sector=10,
        diameter="5.5c",
        fill="blue",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="moccasin",
        ),
        pen="1p",
        norm=True,
        scale=0.4,
    )
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare
def test_rose_plot_data_using_cpt(data):
    """
    Test supplying a 2-D numpy array containing a list of lengths and directions.

    Use a cmap to color sectors.
    """
    fig = Figure()
    fig.rose(
        data=data,
        region=[0, 1, 0, 360],
        sector=15,
        diameter="5.5c",
        cmap="SCM/batlow",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="darkgray",
        ),
        pen="1p",
        norm=True,
        scale=0.4,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_rose_plot_with_transparency(data_fractures_compilation):
    """
    Test supplying the sample fractures compilation dataset to the data parameter.

    Use transparency.
    """
    fig = Figure()
    fig.rose(
        data=data_fractures_compilation,
        region=[0, 1, 0, 360],
        sector=15,
        diameter="5.5c",
        fill="blue",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="lightgray",
        ),
        pen="1p",
        norm=True,
        scale=0.4,
        transparency=50,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_rose_no_sectors(data_fractures_compilation):
    """
    Test supplying the sample fractures compilation dataset to the data parameter.

    Plot data without defining a sector width, add a title and rename labels.
    """
    fig = Figure()
    fig.rose(
        data=data_fractures_compilation,
        region=[0, 500, 0, 360],
        diameter="10c",
        labels="180/0/90/270",
        frame=Frame(
            xaxis=Axis(grid=100), yaxis=Axis(grid=45), title="Windrose diagram"
        ),
        pen="1.5p,red3",
        transparency=40,
        scale=0.5,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_rose_bools(data_fractures_compilation):
    """
    Test supplying the sample fractures compilation dataset to the data parameter.

    Test bools.
    """
    fig = Figure()
    fig.rose(
        data=data_fractures_compilation,
        region=[0, 1, 0, 360],
        sector=10,
        diameter="10c",
        frame=Frame(
            xaxis=Axis(annot=0.2, grid=0.2),
            yaxis=Axis(grid=30, annot=30),
            fill="lightgray",
        ),
        fill="red3",
        pen="1p",
        orientation=False,
        norm=True,
        vectors=True,
        no_scale=True,
        shift=False,
    )
    return fig
