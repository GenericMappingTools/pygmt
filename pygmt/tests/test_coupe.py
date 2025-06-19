"""
Test Figure.coupe.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from packaging.version import Version
from pygmt import Figure
from pygmt.clib import __gmt_version__
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile

@pytest.mark.mpl_image_compare(filename="test_coupe_spec_single_focalmech.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha", "dict_full", "array1d", "pandas"])
def test_coupe_spec_single_focalmecha(inputtype):
    """
    Test passing a single focal mechanism to the spec parameter.
    Original script: https://github.com/GenericMappingTools/gmt-for-geodesy/blob/main/05_seismology/beachball-cross-section.sh
    """
    if inputtype == "dict_mecha":
        args = {
            "spec": {"strike": 30, "dip": 90, "rake": 0, "magnitude": 4},
            "longitude": 112,
            "latitude": 32,
            "depth": 25,
        }

    elif inputtype == "dict_full":
        args = {
            "spec": {
                "longitude": 112,
                "latitude": 32,
                "depth": 25,
                "strike": 30,
                "dip": 90,
                "rake": 0,
                "magnitude": 4,
            }
        }
    elif inputtype == "array1d":
        args = {
            "spec": np.array([112, 32, 25, 30, 90, 0, 4]),
            "convention": "aki",
        }
    elif inputtype == "pandas":
        args = {
            "spec": pd.DataFrame(
                {
                    "longitude": 112,
                    "latitude": 32,
                    "depth": 25,
                    "strike": 30,
                    "dip": 90,
                    "rake": 0,
                    "magnitude": 4,
                },
                index=[0],
            )
        }
    fig = Figure()
    fig.basemap(region=[111, 113, 31.5, 32.5], projection="M8c", frame=True)
    fig.meca(scale="2.5c", **args)
    fig.shift_origin(yshift="5.5c")
    fig.basemap(region=[0, 1000, 0, 30], projection="X8c/-4c", frame=True)
    fig.coupe(
        scale="2.5c",
        section=[110, 33, 120, 33],
        section_format="lonlat_lonlat",
        no_file=True,
        **args
    )

    return fig
    
@pytest.mark.mpl_image_compare(filename="test_coupe_spec_single_focalmech.png")
def test_coupe_spec_single_focalmecha_file():
    """
    Test supplying a file containing focal mechanisms and locations to the spec
    parameter.
    """
    fig = Figure()
    fig.basemap(region=[111, 113, 31.5, 32.5], projection="M8c", frame=True)
    with GMTTempFile() as temp:
        Path(temp.name).write_text("112 32 25 30 90 0 4", encoding="utf-8")
        fig.meca(spec=temp.name, convention="aki", scale="2.5c")
    fig.shift_origin(yshift="5.5c")
    fig.basemap(region=[0, 1000, 0, 30], projection="X8c", frame=True)
    with GMTTempFile() as temp:
        Path(temp.name).write_text("112 32 25 30 90 0 4", encoding="utf-8")
        fig.coupe(spec=temp.name, convention="aki", scale="2.5c", no_file=True,
                  section=[110, 33, 120, 33], section_format="lonlat_lonlat")
    return fig

@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_coupe_spec_multiple_focalmecha.png")
@pytest.mark.parametrize(
    "inputtype", ["dict_mecha", "dict_mecha_mixed", "dataframe", "array2d"]
)
def test_coupe_spec_multiple_focalmecha(inputtype):
    """
    Test passing multiple focal mechanisms to the spec parameter.
    """

    if inputtype == "dict_mecha":
        args = {
            "spec": {
                "strike": [30, 30, 30],
                "dip": [90, 60, 60],
                "rake": [0, 90, -90],
                "magnitude": [4, 5, 6],
            },
            "longitude": [112, 115, 118],
            "latitude": [32, 34, 32],
            "depth": [25, 15, 45],
        }
    elif inputtype == "dict_mecha_mixed":
        args = {
            "spec": {
                "strike": [30, 30, 30],
                "dip": [90, 60, 60],
                "rake": [0, 90, -90],
                "magnitude": [4, 5, 6],
            },
            "longitude": np.array([112, 115, 118]),
            "latitude": [32, 34, 32],
            "depth": [25, 15, 45],
        }
    elif inputtype == "dataframe":
        args = {
            "spec": pd.DataFrame(
                data={
                    "strike": [30, 30, 30],
                    "dip": [90, 60, 60],
                    "rake": [0, 90, -90],
                    "magnitude": [4, 5, 6],
                    "longitude": [112, 115, 118],
                    "latitude": [32, 34, 32],
                    "depth": [25, 15, 45],
                },
            )
        }
    elif inputtype == "array2d":
        args = {
            "spec": np.array(
                [
                    [112, 32, 25, 30, 90, 0, 4],
                    [115, 34, 15, 30, 60, 90, 5],
                    [118, 32, 45, 30, 60, -90, 6],
                ]
            ),
            "convention": "aki",
        }

    fig = Figure()
    fig.basemap(region=[110, 120, 31, 35], projection="M8c", frame=True)
    fig.meca(scale="1.5c", **args)
    fig.shift_origin(yshift="5.5c")
    fig.basemap(region=[0, 1000, 0, 60], projection="X8c/-4c", frame=True)
    fig.coupe(
        scale="1.5c",
        section=[110, 33, 120, 33],
        section_format="lonlat_lonlat",
        no_file=True,
        **args
    )
    return fig

# TODO(GMT>=6.5.0): Remove the skipif marker for GMT>=6.5.0.
# Passing event names via pandas doesn't work for GMT<=6.4.
# See https://github.com/GenericMappingTools/pygmt/issues/2524.
@pytest.mark.mpl_image_compare(filename="test_coupe_eventname.png")
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
def test_coupe_eventname(inputtype):
    """
    Test passing event names.
    """
    if inputtype == "args":
        args = {
            "spec": {"strike": 30, "dip": 90, "rake": 0, "magnitude": 4},
            "longitude": 112,
            "latitude": 32,
            "depth": 25,
            "event_name": "Strike-slip"
        }
    elif inputtype == "dataframe":
        # Test pandas.DataFrame input. Requires GMT>=6.5.
        # See https://github.com/GenericMappingTools/pygmt/issues/2524.
        # The numeric columns must be in float type to trigger the bug.
        args = {
            "spec": pd.DataFrame(
                {
                    "longitude": [112],
                    "latitude": [32],
                    "depth": [25],
                    "strike": [30],
                    "dip": [90],
                    "rake": [0],
                    "magnitude": [4],
                    "event_name": ["Strike-slip"]
                },
                index=[0],
            )
        }
    fig = Figure()
    fig.basemap(region=[111, 113, 31.5, 32.5], projection="M8c", frame=True)
    fig.meca(scale="1.5c", **args)
    fig.shift_origin(yshift="5.5c")
    fig.basemap(region=[0, 1000, 0, 30], projection="X8c/-4c", frame=True)
    fig.coupe(
            scale="1.5c",
            section=[110, 33, 120, 33],
            section_format="lonlat_lonlat",
            no_file=True,
            **args
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_coupe_vertical_profile.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha"])
def test_coupe_vertical_profile(inputtype):
    """
    Test passing vertical profile.
    See example of https://docs.gmt-china.org/6.1/module/coupe/
    """

    if inputtype == "dict_mecha":
        args = {
            "spec": {
                "mrr": [1.14, 6.19, 0.95, -2.49],
                "mtt": [-0.10, -1.14, 0.11, 3.40],
                "mff": [-1.04, -5.05, -1.06, -0.91],
                "mrt": [-0.51, -0.72, -0.20, 3.09],
                "mrf": [-2.21, -9.03, -2.32, 0.83],
                "mtf": [-0.99, -4.24, 0.90, -3.64],
                "exponent": [26, 25, 25, 25]
            },
            "longitude": [131.55, 133.74, 135.52, 138.37],
            "latitude": [41.48, 41.97, 37.64, 42.85],
            "depth": [579, 604, 432, 248],
        }

    fig = Figure()
    fig.coupe(
        projection="X15c/-6c",
        scale="0.8",
        section=[130, 43, 140, 36, 90, 100, 0, 700, "+f"],
        section_format="lonlat_lonlat",
        component="dc",
        no_clip=True,
        no_file=True,
        **args
    )
    fig.basemap(frame=True)

    return fig

@pytest.mark.mpl_image_compare(filename="test_coupe_PT_axis.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha"])
def test_coupe_PT_axis(inputtype):
    """
    Test plotting P and T axis with W-E cross-section.
    See example of https://docs.gmt-china.org/5.4/module/pscoupe/
    """

    if inputtype == "dict_mecha":
        args = {
            "spec": {"strike1": [0], "dip1": [90], "rake1": [0],
                     "strike2": [90], "dip2": [90], "rake2": [180],
                     "mantissa": [1], "exponent": [24]},
            "longitude": [129.5],
            "latitude": [10.5],
            "depth": [10]
        }
    fig = Figure()
    fig.coupe(
        projection="X1.5c/-1.5c",
        scale="0.4c",
        section=[128, 11, 130, 11, 10, 60, 0, 100, "+f"],
        section_format="lonlat_lonlat",
        pt_axes=True,
        no_clip=True,
        no_file=True,
        **args
    )
    fig.basemap(frame=True)

    return fig   

