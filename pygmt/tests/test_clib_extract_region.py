"""
Test the Session.extract_region function.
"""

import numpy as np
import numpy.testing as npt
import pytest
from pygmt import Figure, clib
from pygmt.exceptions import GMTCLibError


def test_extract_region_fails():
    """
    Check that extract region fails if nothing has been plotted.
    """
    Figure()
    with pytest.raises(GMTCLibError):
        with clib.Session() as lib:
            lib.extract_region()


def test_extract_region_two_figures():
    """
    Extract region should handle multiple figures existing at the same time.
    """
    # Make two figures before calling extract_region to make sure that it's
    # getting from the current figure, not the last figure.
    fig1 = Figure()
    region1 = np.array([0, 10, -20, -10])
    fig1.coast(region=region1, projection="M6i", frame=True, land="black")

    fig2 = Figure()
    fig2.basemap(region="US.HI+r5", projection="M6i", frame=True)

    # Activate the first figure and extract the region from it
    # Use in a different session to avoid any memory problems.
    with clib.Session() as lib:
        lib.call_module("figure", [fig1._name, "-"])
    with clib.Session() as lib:
        wesn1 = lib.extract_region()
        npt.assert_allclose(wesn1, region1)

    # Now try it with the second one
    with clib.Session() as lib:
        lib.call_module("figure", [fig2._name, "-"])
    with clib.Session() as lib:
        wesn2 = lib.extract_region()
        npt.assert_allclose(wesn2, np.array([-165.0, -150.0, 15.0, 25.0]))
