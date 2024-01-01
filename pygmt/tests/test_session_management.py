"""
Test the session management modules.
"""
import os
from pathlib import Path

import pytest
from pygmt.clib import Session
from pygmt.session_management import begin, end


@pytest.mark.benchmark
def test_begin_end():
    """
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
        # Generate a gmt.conf file in the current directory
        # with GMT_COMPATIBILITY = 5
        with Session() as lib:
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
        end()
        # Clean up the global "gmt.conf" in the current directory
        assert os.path.exists("gmt.conf")
        os.remove("gmt.conf")
        assert os.path.exists("pygmt-session.pdf")
        os.remove("pygmt-session.pdf")
        # Make sure no global "gmt.conf" in the current directory
        assert not os.path.exists("gmt.conf")
        begin()  # Restart the global session


def gmt_func(figname):
    """
    Workaround to let PyGMT support multiprocessing.

    See
    https://github.com/GenericMappingTools/pygmt/issues/217#issuecomment-754774875
    """
    from importlib import reload

    import pygmt

    reload(pygmt)
    fig = pygmt.Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    fig.savefig(figname)


def test_session_multiprocessing():
    """
    Make sure that the multiprocessing is supported if pygmt is re-imported.
    """

    import multiprocessing as mp

    fig_prefix = "test_session_multiprocessing"
    with mp.Pool(2) as p:
        p.map(gmt_func, [f"{fig_prefix}-1.png", f"{fig_prefix}-2.png"])
    for i in [1, 2]:
        assert Path(f"{fig_prefix}-{i}.png").exists()
        Path(f"{fig_prefix}-{i}.png").unlink()
