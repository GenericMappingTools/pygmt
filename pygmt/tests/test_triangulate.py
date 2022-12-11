"""
Tests for triangulate.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pygmt import triangulate, which
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile, data_kind


@pytest.fixture(scope="module", name="dataframe")
def fixture_dataframe():
    """
    Load the table data from the sample bathymetry dataset.
    """
    fname = which("@Table_5_11_mean.xyz", download="c")
    return pd.read_csv(
        fname, sep=r"\s+", header=None, names=["x", "y", "z"], skiprows=1
    )[:10]


@pytest.fixture(scope="module", name="expected_dataframe")
def fixture_expected_dataframe():
    """
    Load the expected triangulate dataframe result.
    """
    return pd.DataFrame(
        data=[
            [7, 8, 2],
            [8, 7, 9],
            [7, 1, 0],
            [1, 7, 2],
            [1, 2, 4],
            [8, 3, 2],
            [9, 5, 3],
            [5, 9, 6],
            [5, 4, 3],
            [4, 5, 6],
            [4, 6, 1],
            [3, 4, 2],
            [9, 3, 8],
        ]
    )


@pytest.fixture(scope="module", name="expected_grid")
def fixture_expected_grid():
    """
    Load the expected triangulate grid result.
    """
    return xr.DataArray(
        data=[[779.6264, 752.1539, 749.38776], [771.2882, 726.9792, 722.1368]],
        coords=dict(y=[5, 6], x=[2, 3, 4]),
        dims=["y", "x"],
    )


@pytest.mark.parametrize("array_func", [np.array, xr.Dataset])
def test_delaunay_triples_input_table_matrix(array_func, dataframe, expected_dataframe):
    """
    Run triangulate.delaunay_triples by passing in a numpy.array or
    xarray.Dataset.
    """
    table = array_func(dataframe)
    output = triangulate.delaunay_triples(data=table)
    pd.testing.assert_frame_equal(left=output, right=expected_dataframe)


def test_delaunay_triples_input_xyz(dataframe, expected_dataframe):
    """
    Run triangulate.delaunay_triples by passing in x, y, z numpy.ndarrays
    individually.
    """
    output = triangulate.delaunay_triples(x=dataframe.x, y=dataframe.y, z=dataframe.z)
    pd.testing.assert_frame_equal(left=output, right=expected_dataframe)


def test_delaunay_triples_input_xy_no_z(dataframe, expected_dataframe):
    """
    Run triangulate.delaunay_triples by passing in x and y, but no z.
    """
    output = triangulate.delaunay_triples(x=dataframe.x, y=dataframe.y)
    pd.testing.assert_frame_equal(left=output, right=expected_dataframe)


def test_delaunay_triples_wrong_kind_of_input(dataframe):
    """
    Run triangulate.delaunay_triples using grid input that is not
    file/matrix/vectors.
    """
    data = dataframe.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        triangulate.delaunay_triples(data=data)


def test_delaunay_triples_ndarray_output(dataframe, expected_dataframe):
    """
    Test triangulate.delaunay_triples with "numpy" output type.
    """
    output = triangulate.delaunay_triples(data=dataframe, output_type="numpy")
    assert isinstance(output, np.ndarray)
    np.testing.assert_allclose(actual=output, desired=expected_dataframe.to_numpy())


def test_delaunay_triples_outfile(dataframe, expected_dataframe):
    """
    Test triangulate.delaunay_triples with ``outfile``.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        with pytest.warns(RuntimeWarning) as record:
            result = triangulate.delaunay_triples(data=dataframe, outfile=tmpfile.name)
            assert len(record) == 1  # check that only one warning was raised
        assert result is None  # return value is None
        assert Path(tmpfile.name).stat().st_size > 0
        temp_df = pd.read_csv(filepath_or_buffer=tmpfile.name, sep="\t", header=None)
        pd.testing.assert_frame_equal(left=temp_df, right=expected_dataframe)


def test_delaunay_triples_invalid_format(dataframe):
    """
    Test that triangulate.delaunay_triples fails with incorrect format.
    """
    with pytest.raises(GMTInvalidInput):
        triangulate.delaunay_triples(data=dataframe, output_type=1)


def test_regular_grid_no_outgrid(dataframe, expected_grid):
    """
    Run triangulate.regular_grid with no set outgrid and see it load into an
    xarray.DataArray.
    """
    data = dataframe.to_numpy()
    output = triangulate.regular_grid(data=data, spacing=1, region=[2, 4, 5, 6])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    xr.testing.assert_allclose(a=output, b=expected_grid)


def test_regular_grid_with_outgrid_param(dataframe, expected_grid):
    """
    Run triangulate.regular_grid with the -Goutputfile.nc parameter.
    """
    data = dataframe.to_numpy()
    with GMTTempFile(suffix=".nc") as tmpfile:
        output = triangulate.regular_grid(
            data=data, spacing=1, region=[2, 4, 5, 6], outgrid=tmpfile.name
        )
        assert output is None  # check that output is None since outgrid is set
        assert Path(tmpfile.name).stat().st_size > 0  # check that outgrid exists
        with xr.open_dataarray(tmpfile.name) as grid:
            assert isinstance(grid, xr.DataArray)
            assert grid.gmt.registration == 0  # Gridline registration
            assert grid.gmt.gtype == 0  # Cartesian type
            xr.testing.assert_allclose(a=grid, b=expected_grid)


def test_regular_grid_invalid_format(dataframe):
    """
    Test that triangulate.regular_grid fails with outgrid that is not None or a
    proper file name.
    """
    with pytest.raises(GMTInvalidInput):
        triangulate.regular_grid(data=dataframe, outgrid=True)
