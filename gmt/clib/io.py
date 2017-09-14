"""
Wrappers for creating and accessing GMT data containers.
"""
import ctypes

from ..exceptions import GMTCLibError
from .core import get_constant


DATA_FAMILIES = [
    'GMT_IS_DATASET',
    'GMT_IS_GRID',
    'GMT_IS_PALETTE',
    'GMT_IS_TEXTSET',
    'GMT_IS_MATRIX',
    'GMT_IS_VECTOR',
]
DATA_VIAS = [
    'GMT_VIA_MATRIX',
    'GMT_VIA_VECTOR',
]
DATA_GEOMETRIES = [
    'GMT_IS_NONE',
    'GMT_IS_POINT',
    'GMT_IS_LINE',
    'GMT_IS_POLYGON',
    'GMT_IS_PLP',
    'GMT_IS_SURFACE',
]
DATA_MODES = [
    'GMT_CONTAINER_ONLY',
    'GMT_OUTPUT',
]


def create_data(libgmt, session, family, geometry, mode, **kwargs):
    """
    Create an empty GMT data container.

    Parameters
    ----------
    family : str

    """
    # Parse and check input arguments
    family_int = _parse_data_family(libgmt, family)
    if mode not in DATA_MODES:
        raise GMTCLibError("Invalid data creation mode '{}'.".format(mode))
    if geometry not in DATA_GEOMETRIES:
        raise GMTCLibError("Invalid data geometry '{}'.".format(geometry))

    # Convert dim, ranges, and inc to ctypes arrays if given
    dim = _kwargs_to_ctypes_array('dim', kwargs, ctypes.c_uint64*4)
    ranges = _kwargs_to_ctypes_array('ranges', kwargs, ctypes.c_double*4)
    inc = _kwargs_to_ctypes_array('inc', kwargs, ctypes.c_double*2)

    # Use the GMT defaults if no value is given
    registration = kwargs.get('registration',
                              get_constant('GMT_GRID_NODE_REG', libgmt))
    pad = kwargs.get('pad', get_constant('GMT_PAD_DEFAULT', libgmt))

    # Get the C function and set the argument types
    c_create_data = libgmt.GMT_Create_Data
    c_create_data.argtypes = [
        ctypes.c_void_p,                  # API
        ctypes.c_uint,                    # family
        ctypes.c_uint,                    # geometry
        ctypes.c_uint,                    # mode
        ctypes.POINTER(ctypes.c_uint64),  # dim
        ctypes.POINTER(ctypes.c_double),  # range
        ctypes.POINTER(ctypes.c_double),  # inc
        ctypes.c_uint,                    # registration
        ctypes.c_int,                     # pad
        ctypes.c_void_p,                  # data
    ]
    c_create_data.restype = ctypes.c_void_p

    data_ptr = c_create_data(
        session,
        family_int,
        get_constant(geometry, libgmt),
        get_constant(mode, libgmt),
        dim,
        ranges,
        inc,
        registration,
        pad,
        None,  # NULL pointer for existing data
    )

    if data_ptr is None:
        raise GMTCLibError("Failed to create an empty GMT data pointer.")

    return data_ptr


def _kwargs_to_ctypes_array(argument, kwargs, dtype):
    """
    Convert an iterable argument from kwargs into a ctypes array variable.

    If the argument is not present in kwargs, returns ``None``.

    Parameters
    ----------
    argument : str
        The name of the argument.
    kwargs : dict
        Dictionary of keyword arguments.
    dtype : ctypes type
        The ctypes array type (e.g., ``ctypes.c_double*4``)

    Returns
    -------
    ctypes_value : ctypes array or None

    Examples
    --------

    >>> import ctypes as ct
    >>> value = _kwargs_to_ctypes_array('bla', {'bla': [10, 10]}, ct.c_int*2)
    >>> type(value)
    <class 'gmt.clib.io.c_int_Array_2'>
    >>> b = 1
    >>> should_be_none = _kwargs_to_ctypes_array(
    ...     'swallow', {'bla': 1, 'foo': [20, 30]}, ct.c_int*2)
    >>> print(should_be_none)
    None

    """
    if argument in kwargs:
        return dtype(*kwargs[argument])
    return None


def _parse_data_family(libgmt, family):
    """
    Parse the data family string into a GMT constant number.

    Valid family names are: GMT_IS_DATASET, GMT_IS_GRID, GMT_IS_PALETTE,
    GMT_IS_TEXTSET, GMT_IS_MATRIX, and GMT_IS_VECTOR.

    Optionally append a "via" argument to a family name (separated by
    ``|``): GMT_VIA_MATRIX or GMT_VIA_VECTOR.

    Parameters
    ----------
    family : str
        A GMT data family name.

    Returns
    -------
    family_value : int
        The GMT constant corresponding to the family.

    Raises
    ------
    GMTCLibError
        If the family name is invalid or there are more than 2 components
        to the name.

    """
    parts = family.split('|')
    if len(parts) > 2:
        raise GMTCLibError(
            "Too many sections in family (>2): '{}'".format(family))
    family_name = parts[0]
    if family_name not in DATA_FAMILIES:
        raise GMTCLibError(
            "Invalid data family '{}'.".format(family_name))
    family_value = get_constant(family_name, libgmt)
    if len(parts) == 2:
        via_name = parts[1]
        if via_name not in DATA_VIAS:
            raise GMTCLibError(
                "Invalid data family (via) '{}'.".format(via_name))
        via_value = get_constant(via_name, libgmt)
    else:
        via_value = 0
    return family_value + via_value
