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

@pytest.mark.mpl_image_compare(filename="test_coupe_one_type.png")
@pytest.mark.parametrize("inputtype", ["dict_mecha", "dict_full", "array1d", "pandas"])
def test_coupe_one_type(inputtype):
    """
    Test passing a single focal mechanism to the spec parameter.
    """
    if inputtype == "dict_mecha":
        args = {
            "spec": {"strike": 30, "dip": 90, "rake": 0, "magnitude": 4},
            "longitude": 0,
            "latitude": 5,
            "depth": 10,
        }
    elif inputtype == "dict_full":
        args = {
            "spec": {
                "longitude": 0,
                "latitude": 5,
                "depth": 10,
                "strike": 30,
                "dip": 90,
                "rake": 0,
                "magnitude": 4,
            }
        }
    elif inputtype == "array1d":
        args = {
            "spec": np.array([0, 5, 10, 0, 30, 0, 4]),
            "convention": "a",
        }
    elif inputtype == "pandas":
        args = {
            "spec": pd.DataFrame(
                {
                    "longitude": 0,
                    "latitude": 5,
                    "depth": 10,
                    "strike": 0,
                    "dip": 30,
                    "rake": 0,
                    "magnitude": 4,
                },
                index=[0],
            )
        }
    fig = Figure()
    fig.basemap(region=[-1, 1, 4, 6], projection="M8c", frame=2)
    fig.meca(scale="2.5c", **args)
    return fig