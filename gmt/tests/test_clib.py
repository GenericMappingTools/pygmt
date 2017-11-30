# pylint: disable=protected-access
"""
Test the wrappers for the C API.
"""
import os

import pytest
import numpy as np

from ..clib.core import LibGMT
from ..clib.utils import clib_extension, load_libgmt, check_libgmt
from ..exceptions import GMTCLibError, GMTOSError, GMTCLibNotFoundError, \
    GMTCLibNoSessionError


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
    assert lib.get_constant('GMT_DOUBLE') != -99999
    with pytest.raises(GMTCLibError):
        lib.get_constant('A_WHOLE_LOT_OF_JUNK')


def test_create_destroy_session():
    "Test that create and destroy session are called without errors"
    lib = LibGMT()
    session1 = lib.create_session(session_name='test_session1')
    assert session1 is not None
    session2 = lib.create_session(session_name='test_session2')
    assert session2 is not None
    assert session2 != session1
    lib.destroy_session(session1)
    lib.destroy_session(session2)


def test_destroy_session_fails():
    "Fail to destroy session when given bad input"
    lib = LibGMT()
    with pytest.raises(GMTCLibError):
        lib.destroy_session(None)


def test_set_log_file_fails():
    "log_to_file should fail for invalid file names"
    with LibGMT() as lib:
        with pytest.raises(GMTCLibError):
            with lib.log_to_file(logfile=''):
                pass


def test_errors_sent_to_log_file():
    "Make sure error messages are recorded in the log file."
    with LibGMT() as lib:
        mode = lib.get_constant('GMT_MODULE_CMD')
        with lib.log_to_file() as logfile:
            assert os.path.exists(logfile)
            data_file = 'not-a-valid-data-file.bla'
            # Make a bogus module call that will fail
            status = lib._c_call_module(lib.current_session,
                                        'info'.encode(),
                                        mode,
                                        data_file.encode())
            assert status != 0
            # Check the file content
            with open(logfile) as flog:
                log = flog.read()
    msg = 'gmtinfo [ERROR]: Error for input file: No such file ({})'.format(
        data_file)
    assert log.strip() == msg
    # Log should be deleted as soon as the with is over
    assert not os.path.exists(logfile)


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


def test_call_module_error_message():
    "Check that the exception has the error message from call_module"
    data_file = 'bogus-data.bla'
    true_msg = '\n'.join([
        "'info' failed (error: 69).",
        "---------- Error log ----------",
        '',
        'gmtinfo [ERROR]: Error for input file: No such file (bogus-data.bla)',
        '',
        "-------------------------------",
    ])
    with LibGMT() as lib:
        # Make a bogus module call that will fail
        try:
            lib.call_module('info', data_file)
        except GMTCLibError as error:
            assert str(error) == true_msg
        else:
            assert False, "Didn't raise an exception"


def test_call_module_invalid_name():
    "Fails when given bad input"
    with LibGMT() as lib:
        with pytest.raises(GMTCLibError):
            lib.call_module('meh', '')


def test_method_no_session():
    "Fails when not in a session"
    # Create an instance of LibGMT without "with" so no session is created.
    lib = LibGMT()
    with pytest.raises(GMTCLibNoSessionError):
        lib.call_module('gmtdefaults', '')
    with pytest.raises(GMTCLibNoSessionError):
        lib.current_session  # pylint: disable=pointless-statement


def test_parse_data_family_single():
    "Parsing a single family argument correctly."
    lib = LibGMT()
    for family in lib.data_families:
        assert lib._parse_data_family(family) == lib.get_constant(family)


def test_parse_data_family_via():
    "Parsing a composite family argument (separated by |) correctly."
    lib = LibGMT()
    test_cases = ((family, via)
                  for family in lib.data_families
                  for via in lib.data_vias)
    for family, via in test_cases:
        composite = '|'.join([family, via])
        expected = lib.get_constant(family) + lib.get_constant(via)
        assert lib._parse_data_family(composite) == expected


def test_parse_data_family_fails():
    "Check if the function fails when given bad input"
    lib = LibGMT()
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


