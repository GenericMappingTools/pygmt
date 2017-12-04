# pylint: disable=redefined-outer-name
"""
Tests plot.
"""
import os

import pytest
import numpy as np

from .. import Figure
from ..exceptions import GMTError


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
POINTS_DATA = os.path.join(TEST_DATA_DIR, 'points.txt')


@pytest.fixture(scope='module')
def data():
    "Load the point data from the test file"
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope='module')
def region():
    "The data region"
    return [10, 70, -5, 10]


@pytest.mark.mpl_image_compare
def test_plot_red_circles(data, region):
    "Plot the data in red circles passing in vectors"
    fig = Figure()
    fig.plot(x=data[:, 0], y=data[:, 1], region=region, projection='X4i',
             style='c0.2c', color='red', frame='afg')
    return fig


def test_plot_fail_no_data(data):
    "Plot should raise an exception if no data is given"
    fig = Figure()
    with pytest.raises(GMTError):
        fig.plot(region=region, projection='X4i', style='c0.2c', color='red',
                 frame='afg')
    with pytest.raises(GMTError):
        fig.plot(x=data[:, 0], region=region, projection='X4i', style='c0.2c',
                 color='red', frame='afg')
    with pytest.raises(GMTError):
        fig.plot(y=data[:, 0], region=region, projection='X4i', style='c0.2c',
                 color='red', frame='afg')
    # Should also fail if given too much data
    with pytest.raises(GMTError):
        fig.plot(x=data[:, 0], y=data[:, 1], data=data, region=region,
                 projection='X4i', style='c0.2c', color='red', frame='afg')


def test_plot_fail_size_color(data):
    "Should raise an exception if array sizes and color are used with matrix"
    fig = Figure()
    with pytest.raises(GMTError):
        fig.plot(data=data, region=region, projection='X4i', style='c0.2c',
                 color=data[:, 2], frame='afg')
    with pytest.raises(GMTError):
        fig.plot(data=data, region=region, projection='X4i', style='cc',
                 sizes=data[:, 2], color='red', frame='afg')


@pytest.mark.mpl_image_compare
def test_plot_projection(data):
    "Plot the data in green squares with a projection"
    fig = Figure()
    fig.plot(x=data[:, 0], y=data[:, 1], region='g', projection='R270/4i',
             style='s0.2c', color='green', frame='ag')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors(data, region):
    "Plot the data using z as sizes"
    fig = Figure()
    fig.plot(x=data[:, 0], y=data[:, 1], color=data[:, 2], region=region,
             projection='X3i', style='c0.5c', cmap='cubhelix', frame='af')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_sizes(data, region):
    "Plot the data using z as sizes"
    fig = Figure()
    fig.plot(x=data[:, 0], y=data[:, 1], sizes=0.5*data[:, 2], region=region,
             projection='X4i', style='cc', color='blue', frame='af')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors_sizes(data, region):
    "Plot the data using z as sizes and colors"
    fig = Figure()
    fig.plot(x=data[:, 0], y=data[:, 1], color=data[:, 2],
             sizes=0.5*data[:, 2], region=region, projection='X3i', style='cc',
             cmap='copper', frame='af')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_colors_sizes_proj(data, region):
    "Plot the data using z as sizes and colors with a projection"
    fig = Figure()
    fig.coast(region=region, projection='M10i', frame='af', water='skyblue')
    fig.plot(x=data[:, 0], y=data[:, 1], color=data[:, 2],
             sizes=0.5*data[:, 2], style='cc',
             cmap='copper')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_matrix(data):
    "Plot the data passing in a matrix and specifying columns"
    fig = Figure()
    fig.plot(data=data, region=[10, 70, -5, 10], projection='M10i', style='cc',
             color='#aaaaaa', B='a', columns='0,1,2+s0.005')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_matrix_color(data):
    "Plot the data passing in a matrix and using a colormap"
    fig = Figure()
    fig.plot(data=data, region=[10, 70, -5, 10], projection='X5i',
             style='c0.5c', cmap='rainbow', B='a')
    return fig


@pytest.mark.mpl_image_compare
def test_plot_from_file(region):
    "Plot using the data file name instead of loaded data"
    fig = Figure()
    fig.plot(data=POINTS_DATA, region=region, projection='X10i', style='d1c',
             color='yellow', frame=True, portrait=True, columns=[0, 1])
    return fig
