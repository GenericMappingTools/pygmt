"""
Test Figure.psconvert.
"""

from pathlib import Path

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


@pytest.mark.benchmark
def test_psconvert():
    """
    Check that psconvert creates a figure in the current directory.
    """
    fig = Figure()
    fig.basemap(region="10/70/-3/8", projection="X4i/3i", frame="a")
    prefix = "test_psconvert"
    fig.psconvert(prefix=prefix, fmt="f", crop=True)
    fname = Path(prefix + ".pdf")
    assert fname.exists()
    fname.unlink()


def test_psconvert_twice():
    """
    Call psconvert twice to get two figures.
    """
    fig = Figure()
    fig.basemap(region="10/70/-3/8", projection="X4i/3i", frame="a")
    prefix = "test_psconvert_twice"
    # Make a PDF
    fig.psconvert(prefix=prefix, fmt="f")
    fname = Path(prefix + ".pdf")
    assert fname.exists()
    fname.unlink()
    # Make a PNG
    fig.psconvert(prefix=prefix, fmt="g")
    fname = Path(prefix + ".png")
    assert fname.exists()
    fname.unlink()


def test_psconvert_without_prefix():
    """
    Call psconvert without the 'prefix' parameter.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.psconvert(fmt="g")


@pytest.mark.parametrize("prefix", ["", None, False, True])
def test_psconvert_invalid_prefix(prefix):
    """
    Call psconvert with an invalid 'prefix' argument.
    """
    fig = Figure()
    with pytest.raises(GMTInvalidInput):
        fig.psconvert(fmt="g", prefix=prefix)
