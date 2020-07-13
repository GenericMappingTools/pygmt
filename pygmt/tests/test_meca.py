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
