"""
Test the session management modules.
"""
import os

from .. import begin, end, figure
from ..clib import call_module


def test_session():
    """"
    Run a command inside a begin-end modern mode block.
    """
    begin()
    call_module('psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()
    assert os.path.exists('gmt-python-session.pdf')
    os.remove('gmt-python-session.pdf')


def test_session_figure():
    """
    Run a figure command inside a begin-end modern mode block.
    No file should be generated.
    """
    begin()
    figure()
    call_module('psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()
    assert not os.path.exists('gmt-python-figure.pdf')