def test_create_data_dataset():
    "Run the function to make sure it doesn't fail badly."
    with LibGMT() as lib:
        # Dataset from vectors
        data_vector = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_VECTOR',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[10, 20, 1, 0],  # columns, rows, layers, dtype
        )
        # Dataset from matrices
        data_matrix = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_MATRIX',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[10, 20, 1, 0],
        )
        assert data_vector != data_matrix


def test_create_data_grid_dim():
    "Run the function to make sure it doesn't fail badly."
    with LibGMT() as lib:
        # Grids from matrices using dim
        lib.create_data(
            family='GMT_IS_GRID|GMT_VIA_MATRIX',
            geometry='GMT_IS_SURFACE',
            mode='GMT_CONTAINER_ONLY',
            dim=[10, 20, 1, 0],
        )


def test_create_data_grid_range():
    "Run the function to make sure it doesn't fail badly."
    with LibGMT() as lib:
        # Grids from matrices using range and int
        lib.create_data(
            family='GMT_IS_GRID|GMT_VIA_MATRIX',
            geometry='GMT_IS_SURFACE',
            mode='GMT_CONTAINER_ONLY',
            dim=[0, 0, 1, 0],
            ranges=[150., 250., -20., 20.],
            inc=[0.1, 0.2],
        )


def test_create_data_fails():
    "Test for failures on bad input"
    with LibGMT() as lib:
        # Passing in invalid mode
        with pytest.raises(GMTCLibError):
            lib.create_data(
                family='GMT_IS_DATASET',
                geometry='GMT_IS_SURFACE',
                mode='Not_a_valid_mode',
                dim=[0, 0, 1, 0],
                ranges=[150., 250., -20., 20.],
                inc=[0.1, 0.2],
            )
        # Passing in invalid geometry
        with pytest.raises(GMTCLibError):
            lib.create_data(
                family='GMT_IS_GRID',
                geometry='Not_a_valid_geometry',
                mode='GMT_CONTAINER_ONLY',
                dim=[0, 0, 1, 0],
                ranges=[150., 250., -20., 20.],
                inc=[0.1, 0.2],
            )

def test_put_vector():
    "Check that assigning a numpy array to a dataset works"
    dtypes = 'float32 float64 int32 int64 uint32 uint64'.split()
    with LibGMT() as lib:
        # Dataset from vectors
        dataset = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_VECTOR',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[len(dtypes), 5, 1, 0],  # columns, rows, layers, dtype
        )
        for col, dtype in enumerate(dtypes):
            data = np.array([37, 12, 556, 21, 42], dtype=dtype)
            lib.put_vector(dataset, column=col, vector=data)


def test_put_vector_invalid_dtype():
    "Check that it fails with an exception for invalid data types"
    with LibGMT() as lib:
        # Dataset from vectors
        dataset = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_VECTOR',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[2, 3, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([37, 12, 556], dtype='complex128')
        with pytest.raises(GMTCLibError):
            lib.put_vector(dataset, column=1, vector=data)


def test_put_vector_wrong_column():
    "Check that it fails with an exception when giving an invalid column"
    with LibGMT() as lib:
        # Dataset from vectors
        dataset = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_VECTOR',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[1, 3, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([37, 12, 556], dtype='float32')
        with pytest.raises(GMTCLibError):
            lib.put_vector(dataset, column=1, vector=data)


def test_put_vector_2d_fails():
    "Check that it fails with an exception for multidimensional arrays"
    with LibGMT() as lib:
        # Dataset from vectors
        dataset = lib.create_data(
            family='GMT_IS_DATASET|GMT_VIA_VECTOR',
            geometry='GMT_IS_POINT',
            mode='GMT_CONTAINER_ONLY',
            dim=[1, 6, 1, 0],  # columns, rows, layers, dtype
        )
        data = np.array([[37, 12, 556], [37, 12, 556]], dtype='int32')
        with pytest.raises(GMTCLibError):
            lib.put_vector(dataset, column=0, vector=data)
