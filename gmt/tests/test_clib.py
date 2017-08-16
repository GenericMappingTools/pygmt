# pylint: disable=protected-access
"""
Test the wrappers for the C API.
"""
import os

import pytest

from ..clib import load_libgmt, LibGMT
from ..clib.core import clib_extension, check_libgmt
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
    lib = LibGMT()
    assert lib.get_constant('GMT_SESSION_EXTERNAL') != -99999
    assert lib.get_constant('GMT_MODULE_CMD') != -99999
    assert lib.get_constant('GMT_PAD_DEFAULT') != -99999
    with pytest.raises(GMTCLibError):
        lib.get_constant('A_WHOLE_LOT_OF_JUNK')


def test_clib_session_management():
    "Test that create and destroy session are called without errors"
    lib = LibGMT()
    session1 = lib._create_session()
    assert session1 is not None
    session2 = lib._create_session()
    assert session2 is not None
    assert session2 != session1
    lib._destroy_session(session1)
    lib._destroy_session(session2)


def test_destroy_session_fails():
    "Fail to destroy session when given bad input"
    lib = LibGMT()
    with pytest.raises(GMTCLibError):
        lib._destroy_session(None)


def test_call_module():
    "Run a command to see if call_module works"
    data_fname = os.path.join(TEST_DATA_DIR, 'points.txt')
    out_fname = 'test_call_module.txt'
    with LibGMT() as lib:
        lib.call_module('gmtinfo', '{} -C ->{}'.format(data_fname, out_fname))
    assert os.path.exists(out_fname)
    with open(out_fname) as out_file:
        output = out_file.read().strip().replace('\t', ' ')
        assert output == '11.5309 61.7074 -2.9289 7.8648 0.1412 0.9338'
    os.remove(out_fname)


def test_call_module_fails():
    "Fails when given bad input"
    with LibGMT() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module('meh', '')


def test_call_module_no_session():
    "Fails when not in a session"
    lib = LibGMT()
    with pytest.raises(GMTCLibError):
        lib.call_module('gmtdefaults', '')


def test_parse_data_family():
    "Parsing the family argument correctly."
    # 'family' can be a single GMT constant or two separated by a |
    with LibGMT() as lib:
        families = lib._valid_families
        vias = lib._valid_vias
        test_cases = ((family, via) for family in families for via in vias)
        for family in families:
            assert lib._parse_data_family(family) == lib.get_constant(family)
        for family, via in test_cases:
            composite = '|'.join([family, via])
            expected = lib.get_constant(family) + lib.get_constant(via)
            assert lib._parse_data_family(composite) == expected


def test_parse_data_family_fails():
    "Check if the function fails when given bad input"
    with LibGMT() as lib:
        test_cases = [
            'SOME_random_STRING',
            'GMT_IS_DATASET|GMT_VIA_MATRIX|GMT_VIA_VECTOR',
            'GMT_IS_DATASET|NOT_A_PROPER_VIA',
            'NOT_A_PROPER_FAMILY|GMT_VIA_MATRIX',
            'NOT_A_PROPER_FAMILY|ALSO_INVALID',
        ]
        for test_case in test_cases:
            with pytest.raises(GMTCLibError):
                lib._parse_data_family(test_case)
