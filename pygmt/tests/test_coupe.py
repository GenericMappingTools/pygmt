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
    fig.coupe(scale="2.5c", section=[110, 33, 120, 33], section_format='lonlat_lonlat', **args)

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
        fig.coupe(spec=temp.name,  convention="aki", scale="2.5c", 
                  section=[110, 33, 120, 33], section_format='lonlat_lonlat')
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
    fig.coupe(scale="1.5c", section=[110, 33, 120, 33], section_format='lonlat_lonlat', **args)
    return fig
