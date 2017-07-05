"""
Test the wrappers for the C API.
"""
import os

from ..clib import create_session, destroy_session, call_module, load_libgmt


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    libgmt = load_libgmt()
    assert hasattr(libgmt, 'GMT_Create_Session')


def test_clib_session_management():
    "Test that create and destroy session are called without errors"
    session1 = create_session()
    assert session1 is not None
    session2 = create_session()
    assert session2 is not None
    assert session2 != session1
    destroy_session(session1)
    destroy_session(session2)


def test_call_module():
    "Run a psbasemap call to see if the module works"
    module = 'psbasemap'
    args = '-R10/70/-3/8 -JX4i/3i -Ba -P ->tmp.ps'
    session = create_session()
    call_module(session, module, args)
    destroy_session(session)
    assert os.path.exists('tmp.ps')
    os.remove('tmp.ps')
    # Not the most ideal test. Just check if no segfaults or exceptions occur.
