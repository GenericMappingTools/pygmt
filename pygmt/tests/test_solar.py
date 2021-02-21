"""
Tests for solar.
"""
import datetime

from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_solar_default_terminator_string_datetime():
    """
    Test passing the solar argument with the day_night argument and confirm the
    working aliases for the solar function.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", T="d+d1990-02-17T04:25:00")
    fig_test.solar(R="d", J="W0/15c", B="a", terminator_datetime="1990-02-17 04:25:00")
    return fig_ref, fig_test
