"""
Test the session management modules.
"""
import os

from .. import Figure
from ..session_management import begin, end


def test_begin_end():
    """"
    Run a command inside a begin-end modern mode block.
    First, end the global session. When finished, restart it.
    """
    end()  # Kill the global session
    begin()
    Figure().psbasemap(R='10/70/-3/8', J='X4i/3i', B='a', P=True)
    end()
    begin()  # Restart the global session
    assert os.path.exists('gmt-python-session.pdf')
    os.remove('gmt-python-session.pdf')
