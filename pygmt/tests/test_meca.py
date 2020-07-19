"""
Tests for meca
"""
import os

import pytest

from .. import Figure


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.mpl_image_compare
def test_meca_spec_dictionary():
    """
    Test supplying a dictionary to the `spec` argument.
    """

    fig = Figure()

    # Right lateral strike slip
    fig.meca(
        dict(strike=0, dip=90, rake=0, magnitude=5),
        lon=0,
        lat=5,
        depth=0,
        scale="2.5c",
        region=[-1, 4, 0, 6],
        projection="M14c",
        frame=2,
    )

    # Left lateral strike slip
    fig.meca(
        dict(strike=0, dip=90, rake=180, magnitude=5),
        lon=2,
        lat=5,
        depth=0,
        scale="2.5c",
    )

    # Thrust
    fig.meca(
        dict(strike=0, dip=45, rake=90, magnitude=5),
        lon=0,
        lat=3,
        depth=0,
        scale="2.5c",
    )
    fig.meca(
        dict(strike=45, dip=45, rake=90, magnitude=5),
        lon=2,
        lat=3,
        depth=0,
        scale="2.5c",
    )

    # Normal
    fig.meca(
        dict(strike=0, dip=45, rake=-90, magnitude=5),
        lon=0,
        lat=1,
        depth=0,
        scale="2.5c",
    )
    fig.meca(
        dict(strike=45, dip=45, rake=-90, magnitude=5),
        lon=2,
        lat=1,
        depth=0,
        scale="2.5c",
    )

    # Mixed
    fig.meca(
        dict(strike=10, dip=35, rake=129, magnitude=5),
        lon=3.4,
        lat=0.6,
        depth=0,
        scale="2.5c",
    )

    return fig
