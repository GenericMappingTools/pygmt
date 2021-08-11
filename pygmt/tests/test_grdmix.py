"""
Tests for grdmix.
"""
import os

import numpy.testing as npt
import pytest
import xarray as xr
from pygmt import grdmix, which


@pytest.fixture(scope="module", name="grid")
def fixture_grid():
    """
    Load the grid data from the sample earth_day file.
    """
    return which(fname="@earth_day_01d", download="c")


def test_grdmix_deconstruct(grid):
    """
    Test that a 3-band RGB grid can be deconstructed into 3 separate files.
    """
    paths = ["layerR.nc", "layerG.nc", "layerB.nc"]
    try:
        grdmix(grid=grid, outgrid="layer%c.nc", deconstruct=True)
        assert all(os.path.exists(path=path) for path in paths)
        dataarray = xr.concat(
            objs=[xr.open_dataarray(path) for path in paths], dim="band"
        )
        assert dataarray.shape == (3, 180, 360)  # bands, latitude, longitude
        npt.assert_allclose(actual=dataarray.mean(), desired=54.74891)
    finally:
        _ = [os.remove(path=path) for path in paths]
