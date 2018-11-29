"""
Test the session management modules.
"""
import os

from ..session_management import begin, end
from ..clib import Session


def test_begin_end():
    """"
    Run a command inside a begin-end modern mode block.
    First, end the global session. When finished, restart it.
    """
    end()  # Kill the global session
    begin()
    with Session() as lib:
        lib.call_module("psbasemap", "-R10/70/-3/8 -JX4i/3i -Ba")
    end()
    begin()  # Restart the global session
    assert os.path.exists("gmt-python-session.pdf")
    os.remove("gmt-python-session.pdf")
