"""
Test the wrappers for the API functions
"""
import os

from .. import create_session, call_module


def test_create_session():
    "Test that create_session is called without errors"
    session = create_session()
    assert session is not None


def test_call_module():
    "Run a psbasemap call to see if the module works"
    module = 'psbasemap'
    args = '-R10/70/-3/8 -JX4i/3i -Ba -P ->tmp.ps'
    session = create_session()
    call_module(session, module, args)
    assert os.path.exists('tmp.ps')
    # Not the most ideal test. Just check if no segfaults or exceptions occur.
