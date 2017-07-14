"""
Tests psconvert.
"""
import os

from .. import figure, psconvert, psbasemap


def test_psconvert():
    """
    psconvert creates a figure in the current directory.
    """
    figure()
    psbasemap(R='10/70/-3/8', J='X4i/3i', B='a', P=True)
    prefix = 'test_psconvert'
    psconvert(F=prefix, T='f', A=True, P=True)
    fname = prefix + '.pdf'
    assert os.path.exists(fname)
    os.remove(fname)


def test_psconvert_twice():
    """
    Call psconvert twice to get two figures.
    """
    figure()
    psbasemap(R='10/70/-3/8', J='X4i/3i', B='a', P=True)
    prefix = 'test_psconvert_twice'
    # Make a PDF
    psconvert(F=prefix, T='f')
    fname = prefix + '.pdf'
    assert os.path.exists(fname)
    os.remove(fname)
    # Make a PNG
    psconvert(F=prefix, T='g')
    fname = prefix + '.png'
    assert os.path.exists(fname)
    os.remove(fname)


def test_psconvert_int_options():
    """
    psconvert handles integer options well.
    """
    figure()
    psbasemap(R='10/70/-3/8', J='X4i/3i', B='a', P=True)
    prefix = 'test_psconvert_int_options'
    psconvert(F=prefix, E=100, T='g', I=True)
    assert os.path.exists(prefix + '.png')
    os.remove(prefix + '.png')


def test_psconvert_aliases():
    """
    Use the aliases to make sure they work.
    """
    figure()
    psbasemap(R='10/70/-3/8', J='X4i/3i', B='a', P=True)
    prefix = 'test_psconvert_aliases'
    psconvert(prefix=prefix, fmt='g', crop=True, portrait=True, dpi=100)
    fname = prefix + '.png'
    assert os.path.exists(fname)
    os.remove(fname)
