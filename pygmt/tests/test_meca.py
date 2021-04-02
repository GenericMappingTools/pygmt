"""
Tests for meca.
"""
import os

import numpy as np
import pandas as pd
import pytest
from pygmt import Figure
from pygmt.helpers import GMTTempFile

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.mpl_image_compare
def test_meca_spec_dictionary():
    """
    Test supplying a dictionary containing a single focal mechanism to the spec
    parameter.
    """
    fig = Figure()
    # Right lateral strike slip focal mechanism
    fig.meca(
        dict(strike=0, dip=90, rake=0, magnitude=5),
        longitude=0,
        latitude=5,
        depth=0,
        scale="2.5c",
        region=[-1, 1, 4, 6],
        projection="M14c",
        frame=2,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_dict_list():
    """
    Test supplying a dictionary containing a list of focal mechanism to the
    spec parameter.
    """
    fig = Figure()
    # supply focal mechanisms as a dict of lists
    focal_mechanisms = dict(
        strike=[330, 350], dip=[30, 50], rake=[90, 90], magnitude=[3, 2]
    )
    fig.meca(
        focal_mechanisms,
        longitude=[-124.3, -124.4],
        latitude=[48.1, 48.2],
        depth=[12.0, 11.0],
        region=[-125, -122, 47, 49],
        scale="2c",
        projection="M14c",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_dataframe():
    """
    Test supplying a pandas.DataFrame containing focal mechanisms and locations
    to the spec parameter.
    """

    fig = Figure()

    # supply focal mechanisms to meca as a dataframe
    focal_mechanisms = dict(
        strike=[324, 353],
        dip=[20.6, 40],
        rake=[83, 90],
        magnitude=[3.4, 2.9],
        longitude=[-124, -124.4],
        latitude=[48.1, 48.2],
        depth=[12, 11.0],
    )
    spec_dataframe = pd.DataFrame(data=focal_mechanisms)
    fig.meca(spec_dataframe, region=[-125, -122, 47, 49], scale="2c", projection="M14c")
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_1d_array():
    """
    Test supplying a 1D numpy array containing focal mechanisms and locations
    to the spec parameter.
    """
    fig = Figure()
    # supply focal mechanisms to meca as a 1D numpy array, here we are using
    # the Harvard CMT zero trace convention but the focal mechanism
    # parameters may be specified any of the available conventions. Since we
    # are not using a dict or dataframe the convention and component should
    # be specified.
    focal_mechanism = [
        -127.40,  # longitude
        40.87,  # latitude
        12,  # depth
        -3.19,  # mrr
        0.16,  # mtt
        3.03,  # mff
        -1.02,  # mrt
        -3.93,  # mrf
        -0.02,  # mtf
        23,  # exponent
        0,  # plot_lon, 0 to plot at event location
        0,  # plot_lat, 0 to plot at event location
    ]
    focal_mech_array = np.asarray(focal_mechanism)
    fig.meca(
        focal_mech_array,
        convention="mt",
        component="full",
        region=[-128, -127, 40, 41],
        scale="2c",
        projection="M14c",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_2d_array():
    """
    Test supplying a 2D numpy array containing focal mechanisms and locations
    to the spec parameter.
    """
    fig = Figure()
    # supply focal mechanisms to meca as a 2D numpy array, here we are using
    # the GCMT convention but the focal mechanism parameters may be
    # specified any of the available conventions. Since we are not using a
    # dict or dataframe the convention and component should be specified.
    focal_mechanisms = [
        [
            -127.40,  # longitude
            40.87,  # latitude
            12,  # depth
            170,  # strike1
            20,  # dip1
            -110,  # rake1
            11,  # strike2
            71,  # dip2
            -83,  # rake2
            5.1,  # mantissa
            23,  # exponent
            0,  # plot_lon, 0 means we want to plot at the event location
            0,  # plot_lat
        ],
        [-127.50, 40.88, 12.0, 168, 40, -115, 20, 54, -70, 4.0, 23, 0, 0],
    ]
    focal_mechs_array = np.asarray(focal_mechanisms)
    fig.meca(
        focal_mechs_array,
        convention="gcmt",
        region=[-128, -127, 40, 41],
        scale="2c",
        projection="M14c",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_file():
    """
    Test supplying a file containing focal mechanisms and locations to the spec
    parameter.
    """

    fig = Figure()
    focal_mechanism = [-127.43, 40.81, 12, -3.19, 1.16, 3.93, -1.02, -3.93, -1.02, 23]
    # writes temp file to pass to gmt
    with GMTTempFile() as temp:
        with open(temp.name, mode="w") as temp_file:
            temp_file.write(" ".join([str(x) for x in focal_mechanism]))
        # supply focal mechanisms to meca as a file
        fig.meca(
            temp.name,
            convention="mt",
            component="full",
            region=[-128, -127, 40, 41],
            scale="2c",
            projection="M14c",
        )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_loc_array():
    """
    Test supplying lists and np.ndarrays as the event location (longitude,
    latitude, and depth).
    """
    fig = Figure()
    # specify focal mechanisms
    focal_mechanisms = dict(
        strike=[327, 350], dip=[41, 50], rake=[68, 90], magnitude=[3, 2]
    )
    # longitude, latitude, and depth may be specified as an int, float,
    # list, or 1d numpy array
    longitude = np.array([-123.3, -124.4])
    latitude = np.array([48.4, 48.2])
    depth = [12.0, 11.0]  # to test mixed data types as inputs
    scale = "2c"
    fig.meca(
        focal_mechanisms,
        scale,
        longitude,
        latitude,
        depth,
        region=[-125, -122, 47, 49],
        projection="M14c",
    )
    return fig
