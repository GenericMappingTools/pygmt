"""
Test pygmt.sphdistance.
"""

import numpy as np
import numpy.testing as npt
import pytest
from pygmt import sphdistance
from pygmt.clib import Session
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTParameterError


@pytest.fixture(scope="module", name="array")
def fixture_array():
    """
    Load the table data.
    """
    coords_list = [[85.5, 22.3], [82.3, 22.6], [85.8, 22.4], [86.5, 23.3]]
    return np.array(coords_list)


def test_sphdistance_xy_inputs():
    """
    Test inputs using separate xy arguments.
    """
    y = [22.3, 22.6, 22.4, 23.3]
    x = [85.5, 82.3, 85.8, 86.5]
    temp_grid = sphdistance(x=x, y=y, spacing=[1, 2], region=[82, 87, 22, 24])
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype is GridType.GEOGRAPHIC
    assert temp_grid.gmt.registration is GridRegistration.GRIDLINE
    npt.assert_allclose(temp_grid.max(), 232977.546875)
    npt.assert_allclose(temp_grid.min(), 0)
    npt.assert_allclose(temp_grid.median(), 0)
    npt.assert_allclose(temp_grid.mean(), 62469.17)


def test_sphdistance_outgrid(array, tmp_path):
    """
    Test sphdistance with a set outgrid.
    """
    outgrid = tmp_path / "voronoi cell's grid.nc"
    result = sphdistance(
        data=array, outgrid=outgrid, spacing=[1, 1], region=[82, 87, 22, 24]
    )
    assert result is None
    assert outgrid.stat().st_size > 0


@pytest.mark.benchmark
def test_sphdistance_no_outgrid(array):
    """
    Test sphdistance with no set outgrid.
    """
    temp_grid = sphdistance(data=array, spacing=[1, 2], region=[82, 87, 22, 24])
    assert temp_grid.dims == ("lat", "lon")
    assert temp_grid.gmt.gtype is GridType.GEOGRAPHIC
    assert temp_grid.gmt.registration is GridRegistration.GRIDLINE
    npt.assert_allclose(temp_grid.max(), 232977.546875)
    npt.assert_allclose(temp_grid.min(), 0)
    npt.assert_allclose(temp_grid.median(), 0)
    npt.assert_allclose(temp_grid.mean(), 62469.17)


@pytest.mark.parametrize("with_node_table", [False, True])
def test_sphdistance_voronoi(array, tmp_path, with_node_table):
    """
    Use precomputed Voronoi polygons in place of a coordinate table.
    """
    polygon_name = "voronoi polygons.txt" if with_node_table else "cell's polygons.txt"
    polygons = tmp_path / polygon_name
    nodes = tmp_path / "cell's nodes.txt" if with_node_table else None
    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=array) as vintbl:
            args = [vintbl, "-Qv"]
            if nodes is not None:
                args.extend(["-A", f"-N{nodes}"])
            lib.call_module("sphtriangulate", [*args, f"->{polygons}"])

    expected = sphdistance(data=array, spacing=[1, 1], region=[82, 87, 22, 24])
    actual = sphdistance(
        voronoi=polygons, node_table=nodes, spacing=[1, 1], region=[82, 87, 22, 24]
    )
    assert actual is not None
    assert expected is not None
    assert actual.dims == expected.dims
    for dim in actual.dims:
        npt.assert_array_equal(actual.coords[dim], expected.coords[dim])
    npt.assert_allclose(actual, expected, rtol=1e-6)


def test_sphdistance_fails(array):
    """
    Check that sphdistance fails correctly when neither increment nor region is given.
    """
    with pytest.raises(GMTParameterError):
        sphdistance(data=array)
