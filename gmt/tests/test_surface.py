"""
Tests for surface
"""
from .. import surface
from .. import which
from ..datasets import load_tut_ship


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
