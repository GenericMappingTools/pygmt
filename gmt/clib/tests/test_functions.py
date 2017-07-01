"""
Test the wrappers for the API functions
"""
from .. import create_session


def test_create_session():
    "Test that create_session is called without errors"
    session = create_session()
    assert session is not None
