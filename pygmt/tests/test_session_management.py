"""
Test the session management modules.
"""

import multiprocessing as mp
from importlib import reload
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
        lib.call_module("basemap", ["-R10/70/-3/8", "-JX4i/3i", "-Ba"])
    end()
    begin()  # Restart the global session
    assert Path("pygmt-session.pdf").exists()
    Path("pygmt-session.pdf").unlink()


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
            lib.call_module("gmtset", ["GMT_COMPATIBILITY=5"])
        begin()
        with Session() as lib:
            lib.call_module("basemap", ["-R10/70/-3/8", "-JX4i/3i", "-Ba"])
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
        assert Path("gmt.conf").exists()
        Path("gmt.conf").unlink()
        assert Path("pygmt-session.pdf").exists()
        Path("pygmt-session.pdf").unlink()
        # Make sure no global "gmt.conf" in the current directory
        assert not Path("gmt.conf").exists()
        begin()  # Restart the global session


def _gmt_func_wrapper(figname):
    """
    A wrapper for running PyGMT scripts with multiprocessing.

    Currently, we have to import pygmt and reload it in each process. Workaround from
    https://github.com/GenericMappingTools/pygmt/issues/217#issuecomment-754774875.
    """
    import pygmt

    reload(pygmt)
    fig = pygmt.Figure()
    fig.basemap(region=[10, 70, -3, 8], projection="X8c/6c", frame="afg")
    fig.savefig(figname)


def test_session_multiprocessing():
    """
    Make sure that multiprocessing is supported if pygmt is re-imported.
    """
    prefix = "test_session_multiprocessing"
    with mp.Pool(2) as p:
        p.map(_gmt_func_wrapper, [f"{prefix}-1.png", f"{prefix}-2.png"])
    Path(f"{prefix}-1.png").unlink()
    Path(f"{prefix}-2.png").unlink()
