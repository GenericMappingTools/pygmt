"""
Test the session management modules.
"""
import os

from ..session_management import begin, end
from ..clib import APISession, call_module


def test_begin_end():
    """"
    Run a command inside a begin-end modern mode block.
    First, end the global session. When finished, restart it.
    """
    end()  # Kill the global session
    begin()
    with APISession() as session:
        call_module(session, 'psbasemap', '-R10/70/-3/8 -JX4i/3i -Ba -P')
    end()
    begin()  # Restart the global session
    assert os.path.exists('gmt-python-session.pdf')
    os.remove('gmt-python-session.pdf')
