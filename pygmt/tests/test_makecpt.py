"""
Test pygmt.makecpt.
"""

from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pygmt import Figure, makecpt
from pygmt.exceptions import (
    GMTCLibError,
    GMTInvalidInput,
    GMTParameterError,
    GMTValueError,
)
from pygmt.helpers import GMTTempFile

POINTS_DATA = Path(__file__).parent / "data" / "points.txt"


@pytest.fixture(scope="module", name="points")
def fixture_points():
    """
    Load the points data from the test file.
    """
    return np.loadtxt(POINTS_DATA)


@pytest.fixture(scope="module", name="position")
def fixture_position():
    """
    Return a standard position argument for the colorbar.
    """
    return "x0c/0c+w10c+h"


@pytest.mark.mpl_image_compare
def test_makecpt_plot_points(points):
    """
    Use static color palette table to change color of points.
    """
    fig = Figure()
    makecpt(cmap="gmt/rainbow")
    fig.plot(
        x=points[:, 0],
        y=points[:, 1],
        fill=points[:, 2],
        region=[10, 70, -5, 10],
        style="c1c",
        cmap=True,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_plot_colorbar(position):
    """
    Use static color palette table to plot a colorbar.
    """
    fig = Figure()
    makecpt(cmap="gmt/relief")
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_plot_colorbar_scaled_with_series(position):
    """
    Use static color palette table scaled to a min/max series and plot it on a colorbar.
    """
    fig = Figure()
    makecpt(cmap="SCM/oleron", series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.benchmark
def test_makecpt_output_cpt_file():
    """
    Save the generated static color palette table to a .cpt file.
    """
    with GMTTempFile(suffix=".cpt") as cptfile:
        makecpt(output=cptfile.name)
        assert Path(cptfile.name).stat().st_size > 0


@pytest.mark.parametrize(
    ("series", "gmt_series"),
    [
        pytest.param([0, 0.25, 0.9, 2], "0,0.25,0.9,2", id="explicit-list"),
        pytest.param((0, 0.25, 0.9, 2), "0,0.25,0.9,2", id="explicit-tuple"),
        pytest.param(np.array([0, 0.25, 0.9, 2]), "0,0.25,0.9,2", id="explicit-array"),
        pytest.param(
            np.array([0, 0.25, 0.9, 2], dtype=np.dtype("float64").newbyteorder()),
            "0,0.25,0.9,2",
            id="non-native-array",
        ),
        pytest.param(pd.Series([0, 0.25, 0.9, 2]), "0,0.25,0.9,2", id="pandas-series"),
        pytest.param(range(5), "0,1,2,3,4", id="explicit-range"),
        pytest.param(
            [Fraction(0), Fraction(1, 4), Fraction(9, 10), Fraction(2)],
            "0,0.25,0.9,2",
            id="fractions",
        ),
        pytest.param(
            np.ma.array([0, 0.25, 89, 0.9, 2], mask=[0, 0, 1, 0, 0]),
            "0,0.25,0.9,2",
            id="masked-array",
        ),
        pytest.param([0, 2], "0/2", id="two-value-list"),
        pytest.param(np.array([0, 2]), "0/2", id="two-value-array"),
        pytest.param((0, 2, 0.5), "0/2/0.5", id="three-value-tuple"),
        pytest.param(np.array([0, 2, 0.5]), "0/2/0.5", id="three-value-array"),
        pytest.param(
            np.array(["2020-01-01", "2020-01-15"], dtype="datetime64[s]"),
            "2020-01-01T00:00:00/2020-01-15T00:00:00",
            id="datetime-range",
        ),
    ],
)
def test_makecpt_series(tmp_path, series, gmt_series):
    """
    Match GMT's explicit boundaries or range syntax for sequence inputs.
    """
    expected = tmp_path / "expected.cpt"
    actual = tmp_path / "actual.cpt"
    makecpt(cmap="turbo", series=gmt_series, output=str(expected))
    makecpt(cmap="turbo", series=series, output=str(actual))
    assert actual.read_bytes() == expected.read_bytes()


def test_makecpt_series_iterator(tmp_path):
    """
    Match GMT's explicit boundaries for an iterator without a length.
    """
    expected = tmp_path / "expected.cpt"
    actual = tmp_path / "actual.cpt"
    makecpt(cmap="turbo", series="0,0.25,0.9,2", output=expected)
    makecpt(cmap="turbo", series=iter([0, 0.25, 0.9, 2]), output=actual)
    assert actual.read_bytes() == expected.read_bytes()


@pytest.mark.parametrize(
    ("cmap", "continuous"),
    [("red,green,blue", False), ("red,green,blue,white", True)],
)
def test_makecpt_series_with_colors(tmp_path, cmap, continuous):
    """
    Assign the requested colors to the explicit boundaries.
    """
    expected = tmp_path / "expected.cpt"
    actual = tmp_path / "actual.cpt"
    makecpt(cmap=cmap, continuous=continuous, series="0,0.25,0.9,2", output=expected)
    makecpt(cmap=cmap, continuous=continuous, series=[0, 0.25, 0.9, 2], output=actual)
    assert actual.read_bytes() == expected.read_bytes()


def test_makecpt_series_color_count(tmp_path):
    """
    Ask GMT to validate the number of colors for explicit boundaries.
    """
    with pytest.raises(GMTCLibError, match="Mismatch between number of entries"):
        makecpt(
            cmap="red,green,blue,white",
            series=[0, 0.25, 0.9, 2],
            output=tmp_path / "invalid.cpt",
        )


def test_makecpt_long_series(tmp_path):
    """
    Match an input file for a long sequence of color slice boundaries.
    """
    boundaries = np.linspace(0, 1, 4097)
    series_file = tmp_path / "boundaries.txt"
    np.savetxt(series_file, boundaries)
    expected = tmp_path / "expected.cpt"
    actual = tmp_path / "actual.cpt"
    makecpt(cmap="turbo", series=str(series_file), output=str(expected))
    makecpt(cmap="turbo", series=boundaries, output=str(actual))
    assert actual.read_bytes() == expected.read_bytes()


@pytest.mark.parametrize(
    "series",
    [
        pytest.param(np.datetime64("2020-01-01") + np.arange(4), id="datetime-array"),
        pytest.param(
            [
                "2020-01-01T00:00:00",
                "2020-01-03T00:00:00",
                "2020-01-06T00:00:00",
                "2020-01-15T00:00:00",
            ],
            id="iso-strings",
        ),
        pytest.param(
            np.array([0, 0.25, np.complex128(0.9 + 1j), 2], dtype=object),
            id="complex-objects",
        ),
    ],
)
def test_makecpt_nonnumeric_boundaries(tmp_path, series):
    """
    Reject non-real boundaries before passing the sequence to GMT.
    """
    output = tmp_path / "invalid.cpt"
    with pytest.raises(GMTInvalidInput, match="must be finite real numbers"):
        makecpt(cmap="turbo", series=series, output=output)
    assert not output.exists()


@pytest.mark.parametrize(
    ("series", "match"),
    [
        pytest.param(
            np.arange(8).reshape(4, 2),
            "must be one-dimensional",
            id="two-dimensional",
        ),
        pytest.param(
            np.ma.array([0, 0.25, 0.9, 2], mask=[False, True, True, True]),
            "must provide at least two unmasked boundaries",
            id="too-few-unmasked",
        ),
        pytest.param(
            [0, 0.25, 0.9, np.inf],
            "must be finite real numbers",
            id="nonfinite",
        ),
    ],
)
def test_makecpt_invalid_numeric_boundaries(tmp_path, series, match):
    """
    Reject invalid numeric boundaries without writing a CPT.
    """
    output = tmp_path / "invalid.cpt"
    with pytest.raises(GMTInvalidInput, match=match):
        makecpt(cmap="turbo", series=series, output=output)
    assert not output.exists()


def test_makecpt_series_short_alias(tmp_path):
    """
    Accept a sequence through the short-form GMT option.
    """
    expected = tmp_path / "expected.cpt"
    actual = tmp_path / "actual.cpt"
    makecpt(cmap="turbo", series="0,0.25,0.9,2", output=str(expected))
    with pytest.warns(SyntaxWarning, match=r"Short-form parameter \(T\)"):
        makecpt(cmap="turbo", T=[0, 0.25, 0.9, 2], output=str(actual))
    assert actual.read_bytes() == expected.read_bytes()


def test_makecpt_blank_output():
    """
    Use incorrect setting by passing in blank file name to output parameter.
    """
    with pytest.raises(GMTValueError):
        makecpt(output="")


def test_makecpt_invalid_output():
    """
    Use incorrect setting by passing in invalid type to output parameter.
    """
    with pytest.raises(GMTValueError):
        makecpt(output=["some.cpt"])


@pytest.mark.mpl_image_compare
def test_makecpt_truncated_zlow_zhigh(position):
    """
    Use static color palette table that is truncated to z-low and z-high.
    """
    fig = Figure()
    makecpt(cmap="gmt/rainbow", truncate=[0.15, 0.85], series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_only(position):
    """
    Use static color palette table with its colors reversed.
    """
    fig = Figure()
    makecpt(cmap="gmt/earth", reverse=True, series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_reverse_color_and_zsign(position):
    """
    Use static color palette table with both its colors and z-value sign reversed.
    """
    fig = Figure()
    makecpt(cmap="gmt/earth", reverse="cz", series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_continuous(position):
    """
    Use static color palette table that is continuous from blue to white and scaled from
    0 to 1000 m.
    """
    fig = Figure()
    makecpt(cmap="blue,white", continuous=True, series=[0, 1000])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_categorical(position):
    """
    Use static color palette table that is categorical.
    """
    fig = Figure()
    makecpt(cmap="gmt/categorical", categorical=True, series=[0, 6, 1])
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


@pytest.mark.mpl_image_compare
def test_makecpt_cyclic(position):
    """
    Use static color palette table that is cyclic.
    """
    fig = Figure()
    makecpt(cmap="SCM/cork", cyclic=True)
    fig.colorbar(cmap=True, frame=True, position=position)
    return fig


def test_makecpt_categorical_and_cyclic():
    """
    Use incorrect setting by setting both categorical and cyclic to True.
    """
    with pytest.raises(GMTParameterError):
        makecpt(cmap="SCM/batlow", categorical=True, cyclic=True)
