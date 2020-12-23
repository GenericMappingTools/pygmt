"""
Tests psconvert.
"""
import os

from pygmt import Figure


def test_psconvert():
    """
    psconvert creates a figure in the current directory.
    """
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="a")
    prefix = "test_psconvert"
    fig.psconvert(F=prefix, T="f", A=True)
    fname = prefix + ".pdf"
    assert os.path.exists(fname)
    os.remove(fname)


def test_psconvert_twice():
    """
    Call psconvert twice to get two figures.
    """
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="a")
    prefix = "test_psconvert_twice"
    # Make a PDF
    fig.psconvert(F=prefix, T="f")
    fname = prefix + ".pdf"
    assert os.path.exists(fname)
    os.remove(fname)
    # Make a PNG
    fig.psconvert(F=prefix, T="g")
    fname = prefix + ".png"
    assert os.path.exists(fname)
    os.remove(fname)


def test_psconvert_int_options():
    """
    psconvert handles integer options well.
    """
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="a")
    prefix = "test_psconvert_int_options"
    fig.psconvert(F=prefix, E=100, T="g", I=True)
    assert os.path.exists(prefix + ".png")
    os.remove(prefix + ".png")


def test_psconvert_aliases():
    """
    Use the aliases to make sure they work.
    """
    fig = Figure()
    fig.basemap(R="10/70/-3/8", J="X4i/3i", B="a")
    prefix = "test_psconvert_aliases"
    fig.psconvert(prefix=prefix, fmt="g", crop=True, dpi=100)
    fname = prefix + ".png"
    assert os.path.exists(fname)
    os.remove(fname)
