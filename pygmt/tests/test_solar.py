"""
Tests for solar.
"""
import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_solar_day_night():
    """
    Test passing the solar argument with the day_night argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Td="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d", projection="W0/15c", frame="a", day_night="+d1990-02-17T04:25:00"
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_civil_twighlight():
    """
    Test passing the solar argument with the civil_twighlight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Tc="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        civil_twighlight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_astronomical_twighlight():
    """
    Test passing the solar argument with the astronomical_twighlight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Ta="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        astronomical_twighlight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_nautical_twighlight():
    """
    Test passing the solar argument with the nautical_twighlight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Tn="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        nautical_twighlight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_fill():
    """
    Test plotting solar terminator and night-area fill on top of a coast
    figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00", G="navyblue")
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00", fill="navyblue")
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_fill_transparency():
    """
    Test plotting solar terminator and night-area fill with a transparency
    modifier on top of a coast figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00", G="navyblue@75")
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00", fill="navyblue@75")
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_pen():
    """
    Test plotting solar terminator and setting a pen on top of a coast figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00", W="1p,red,-.-")
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00", pen="1p,red,-.-")
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_xy_shift():
    """
    Test plotting solar terminator with an x-y shift on top of a coast figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00", X=3, Y=5)
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00", xshift=3, yshift=5)
    return fig_ref, fig_test

@check_figures_equal()
def test_solar_perspective():
    """
    Test plotting solar terminator with a perspective shift on top of a coast figure.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.coast(R="d", J="W0/15c", G="darkgreen", S="lightblue")
    fig_ref.solar(Td="+d1990-02-17T04:27:00", p="135/45")
    fig_test.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
    fig_test.solar(day_night="+d1990-02-17T04:27:00", perspective=[135, 45])
    return fig_ref, fig_test
