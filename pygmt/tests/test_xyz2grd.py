"""
Tests for xyz2grd.
"""
import xarray as xr
from pygmt import xyz2grd


def test_xyz2grd_input_file():
    """
    Run xyz2grd by passing in a filename.
    """
    output = xyz2grd("@tut_ship.xyz", spacing=5, region=[245, 255, 20, 30])
    assert isinstance(output, xr.DataArray)
    assert output.gmt.registration == 0  # Gridline registration
    assert output.gmt.gtype == 0  # Cartesian type
    return output
