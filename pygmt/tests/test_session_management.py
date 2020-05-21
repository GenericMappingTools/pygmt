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
        lib.call_module("basemap", "-R10/70/-3/8 -JX4i/3i -Ba")
    end()
    begin()  # Restart the global session
    assert os.path.exists("pygmt-session.pdf")
    os.remove("pygmt-session.pdf")


def test_gmt_compat_6_is_applied(capsys):
    """
    Ensure that users with old gmt.conf files won't get pygmt-session [ERROR]:
    GMT_COMPATIBILITY: Expects values from 6 to 6; reset to 6.
    """
    end()  # Kill the global session
    try:
        with Session() as lib:
            # pretend that gmt.conf has GMT_COMPATIBILITY = 5
            lib.call_module("gmtset", "GMT_COMPATIBILITY 5")
        begin()
        with Session() as lib:
            lib.call_module("basemap", "-R10/70/-3/8 -JX4i/3i -Ba")
            out, err = capsys.readouterr()  # capture stdout and stderr
            assert out == ""
            assert err != (
                "pygmt-session [ERROR]: GMT_COMPATIBILITY:"
                " Expects values from 6 to 6; reset to 6.\n"
            )
            assert err == ""  # double check that there are no other errors
    finally:
        with Session() as lib:
            # revert gmt.conf back to GMT_COMPATIBILITY = 6
            lib.call_module("set", "GMT_COMPATIBILITY 6")
        end()
        begin()  # Restart the global session
        assert os.path.exists("pygmt-session.pdf")
        os.remove("pygmt-session.pdf")
