"""
Test the session management modules.
"""
import os
import pytest

from ..session_management import begin, end
from ..clib import Session
from ..exceptions import GMTCLibError


def test_begin_end():
    """"
    Run a command inside a begin-end modern mode block.
    First, end the global session. When finished, restart it.
    """
    with pytest.raises(GMTCLibError, match="Module 'end' failed with status code 78:"):
        end()  # Kill the global session first

    begin()
    with Session() as lib:
        lib.call_module("basemap", "-R10/70/-3/8 -JX4i/3i -Ba")
    end()

    begin()  # Restart the global session
    assert os.path.exists("pygmt-session.pdf")
    os.remove("pygmt-session.pdf")
