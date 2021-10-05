"""
Tests for solar.
"""
import datetime

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_solar_terminators():
    """
    Test passing the solar argument with a time string and no terminator type
    to confirm the default terminator type.
    """
    fig = Figure()
    fig.basemap(region="d", projection="W0/15c", frame="a")
    fig.solar(
        terminator="d",
        pen="1p,blue",
        terminator_datetime="1990-02-17 04:25:00",
    )
    fig.solar(
        terminator="a",
        pen="1p,red",
        terminator_datetime="1990-02-17 04:25:00",
    )
    fig.solar(
        terminator="c",
        pen="1p,green",
        terminator_datetime="1990-02-17 04:25:00",
    )
    fig.solar(
        terminator="n",
        pen="1p,yellow",
        terminator_datetime="1990-02-17 04:25:00",
    )
    return fig


@pytest.mark.mpl_image_compare(filename="test_solar_set_terminator_datetime.png")
@pytest.mark.parametrize(
    "terminator_datetime",
    [
        pytest.param("1990-02-17 04:25:00", id="terminator_datetime_string"),
        datetime.datetime(year=1990, month=2, day=17, hour=4, minute=25, second=0),
    ],
)
def test_solar_set_terminator_datetime(terminator_datetime):
    """
    Test passing the solar argument with the day_night terminator and a
    datetime string.
    """
    fig = Figure()
    fig.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        terminator="day_night",
        terminator_datetime=terminator_datetime,
    )
    return fig


def test_invalid_terminator_type():
    """
    Test if solar fails when it receives an invalid terminator type.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.solar(
            region="d",
            projection="W0/15c",
            frame="a",
            terminator="invalid",
        )


def test_invalid_parameter():
    """
    Test if solar fails when it receives a GMT argument for 'T' instead of the
    PyGMT arguments for 'terminator' and 'terminator_datetime'.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        # Use single-letter option 'T' for testing
        fig.solar(
            region="d", projection="W0/15c", frame="a", T="d+d1990-02-17T04:25:00"
        )


def test_invalid_datetime():
    """
    Test if solar fails when it receives an invalid datetime string.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.solar(
            region="d",
            projection="W0/15c",
            frame="a",
            terminator_datetime="199A-02-17 04:25:00",
        )


@pytest.mark.mpl_image_compare(filename="test_solar_set_terminator_datetime.png")
def test_solar_default_terminator():
    """
    Test passing the solar argument with a time string and no terminator type
    to confirm the default terminator type.
    """
    fig = Figure()
    fig.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        terminator_datetime="1990-02-17 04:25:00",
    )
    return fig
