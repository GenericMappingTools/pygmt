"""
Test the creation and manipulation of GMT data containers.
"""
import pytest

from ..exceptions import GMTCLibError
from ..clib.core import load_libgmt, create_session, destroy_session, \
    get_constant
from ..clib.io import create_data, _parse_data_family, \
    DATA_FAMILIES, DATA_VIAS


def test_parse_data_family_single():
    "Parsing a single family argument correctly."
    lib = load_libgmt()
    for family in DATA_FAMILIES:
        assert _parse_data_family(lib, family) == get_constant(family, lib)


def test_parse_data_family_via():
    "Parsing a composite family argument (separated by |) correctly."
    lib = load_libgmt()
    test_cases = ((family, via)
                  for family in DATA_FAMILIES
                  for via in DATA_VIAS)
    for family, via in test_cases:
        composite = '|'.join([family, via])
        expected = get_constant(family, lib) + get_constant(via, lib)
        assert _parse_data_family(lib, composite) == expected


def test_parse_data_family_fails():
    "Check if the function fails when given bad input"
    lib = load_libgmt()
    test_cases = [
        'SOME_random_STRING',
        'GMT_IS_DATASET|GMT_VIA_MATRIX|GMT_VIA_VECTOR',
        'GMT_IS_DATASET|NOT_A_PROPER_VIA',
        'NOT_A_PROPER_FAMILY|GMT_VIA_MATRIX',
        'NOT_A_PROPER_FAMILY|ALSO_INVALID',
    ]
    for test_case in test_cases:
        with pytest.raises(GMTCLibError):
            _parse_data_family(lib, test_case)


def test_create_data_dataset():
    "Run the function to make sure it doesn't fail badly."
    lib = load_libgmt()
    session = create_session('test_create_data', lib)
    # Dataset from vectors
    data_vector = create_data(
        libgmt=lib,
        session=session,
        family='GMT_IS_DATASET|GMT_VIA_VECTOR',
        geometry='GMT_IS_POINT',
        mode='GMT_CONTAINER_ONLY',
        dim=[10, 20, 1, 0],  # columns, rows, layers, dtype
    )
    # Dataset from matrices
    data_matrix = create_data(
        libgmt=lib,
        session=session,
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
