"""
Tests for meca.
"""
import numpy as np
import pandas as pd
import pytest
from pygmt import Figure
from pygmt.helpers import GMTTempFile


@pytest.mark.mpl_image_compare(filename="test_meca_spec_single_focalmecha.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha", "dict_full", "array1d", "pandas"])
def test_meca_spec_single_focalmecha(inputtype):
    """
    Test passing a single focal mechanism to the spec parameter.
    """
    if inputtype == "dict_mecha":
        args = {
            "spec": {"strike": 0, "dip": 90, "rake": 0, "magnitude": 5},
            "longitude": 0,
            "latitude": 5,
            "depth": 0,
        }
    elif inputtype == "dict_full":
        args = {
            "spec": {
                "longitude": 0,
                "latitude": 5,
                "depth": 0,
                "strike": 0,
                "dip": 90,
                "rake": 0,
                "magnitude": 5,
            }
        }
    elif inputtype == "array1d":
        args = {
            "spec": np.array([0, 5, 0, 0, 90, 0, 5]),
            "convention": "a",
        }
    elif inputtype == "pandas":
        args = {
            "spec": pd.DataFrame(
                {
                    "longitude": 0,
                    "latitude": 5,
                    "depth": 0,
                    "strike": 0,
                    "dip": 90,
                    "rake": 0,
                    "magnitude": 5,
                },
                index=[0],
            )
        }
    fig = Figure()
    fig.basemap(region=[-1, 1, 4, 6], projection="M8c", frame=2)
    fig.meca(scale="2.5c", **args)
    return fig


@pytest.mark.mpl_image_compare(filename="test_meca_spec_single_focalmecha.png")
def test_meca_spec_single_focalmecha_file():
    """
    Test supplying a file containing focal mechanisms and locations to the spec
    parameter.
    """
    fig = Figure()
    fig.basemap(region=[-1, 1, 4, 6], projection="M8c", frame=2)
    with GMTTempFile() as temp:
        with open(temp.name, mode="w", encoding="utf8") as temp_file:
            temp_file.write("0 5 0 0 90 0 5")
        fig.meca(
            spec=temp.name,
            convention="aki",
            scale="2.5c",
        )
    return fig


@pytest.mark.mpl_image_compare(filename="test_meca_spec_multiple_focalmecha.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha"])
def test_meca_spec_multiple_focalmecha(inputtype):
    """
    Test passing multiple focal mechanisms to the spec parameter.
    """
    if inputtype == "dict_mecha":
        args = {
            "spec": {
                "strike": [330, 350],
                "dip": [30, 50],
                "rake": [90, 90],
                "magnitude": [3, 2],
            },
            "longitude": [-123.5, -124.5],
            "latitude": [47.5, 48.5],
            "depth": [12.0, 11.0],
        }
    fig = Figure()
    fig.basemap(region=[-125, -122, 47, 49], projection="M8c", frame=True)
    fig.meca(scale="2c", **args)
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_dataframe():
    """
    Test supplying a pandas.DataFrame containing focal mechanisms and locations
    to the spec parameter.
    """

    fig = Figure()
    # supply focal mechanisms to meca as a dataframe
    focal_mechanisms = {
        "strike": [324, 353],
        "dip": [20.6, 40],
        "rake": [83, 90],
        "magnitude": [3.4, 2.9],
        "longitude": [-124, -124.4],
        "latitude": [48.1, 48.2],
        "depth": [12, 11.0],
    }
    fig.meca(
        spec=pd.DataFrame(data=focal_mechanisms),
        region=[-125, -122, 47, 49],
        scale="2c",
        projection="M14c",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_spec_2d_array():
    """
    Test supplying a 2-D numpy array containing focal mechanisms and locations
    to the spec parameter.
    """
    fig = Figure()
    # supply focal mechanisms to meca as a 2-D numpy array, here we are using
    # the GCMT convention but the focal mechanism parameters may be
    # specified any of the available conventions. Since we are not using a
    # dict or dataframe the convention and component should be specified.

    # longitude, latitude, depth, strike1, rake1, strike2, dip2, rake2,
    # mantissa, exponent, plot_longitude, plot_latitude
    focal_mechanisms = np.array(
        [
            [-127.40, 40.87, 12, 170, 20, -110, 11, 71, -83, 5.1, 23, 0, 0],
            [-127.50, 40.88, 12.0, 168, 40, -115, 20, 54, -70, 4.0, 23, 0, 0],
        ]
    )
    fig.meca(
        spec=focal_mechanisms,
        convention="gcmt",
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
    focal_mechanisms = {
        "strike": [327, 350],
        "dip": [41, 50],
        "rake": [68, 90],
        "magnitude": [3, 2],
    }
    # longitude, latitude, and depth may be specified as an int, float,
    # list, or 1-D numpy array
    longitude = np.array([-123.3, -124.4])
    latitude = np.array([48.4, 48.2])
    depth = [12.0, 11.0]  # to test mixed data types as inputs
    scale = "2c"
    fig.meca(
        focal_mechanisms,
        scale,
        longitude=longitude,
        latitude=latitude,
        depth=depth,
        region=[-125, -122, 47, 49],
        projection="M14c",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_dict_offset():
    """
    Test offsetting beachballs for a dict input.
    """
    fig = Figure()
    focal_mechanism = {"strike": 330, "dip": 30, "rake": 90, "magnitude": 3}
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(
        spec=focal_mechanism,
        scale="1c",
        longitude=-124,
        latitude=48,
        depth=12.0,
        plot_longitude=-124.5,
        plot_latitude=47.5,
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_meca_dict_offset.png")
def test_meca_dict_offset_in_dict():
    """
    Test offsetting beachballs for a dict input with offset parameters in the
    dict.

    See https://github.com/GenericMappingTools/pygmt/issues/2016.
    """
    fig = Figure()
    focal_mechanism = {
        "strike": 330,
        "dip": 30,
        "rake": 90,
        "magnitude": 3,
        "plot_longitude": -124.5,
        "plot_latitude": 47.5,
    }
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(
        spec=focal_mechanism,
        scale="1c",
        longitude=-124,
        latitude=48,
        depth=12.0,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_dict_eventname():
    """
    Test offsetting beachballs for a dict input.
    """
    fig = Figure()
    focal_mechanism = {"strike": 330, "dip": 30, "rake": 90, "magnitude": 3}
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(
        spec=focal_mechanism,
        scale="1c",
        longitude=-124,
        latitude=48,
        depth=12.0,
        event_name="Event20220311",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_meca_dict_offset_eventname():
    """
    Test offsetting beachballs for a dict input.
    """
    fig = Figure()
    focal_mechanism = {"strike": 330, "dip": 30, "rake": 90, "magnitude": 3}
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(
        spec=focal_mechanism,
        scale="1c",
        longitude=-124,
        latitude=48,
        depth=12.0,
        plot_longitude=-124.5,
        plot_latitude=47.5,
        event_name="Event20220311",
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_meca_dict_eventname.png")
def test_meca_spec_dict_all_scalars():
    """
    Test supplying a dict with scalar values for all focal parameters.

    This is a regression test for
    https://github.com/GenericMappingTools/pygmt/pull/2174
    """
    fig = Figure()
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(
        spec={
            "strike": 330,
            "dip": 30,
            "rake": 90,
            "magnitude": 3,
            "longitude": -124,
            "latitude": 48,
            "depth": 12.0,
            "event_name": "Event20220311",
        },
        scale="1c",
    )
    return fig
