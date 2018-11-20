"""
Tests for surface
"""
import pytest

from .. import surface
from .. import which
from ..datasets import load_tut_ship
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind


def test_surface_input_file():
    """
    Run surface by passing in a filename
    """
    fname = which("@tut_ship.xyz", download="c")
    outputfile = surface(data=fname, I="5m", R="245/255/20/30")
    return outputfile


def test_surface_input_data_array():
    """
    Run surface by passing in a numpy array into data
    """
    ship_data = load_tut_ship()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    outputfile = surface(data=data, I="5m", R="245/255/20/30")
    return outputfile


def test_surface_input_xyz():
    """
    Run surface by passing in x, y, z numpy.ndarrays individually
    """
    ship_data = load_tut_ship()
    outputfile = surface(
        x=ship_data.x, y=ship_data.y, z=ship_data.z, I="5m", R="245/255/20/30"
    )
    return outputfile


def test_surface_input_xy_no_z():
    """
    Run surface by passing in x and y, but no z
    """
    ship_data = load_tut_ship()
    with pytest.raises(GMTInvalidInput):
        surface(x=ship_data.x, y=ship_data.y, I="5m", R="245/255/20/30")


def test_surface_wrong_kind_of_input():
    """
    Run surface using grid input that is not file/matrix/vectors
    """
    ship_data = load_tut_ship()
    data = ship_data.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, I="5m", R="245/255/20/30")
