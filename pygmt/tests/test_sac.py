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
