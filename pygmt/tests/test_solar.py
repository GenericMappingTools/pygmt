"""
Test Figure.solar.
"""

import datetime

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.params import Axis


@pytest.mark.mpl_image_compare
def test_solar_terminators():
    """
    Test passing the solar argument with a time string and no terminator type to confirm
    the default terminator type.
    """
    fig = Figure()
    fig.basemap(region="d", projection="W0/15c", frame=Axis(annot=True))
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


@pytest.mark.benchmark
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
    Test passing the solar argument with the day_night terminator and a datetime string.
    """
    fig = Figure()
    fig.solar(
        region="d",
        projection="W0/15c",
        frame=Axis(annot=True),
        terminator="day_night",
        terminator_datetime=terminator_datetime,
    )
    return fig


@pytest.mark.parametrize(
    ("kwargs", "expected_exception"),
    [
        ({"terminator": "invalid"}, GMTValueError),
        ({"T": "d+d1990-02-17T04:25:00"}, GMTParameterError),
        ({"terminator_datetime": "199A-02-17 04:25:00"}, GMTValueError),
    ],
)
def test_solar_invalid_inputs(kwargs, expected_exception):
    """
    Test if the appropriate error is raised when an invalid
    value is passed.
    """
    fig = Figure()
    with pytest.raises(expected_exception):
        fig.solar(region="d", projection="W0/15c", frame=Axis(annot=True), **kwargs)


@pytest.mark.mpl_image_compare(filename="test_solar_set_terminator_datetime.png")
def test_solar_default_terminator():
    """
    Test passing the solar argument with a time string and no terminator type to confirm
    the default terminator type.
    """
    fig = Figure()
    fig.solar(
        region="d",
        projection="W0/15c",
        frame=Axis(annot=True),
        terminator_datetime="1990-02-17 04:25:00",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_solar_terminator_datetime_timezone():
    """
    Test passing the terminator_datetime argument with a time string that includes a
    timezone.
    """
    fig = Figure()
    fig.basemap(region="d", projection="W0/15c", frame=True)
    fig.solar(terminator_datetime="2020-01-01T01:02:03", pen="1p,black")
    fig.solar(terminator_datetime="2020-01-01T01:02:03+01:00", pen="1p,red")
    fig.solar(terminator_datetime="2020-01-01T01:02:03-01:00", pen="1p,blue")
    fig.solar(
        terminator_datetime=datetime.datetime(
            2020, 1, 1, 1, 2, 3, tzinfo=datetime.timezone(datetime.timedelta(hours=2))
        ),
        pen="1p,lightred",
    )
    fig.solar(
        terminator_datetime=datetime.datetime(
            2020, 1, 1, 1, 2, 3, tzinfo=datetime.timezone(datetime.timedelta(hours=-2))
        ),
        pen="1p,lightblue",
    )
    return fig
