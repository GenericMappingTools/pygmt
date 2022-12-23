"""
Tests psconvert.
"""
import os

import pytest
from pygmt import Figure
from pygmt.exceptions import GMTInvalidInput


def test_psconvert():
    """
    psconvert creates a figure in the current directory.
    """
    fig = Figure()
    fig.basemap(region="10/70/-3/8", projection="X4i/3i", frame="a")
    prefix = "test_psconvert"
    fig.psconvert(prefix=prefix, fmt="f", crop=True)
    fname = prefix + ".pdf"
    assert os.path.exists(fname)
    os.remove(fname)


def test_psconvert_twice():
    """
    Call psconvert twice to get two figures.
    """
    fig = Figure()
    fig.basemap(region="10/70/-3/8", projection="X4i/3i", frame="a")
    prefix = "test_psconvert_twice"
    # Make a PDF
    fig.psconvert(prefix=prefix, fmt="f")
    fname = prefix + ".pdf"
    assert os.path.exists(fname)
    os.remove(fname)
    # Make a PNG
    fig.psconvert(prefix=prefix, fmt="g")
    fname = prefix + ".png"
    assert os.path.exists(fname)
    os.remove(fname)


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
