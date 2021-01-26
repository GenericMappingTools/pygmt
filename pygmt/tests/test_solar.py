"""
Tests for solar.
"""
from pygmt import Figure
from pygmt.helpers.testing import check_figures_equal


@check_figures_equal()
def test_solar_day_night():
    """
    Test passing the solar argument with the day_night argument and confirm the
    working aliases for the solar function.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(
        R="d",
        J="W0/15c",
        B="a",
        Td="+d1990-02-17T04:25:00",
        G="navyblue@75",
        W="1p,red,-.-",
        X=3,
        Y=5,
        p="135/45",
    )
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        day_night="+d1990-02-17T04:25:00",
        fill="navyblue@75",
        pen="1p,red,-.-",
        xshift=3,
        yshift=5,
        perspective=[135, 45],
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_civil_twilight():
    """
    Test passing the solar argument with the civil_twilight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Tc="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        civil_twilight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_astronomical_twilight():
    """
    Test passing the solar argument with the astronomical_twilight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Ta="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        astronomical_twilight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test


@check_figures_equal()
def test_solar_nautical_twilight():
    """
    Test passing the solar argument with the nautical_twilight argument.
    """
    fig_ref, fig_test = Figure(), Figure()
    # Use single-character arguments for the reference image
    fig_ref.solar(R="d", J="W0/15c", B="a", Tn="+d1990-02-17T04:25:00")
    fig_test.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        nautical_twilight="+d1990-02-17T04:25:00",
    )
    return fig_ref, fig_test
