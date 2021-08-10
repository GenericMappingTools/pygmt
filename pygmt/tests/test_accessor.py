"""
Test the behaviour of the GMTDataArrayAccessor class.
"""
import pytest
import xarray as xr
from pygmt import which
from pygmt.exceptions import GMTInvalidInput


def test_accessor_gridline_cartesian():
    """
    Check that a grid returns a registration value of 0 when Gridline
    registered, and a gtype value of 1 when using Geographic coordinates.
    """
    fname = which(fname="@test.dat.nc", download="a")
    grid = xr.open_dataarray(fname)
    assert grid.gmt.registration == 0  # gridline registration
    assert grid.gmt.gtype == 0  # cartesian coordinate type


def test_accessor_pixel_geographic():
    """
    Check that a grid returns a registration value of 1 when Pixel registered,
    and a gtype value of 0 when using Cartesian coordinates.
    """
    fname = which(fname="@earth_relief_01d_p", download="a")
    grid = xr.open_dataarray(fname, engine="netcdf4")
    assert grid.gmt.registration == 1  # pixel registration
    assert grid.gmt.gtype == 1  # geographic coordinate type


def test_accessor_set_pixel_registration():
    """
    Check that we can set a grid to be Pixel registered with a registration
    value of 1.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    assert grid.gmt.registration == 0  # default to gridline registration
    grid.gmt.registration = 1  # set to pixel registration
    assert grid.gmt.registration == 1  # ensure changed to pixel registration


def test_accessor_set_geographic_cartesian_roundtrip():
    """
    Check that we can set a grid to switch between the default Cartesian
    coordinate type using a gtype of 1, set it to Geographic 0, and then back
    to Cartesian again 1.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])
    assert grid.gmt.gtype == 0  # default to cartesian coordinate type
    grid.gmt.gtype = 1  # set to geographic type
    assert grid.gmt.gtype == 1  # ensure changed to geographic coordinate type
    grid.gmt.gtype = 0  # set back to cartesian type
    assert grid.gmt.gtype == 0  # ensure changed to cartesian coordinate type


def test_accessor_set_non_boolean():
    """
    Check that setting non boolean values on registration and gtype do not
    work.
    """
    grid = xr.DataArray(data=[[0.1, 0.2], [0.3, 0.4]])

    with pytest.raises(GMTInvalidInput):
        grid.gmt.registration = "2"

    with pytest.raises(GMTInvalidInput):
        grid.gmt.gtype = 2
