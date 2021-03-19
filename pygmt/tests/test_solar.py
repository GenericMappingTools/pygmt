"""
Tests for solar.
"""
import datetime

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.mpl_image_compare
def test_solar_set_terminator_datetime_string():
    """
    Test passing the solar argument with the civil terminator and a datetime
    string.
    """
    fig = Figure()
    fig.solar(
        region="d",
        projection="W0/15c",
        frame="a",
        terminator="civil",
        terminator_datetime="1990-02-17 04:25:00",
    )
    return fig


@pytest.mark.mpl_image_compare
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


@pytest.mark.mpl_image_compare
def test_solar_set_terminator_datetime_object():
    """
    Test passing the solar argument with the day_night terminator and a
    datetime string.
    """
    fig = Figure()
    terminator_datetime = datetime.datetime(
        year=1990, month=2, day=17, hour=4, minute=25, second=0
    )
    fig.solar(
        R="d",
        J="W0/15c",
        B="a",
        termiantor="day_night",
        terminator_datetime=terminator_datetime,
    )
    return fig


def test_invalid_terminator_type():
    """
    Test if fig.solar fails when it receives an invalid terminator type.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.solar(
            region="d",
            projection="W0/15c",
            frame="a",
            terminator="invalid",
        )


def test_invalid_T_parameter():
    """
    Test if fig.solar fails when it receives a GMT argument for 'T' instead of
    the PyGMT arguments for 'terminator' and 'terminator_datetime'.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.solar(
            region="d", projection="W0/15c", frame="a", T="d+d1990-02-17T04:25:00"
        )


def test_invalid_datetime():
    """
    Test if fig.solar fails when it receives an invalid datetime string.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.solar(
            region="d",
            projection="W0/15c",
            frame="a",
            terminator_datetime="199A-02-17 04:25:00",
        )
