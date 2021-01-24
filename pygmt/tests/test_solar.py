"""
Tests for solar.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_solar():
    """
    Test passing only the solar argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", Td="+d1990-02-17T04:25:00")
    fig_test.solar(region="d", projection="W0/15c", day_night="+d1990-02-17T04:25:00")
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_coast():
    """
    Test plotting solar terminator on top of a coast figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00")
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00")
    return fig_ref, fig_test
