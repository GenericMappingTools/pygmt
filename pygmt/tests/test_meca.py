"""
Test Figure.meca.
"""
import numpy as np
import pandas as pd
import pytest
from packaging.version import Version
from pygmt import Figure, __gmt_version__
from pygmt.exceptions import GMTInvalidInput
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
@pytest.mark.parametrize(
    "inputtype", ["dict_mecha", "dict_mecha_mixed", "dataframe", "array2d"]
)
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
    elif inputtype == "dict_mecha_mixed":
        args = {
            "spec": {
                "strike": [330, 350],
                "dip": [30, 50],
                "rake": [90, 90],
                "magnitude": [3, 2],
            },
            "longitude": np.array([-123.5, -124.5]),
            "latitude": [47.5, 48.5],
            "depth": [12, 11],
        }
    elif inputtype == "dataframe":
        args = {
            "spec": pd.DataFrame(
                data={
                    "strike": [330, 350],
                    "dip": [30, 50],
                    "rake": [90, 90],
                    "magnitude": [3, 2],
                    "longitude": [-123.5, -124.5],
                    "latitude": [47.5, 48.5],
                    "depth": [12.0, 11.0],
                },
            )
        }
    elif inputtype == "array2d":
        args = {
            "spec": np.array(
                [
                    [-123.5, 47.5, 12.0, 330, 30, 90, 3],
                    [-124.5, 48.5, 11.0, 350, 50, 90, 2],
                ]
            ),
            "convention": "aki",
        }

    fig = Figure()
    fig.basemap(region=[-125, -122, 47, 49], projection="M8c", frame=True)
    fig.meca(scale="2c", **args)
    return fig


@pytest.mark.mpl_image_compare(filename="test_meca_offset.png")
@pytest.mark.parametrize(
    "inputtype",
    [
        "args",
        "dict",
        pytest.param(
            "ndarray",
            marks=pytest.mark.skipif(
                condition=Version(__gmt_version__) < Version("6.5.0"),
                reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/7557",
            ),
        ),
    ],
)
def test_meca_offset(inputtype):
    """
    Test offsetting beachballs.
    """
    if inputtype == "args":
        args = {
            "spec": {"strike": 330, "dip": 30, "rake": 90, "magnitude": 3},
            "longitude": -124,
            "latitude": 48,
            "depth": 12.0,
            "plot_longitude": -124.5,
            "plot_latitude": 47.5,
        }
    elif inputtype == "dict":
        # Test https://github.com/GenericMappingTools/pygmt/issues/2016
        # offset parameters are in the dict.
        args = {
            "spec": {
                "strike": 330,
                "dip": 30,
                "rake": 90,
                "magnitude": 3,
                "plot_longitude": -124.5,
                "plot_latitude": 47.5,
            },
            "longitude": -124,
            "latitude": 48,
            "depth": 12.0,
        }
    elif inputtype == "ndarray":
        # Test ndarray input reported in
        # https://github.com/GenericMappingTools/pygmt/issues/2016
        args = {
            "spec": np.array([[-124, 48, 12.0, 330, 30, 90, 3, -124.5, 47.5]]),
            "convention": "aki",
        }

    fig = Figure()
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(scale="1c", **args)
    return fig


# Passing event names via pandas doesn't work for GMT<=6.4, thus marked as
# xfail. See https://github.com/GenericMappingTools/pygmt/issues/2524.
@pytest.mark.mpl_image_compare(filename="test_meca_eventname.png")
@pytest.mark.parametrize(
    "inputtype",
    [
        "args",
        pytest.param(
            "dataframe",
            marks=pytest.mark.skipif(
                condition=Version(__gmt_version__) < Version("6.5.0"),
                reason="Upstream bug fixed in https://github.com/GenericMappingTools/gmt/pull/7557",
            ),
        ),
    ],
)
def test_meca_eventname(inputtype):
    """
    Test passing event names.
    """
    if inputtype == "args":
        args = {
            "spec": {"strike": 330, "dip": 30, "rake": 90, "magnitude": 3},
            "longitude": -124,
            "latitude": 48,
            "depth": 12.0,
            "event_name": "Event20220311",
        }
    elif inputtype == "dataframe":
        # Test pandas.DataFrame input. Requires GMT>=6.5.
        # See https://github.com/GenericMappingTools/pygmt/issues/2524.
        # The numeric columns must be in float type to trigger the bug.
        args = {
            "spec": pd.DataFrame(
                {
                    "longitude": [-124.0],
                    "latitude": [48.0],
                    "depth": [12.0],
                    "strike": [330.0],
                    "dip": [30.0],
                    "rake": [90.0],
                    "magnitude": [3.0],
                    "event_name": ["Event20220311"],
                }
            )
        }
    fig = Figure()
    fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
    fig.meca(scale="1c", **args)
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


@pytest.mark.mpl_image_compare(filename="test_meca_eventname.png")
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
        scale=1.0,  # make sure a non-str scale works
    )
    return fig


def test_meca_spec_ndarray_no_convention():
    """
    Raise an exception if convention is not given for an ndarray input.
    """
    with pytest.raises(GMTInvalidInput):
        fig = Figure()
        fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
        fig.meca(spec=np.array([[-124, 48, 12.0, 330, 30, 90, 3]]), scale="1c")


def test_meca_spec_ndarray_mismatched_columns():
    """
    Raise an exception if the ndarray input doesn't have the expected number of
    columns.
    """
    with pytest.raises(GMTInvalidInput):
        fig = Figure()
        fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
        fig.meca(
            spec=np.array([[-124, 48, 12.0, 330, 30, 90]]), convention="aki", scale="1c"
        )

    with pytest.raises(GMTInvalidInput):
        fig = Figure()
        fig.basemap(region=[-125, -122, 47, 49], projection="M6c", frame=True)
        fig.meca(
            spec=np.array([[-124, 48, 12.0, 330, 30, 90, 3, -124.5, 47.5, 30.0, 50.0]]),
            convention="aki",
            scale="1c",
        )
