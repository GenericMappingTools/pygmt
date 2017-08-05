"""
Test the wrappers for the C API.
"""
import os

import pytest

from ..clib import create_session, destroy_session, call_module, load_libgmt, \
    APISession, get_constant
from ..exceptions import GMTCLibError


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    libgmt = load_libgmt()
    assert hasattr(libgmt, 'GMT_Create_Session')


def test_constant():
    "Test that I can get correct constants from the C lib"
    assert get_constant('GMT_SESSION_EXTERNAL') != -99999
    assert get_constant('GMT_MODULE_CMD') != -99999
    assert get_constant('GMT_PAD_DEFAULT') != -99999
    with pytest.raises(GMTCLibError):
        get_constant('A_WHOLE_LOT_OF_JUNK')


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
    data_fname = os.path.join(TEST_DATA_DIR, 'points.txt')
    out_fname = 'test_call_module.txt'
    with APISession() as session:
        call_module(session, 'gmtinfo',
                    '{} -C ->{}'.format(data_fname, out_fname))
    assert os.path.exists(out_fname)
    with open(out_fname) as out_file:
        output = out_file.read().strip().replace('\t', ' ')
        assert output == '11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338'
    os.remove(out_fname)
