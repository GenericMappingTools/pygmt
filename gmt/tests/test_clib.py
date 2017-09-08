# pylint: disable=protected-access
"""
Test the wrappers for the C API.
"""
import os

import pytest

from ..clib.core import load_libgmt, check_libgmt, create_session, \
    destroy_session, call_module, get_constant
from ..clib.context_manager import LibGMT
from ..clib.utils import clib_extension
from ..exceptions import GMTCLibError, GMTOSError, GMTCLibNotFoundError


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_load_libgmt():
    "Test that loading libgmt works and doesn't crash."
    load_libgmt()


def test_load_libgmt_fail():
    "Test that loading fails when given a bad library path."
    with pytest.raises(GMTCLibNotFoundError):
        load_libgmt('some/wrong/path/libgmt')


def test_check_libgmt():
    "Make sure check_libgmt fails when given a bogus library"
    with pytest.raises(GMTCLibError):
        check_libgmt(dict())


def test_clib_extension():
    "Make sure we get the correct extension for different OS names"
    for linux in ['linux', 'linux2', 'linux3']:
        assert clib_extension(linux) == 'so'
    assert clib_extension('darwin') == 'dylib'
    with pytest.raises(GMTOSError):
        clib_extension('meh')


def test_constant():
    "Test that I can get correct constants from the C lib"
    lib = load_libgmt()
    assert get_constant('GMT_SESSION_EXTERNAL', lib) != -99999
    assert get_constant('GMT_MODULE_CMD', lib) != -99999
    assert get_constant('GMT_PAD_DEFAULT', lib) != -99999
    with pytest.raises(GMTCLibError):
        get_constant('A_WHOLE_LOT_OF_JUNK', lib)


def test_clib_session_management():
    "Test that create and destroy session are called without errors"
    lib = load_libgmt()
    session1 = create_session(session_name='test_session1', libgmt=lib)
    assert session1 is not None
    session2 = create_session(session_name='test_session2', libgmt=lib)
    assert session2 is not None
    assert session2 != session1
    destroy_session(session1, libgmt=lib)
    destroy_session(session2, libgmt=lib)


def test_destroy_session_fails():
    "Fail to destroy session when given bad input"
    lib = load_libgmt()
    with pytest.raises(GMTCLibError):
        destroy_session(None, lib)


def test_call_module():
    "Run a psbasemap call to see if the module works"
    data_fname = os.path.join(TEST_DATA_DIR, 'points.txt')
    out_fname = 'test_call_module.txt'
    lib = load_libgmt()
    session = create_session('test_call_module', lib)
    call_module(session, 'gmtinfo', '{} -C ->{}'.format(data_fname, out_fname),
                lib)
    destroy_session(session, lib)
    assert os.path.exists(out_fname)
    with open(out_fname) as out_file:
        output = out_file.read().strip().replace('\t', ' ')
        assert output == '11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338'
    os.remove(out_fname)


def test_call_module_fails():
    "Fails when given bad input"
    lib = load_libgmt()
    session = create_session('test_call_module_fails', lib)
    with pytest.raises(GMTCLibError):
        call_module(session, 'meh', '', lib)
    destroy_session(session, lib)


def test_call_module_no_session():
    "Fails when not in a session"
    lib = load_libgmt()
    with pytest.raises(GMTCLibError):
        call_module(None, 'gmtdefaults', '', lib)


def test_context_manager():
    "Test the LibGMT context manager"
    with LibGMT() as lib:
        lib.get_constant('GMT_SESSION_EXTERNAL')
        lib.call_module('psbasemap', '-R0/1/0/1 -JX6i -Bafg')
