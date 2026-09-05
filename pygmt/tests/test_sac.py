"""
Test Figure.sac.
"""

from pathlib import Path

import pytest
from packaging.version import Version
from pygmt import Figure
from pygmt.clib import __gmt_version__

SAC_DATA = Path(__file__).parent / "data" / "seis.sac"

# TODO(GMT>6.7.0): Remove the xfail marker when the minimum GMT version is 6.7.0.
XFAIL_GMT_LE_6_6 = pytest.mark.xfail(
    condition=Version(__gmt_version__) <= Version("6.6.0"),
    reason="The sac module was added in GMT 6.7.0.",
)


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac():
    """
    Plot a single SAC waveform on a linear time plot.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=["xaf+lTime (s)", "yaf+lAmplitude", "WSen"],
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_multiple_traces():
    """
    Plot multiple SAC waveforms on a trace number profile.
    """
    fig = Figure()
    fig.sac(
        data=[SAC_DATA, SAC_DATA],
        # Plot two traces on a trace number profile, i.e., the y positions of the
        # two traces are 0 and 1, respectively. The data amplitude is ~±1.6, so
        # the region is set with some margins.
        region=[9, 20, -0.5, 3],
        projection="X15c/5c",
        frame=True,
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_time_window():
    """
    Plot a SAC waveform in a given time window.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        time_window=[10, 18],
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_time_window_bare():
    """
    Plot a SAC waveform in the time window determined by the region.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        time_window=True,
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_fill_positive_negative():
    """
    Plot a SAC waveform with the positive and negative portions filled.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        positive_fill="black",
        negative_fill="red",
        preprocess="r",
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=True,
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_offset():
    """
    Plot SAC waveforms with an offset.
    """
    fig = Figure()
    fig.sac(
        data=[SAC_DATA, SAC_DATA],
        # Offset the two traces (at y positions 0 and 1) by dy=1, so the y range
        # of the traces becomes 1 and 2, respectively. The data amplitude is
        # ~±1.6, so the region is set with some margins.
        offset=[0, 1],
        region=[9, 20, -1, 4],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_fill():
    """
    Plot a SAC waveform with the positive portion filled.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        positive_fill="gray",
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_amplitude_scale():
    """
    Plot a SAC waveform with vertical scaling.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        amplitude_scale="1.5c",
        region=[9, 20, -4, 4],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_profile():
    """
    Plot a SAC waveform on a trace number profile.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        trace_number=1,
        region=[9, 20, -1, 3],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_preprocess():
    """
    Plot a SAC waveform with the mean removed.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        preprocess="r",
        region=[9, 20, -2, 2],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_vertical():
    """
    Plot a SAC waveform vertically.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        vertical=True,
        region=[-2, 2, 9, 20],
        projection="X5c/15c",
        frame=True,
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_time_scale():
    """
    Plot a SAC waveform on a geographic map with a time scale.
    """
    fig = Figure()
    # The station is at (stlo, stla) = (-120, 48), so the region is extended
    # westward to keep the waveform from sticking to the map boundary.
    fig.basemap(region=[-135, -30, 35, 65], projection="M10c", frame=True)
    fig.sac(
        data=SAC_DATA,
        amplitude_scale="1i",
        # Use the reciprocal time scale, i.e., 0.5 cm per second, so that the
        # 10-s waveform occupies 5 cm on the map.
        time_scale="i0.5c",
        pen="0.5p,red",
    )
    return fig


@XFAIL_GMT_LE_6_6
@pytest.mark.mpl_image_compare
def test_sac_time_options():
    """
    Plot a SAC waveform with time alignment, shift, and reduction velocity.
    """
    fig = Figure()
    fig.sac(
        data=SAC_DATA,
        reduction_velocity=8,
        time_shift=2,
        time_reference="o",
        region=[5, 18, -2, 2],
        projection="X15c/5c",
        frame=True,
        pen="0.5p,red",
    )
    return fig
