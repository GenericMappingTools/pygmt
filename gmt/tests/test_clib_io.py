"""
Test the creation and manipulation of GMT data containers.
"""
import pytest

from ..exceptions import GMTCLibError
from ..clib.core import load_libgmt, create_session, destroy_session, \
    get_constant
from..clib import DATA_FAMILIES, DATA_VIAS


def test_parse_data_family_single():
    "Parsing a single family argument correctly."
    lib = LibGMT()
    for family in DATA_FAMILIES:
        assert lib._parse_data_family(family) == lib.get_constant(family)


def test_parse_data_family_via():
    "Parsing a composite family argument (separated by |) correctly."
    lib = LibGMT()
    test_cases = ((family, via)
                  for family in DATA_FAMILIES
                  for via in DATA_VIAS)
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
        destroy_session(session, lib)
        assert data_vector != data_matrix


def test_create_data_grid_dim():
    "Run the function to make sure it doesn't fail badly."
    lib = load_libgmt()
    session = create_session('test_create_data', lib)
    # Grids from matrices using dim
    create_data(
        libgmt=lib,
        session=session,
        family='GMT_IS_GRID|GMT_VIA_MATRIX',
        geometry='GMT_IS_SURFACE',
        mode='GMT_CONTAINER_ONLY',
        dim=[10, 20, 1, 0],
    )
    destroy_session(session, lib)


def test_create_data_grid_range():
    "Run the function to make sure it doesn't fail badly."
    lib = load_libgmt()
    session = create_session('test_create_data', lib)
    # Grids from matrices using range and int
    create_data(
        libgmt=lib,
        session=session,
        family='GMT_IS_GRID|GMT_VIA_MATRIX',
        geometry='GMT_IS_SURFACE',
        mode='GMT_CONTAINER_ONLY',
        dim=[0, 0, 1, 0],
        ranges=[150., 250., -20., 20.],
        inc=[0.1, 0.2],
    )
    destroy_session(session, lib)


def test_create_data_fails():
    "Test for failures on bad input"
    lib = load_libgmt()
    session = create_session('test_create_data', lib)
    # Passing in invalid mode
    with pytest.raises(GMTCLibError):
        create_data(
            libgmt=lib,
            session=session,
            family='GMT_IS_DATASET',
            geometry='GMT_IS_SURFACE',
            mode='Not_a_valid_mode',
            dim=[0, 0, 1, 0],
            ranges=[150., 250., -20., 20.],
            inc=[0.1, 0.2],
        )
    # Passing in invalid geometry
    with pytest.raises(GMTCLibError):
        create_data(
            libgmt=lib,
            session=session,
            family='GMT_IS_GRID',
            geometry='Not_a_valid_geometry',
            mode='GMT_CONTAINER_ONLY',
            dim=[0, 0, 1, 0],
            ranges=[150., 250., -20., 20.],
            inc=[0.1, 0.2],
        )
    destroy_session(session, lib)
