"""
Tests psconvert.
"""
import os

from .. import clib, figure, psconvert


def test_psconvert():
    """
    psconvert creates a figure in the current directory.
    """
    figure()
    clib.call_module('psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    psconvert(F='test_psconvert', T='f', A=True, P=True)
    assert os.path.exists('test_psconvert.pdf')
    os.remove('test_psconvert.pdf')
    # Calling twice doesn't yet work on GMT trunk
    # psconvert(F='test_psconvert', T='g', A=True, P=True)
    # assert os.path.exists('test_psconvert.png')
    # os.remove('test_psconvert.png')


def test_psconvert_int_options():
    """
    psconvert handles integer options well.
    """
    figure()
    clib.call_module('psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    prefix = 'test_psconvert_int_options'
    psconvert(F=prefix, E=100, T='g', I=True)
    assert os.path.exists(prefix + '.png')
    os.remove(prefix + '.png')
