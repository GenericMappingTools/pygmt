"""
Tests for meca
"""
import os

import pytest

from .. import Figure


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.mpl_image_compare
def test_meca_full_moment_tensor():
    """
    Check full moment tensor, especially with big isotropic components. The
    data files and original script are provided by Carl Tape, available from
    https://github.com/carltape/compearth, licensed under MIT license. Also see
    https://github.com/GenericMappingTools/gmt/issues/661.
    """

    fig = Figure()

    for file in (
        "fullmt_ipts1_iref1",
        "fullmt_ipts1_iref2",
        "fullmt_ipts1_iref3",
        "fullmt_ipts1_iref4",
        "fullmt_ipts1_iref5",
        "fullmt_ipts2_iref3",
    ):

        fig.basemap(
            region=[-30, 30, -90, 90], projection="H0/2.8i", frame=["g10", "+g200"]
        )
        fig.meca(
            os.path.join(TEST_DATA_DIR, file),
            scale="0.45i",
            convention="mt",
            L="0.5p",
            G="red",
            N=True,
        )
        fig.shift_origin(xshift="3.5i")

    return fig


@pytest.mark.mpl_image_compare
def test_meca_mt_components():
    """
    Check meca `component` argument with `convention="mt". This is equivalent
    to `-Sm`, `-Sz` and `-Sd`. The data files and original script are provided
    by Carl Tape, available from https://github.com/carltape/compearth,
    licensed under MIT license. Also see
    https://github.com/GenericMappingTools/gmt/pull/2135.
    """

    fig = Figure()

    for component in "full", "deviatoric", "dc":

        fig.basemap(region=[-30, 30, -90, 90], projection="H0/2.8i", frame="g10")
        fig.meca(
            os.path.join(TEST_DATA_DIR, "fullmt_ipts1_iref1"),
            scale="0.45i",
            convention="mt",
            component=component,
            L="0.5p",
            G="red",
            N=True,
        )
        fig.shift_origin(xshift="3.5i")

    return fig


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
