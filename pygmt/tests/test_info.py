"""
Tests for gmtinfo.
"""
import os
import pathlib
import sys

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
import xarray as xr
from pygmt import info
from pygmt.exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


def test_info():
    """
    Make sure info works on file name inputs.
    """
    output = info(data=POINTS_DATA)
    expected_output = (
        f"{POINTS_DATA}: N = 20 "
        "<11.5309/61.7074> "
        "<-2.9289/7.8648> "
        "<0.1412/0.9338>\n"
    )
    assert output == expected_output


@pytest.mark.parametrize(
    "table",
    [
        pathlib.Path(POINTS_DATA),
        pytest.param(
            pathlib.PureWindowsPath(POINTS_DATA),
            marks=pytest.mark.skipif(
                sys.platform != "win32",
                reason="PureWindowsPath is only available on Windows",
            ),
        ),
        pytest.param(
            pathlib.PurePosixPath(POINTS_DATA),
            marks=pytest.mark.skipif(
                sys.platform == "win32",
                reason="PurePosixPath is not available on Windows",
            ),
        ),
    ],
)
def test_info_path(table):
    """
    Make sure info works on a pathlib.Path input.
    """
    output = info(data=table)
    expected_output = (
        f"{POINTS_DATA}: N = 20 "
        "<11.5309/61.7074> "
        "<-2.9289/7.8648> "
        "<0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_2d_list():
    """
    Make sure info works on a 2-D list.
    """
    output = info(data=[[0, 8], [3, 5], [6, 2]])
    expected_output = "<vector memory>: N = 3 <0/6> <2/8>\n"
    assert output == expected_output


def test_info_series():
    """
    Make sure info works on a pandas.Series input.
    """
    output = info(pd.Series(data=[0, 4, 2, 8, 6]))
    expected_output = "<vector memory>: N = 5 <0/8>\n"
    assert output == expected_output


def test_info_dataframe():
    """
    Make sure info works on pandas.DataFrame inputs.
    """
    table = pd.read_csv(POINTS_DATA, sep=" ", header=None)
    output = info(data=table)
    expected_output = (
        "<vector memory>: N = 20 <11.5309/61.7074> <-2.9289/7.8648> <0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_numpy_array_time_column():
    """
    Make sure info works on a numpy.ndarray input with a datetime type.
    """
    table = pd.date_range(start="2020-01-01", periods=5).to_numpy()
    output = info(data=table)
    expected_output = (
        "<vector memory>: N = 5 <2020-01-01T00:00:00/2020-01-05T00:00:00>\n"
    )
    assert output == expected_output


def test_info_pandas_dataframe_time_column():
    """
    Make sure info works on pandas.DataFrame inputs with a time column.
    """
    table = pd.DataFrame(
        data={
            "z": [10, 13, 12, 15, 14],
            "time": pd.date_range(start="2020-01-01", periods=5),
        }
    )
    output = info(data=table)
    expected_output = (
        "<vector memory>: N = 5 <10/15> <2020-01-01T00:00:00/2020-01-05T00:00:00>\n"
    )
    assert output == expected_output


def test_info_xarray_dataset_time_column():
    """
    Make sure info works on xarray.Dataset 1-D inputs with a time column.
    """
    table = xr.Dataset(
        coords={"index": [0, 1, 2, 3, 4]},
        data_vars={
            "z": ("index", [10, 13, 12, 15, 14]),
            "time": ("index", pd.date_range(start="2020-01-01", periods=5)),
        },
    )
    output = info(data=table)
    expected_output = (
        "<vector memory>: N = 5 <10/15> <2020-01-01T00:00:00/2020-01-05T00:00:00>\n"
    )
    assert output == expected_output


def test_info_2d_array():
    """
    Make sure info works on 2-D numpy.ndarray inputs.
    """
    table = np.loadtxt(POINTS_DATA)
    output = info(data=table)
    expected_output = (
        "<matrix memory>: N = 20 <11.5309/61.7074> <-2.9289/7.8648> <0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_1d_array():
    """
    Make sure info works on 1-D numpy.ndarray inputs.
    """
    output = info(data=np.arange(20))
    expected_output = "<vector memory>: N = 20 <0/19>\n"
    assert output == expected_output


def test_info_per_column():
    """
    Make sure the per_column parameter works.
    """
    output = info(data=POINTS_DATA, per_column=True)
    npt.assert_allclose(
        actual=output, desired=[11.5309, 61.7074, -2.9289, 7.8648, 0.1412, 0.9338]
    )


def test_info_per_column_with_time_inputs():
    """
    Make sure the per_column parameter works with time inputs.
    """
    table = pd.date_range(start="2020-01-01", periods=5).to_numpy()
    output = info(data=table, per_column=True)
    npt.assert_equal(
        actual=output, desired=["2020-01-01T00:00:00", "2020-01-05T00:00:00"]
    )


def test_info_spacing():
    """
    Make sure the spacing parameter works.
    """
    output = info(data=POINTS_DATA, spacing=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, -3, 7.9])


def test_info_spacing_bounding_box():
    """
    Make sure the spacing parameter for writing a bounding box works.
    """
    output = info(data=POINTS_DATA, spacing="b")
    npt.assert_allclose(
        actual=output,
        desired=[
            [11.5309, -2.9289],
            [61.7074, -2.9289],
            [61.7074, 7.8648],
            [11.5309, 7.8648],
            [11.5309, -2.9289],
        ],
    )


def test_info_per_column_spacing():
    """
    Make sure the per_column and spacing parameters work together.
    """
    output = info(data=POINTS_DATA, per_column=True, spacing=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, -3, 7.9, 0.1412, 0.9338])


def test_info_nearest_multiple():
    """
    Make sure the nearest_multiple parameter works.
    """
    output = info(data=POINTS_DATA, nearest_multiple=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, 0.1])


def test_info_fails():
    """
    Make sure info raises an exception if not given either a file name, pandas
    DataFrame, or numpy ndarray.
    """
    with pytest.raises(GMTInvalidInput):
        info(data=xr.DataArray(21))


def test_incols_for_vector_input():
    """
    Make sure that incols (-i) works for vector input.

    Related to https://github.com/GenericMappingTools/pygmt/issues/1313.
    """
    x = np.arange(0, 10, 1)
    y = np.arange(10, 20, 1)
    data = np.array([x, y]).T

    output = info(data=data, per_column=True)
    npt.assert_allclose(actual=output, desired=[0.0, 9.0, 10.0, 19.0])

    output = info(data=data, per_column=True, incols=[1, 0])
    npt.assert_allclose(actual=output, desired=[10.0, 19.0, 0.0, 9.0])

    output = info(data=data, per_column=True, incols=["1+s2.0", "0+s5.0+o15"])
    npt.assert_allclose(actual=output, desired=[20.0, 38.0, 15.0, 60.0])
