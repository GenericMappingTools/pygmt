"""
ctypes wrappers for core functions from the C API
"""
import sys
import ctypes

from ..exceptions import GMTOSError, GMTCLibNotFoundError, GMTCLibError


def clib_extension(os_name=None):
    """
    Return the extension for the shared library for the current OS.

    .. warning::

        Currently only works for OSX and Linux.

    Returns
    -------
    os_name : str or None
        The operating system name as given by ``sys.platform``
        (the default if None).

    Returns
    -------
    ext : str
        The extension ('.so', '.dylib', etc).

    """
    if os_name is None:
        os_name = sys.platform
    # Set the shared library extension in a platform independent way
    if os_name.startswith('linux'):
        lib_ext = 'so'
    elif os_name == 'darwin':
        # Darwin is OSX
        lib_ext = 'dylib'
    else:
        raise GMTOSError('Unknown operating system: {}'.format(sys.platform))
    return lib_ext


def check_libgmt(libgmt):
    """
    Make sure that libgmt was loaded correctly.

    Checks if it defines some common required functions.

    Does nothing if everything is fine. Raises an exception if any of the
    functions are missing.

    Parameters
    ----------
    libgmt : ctypes.CDLL
        A shared library loaded using ctypes.

    Raises
    ------
    GMTCLibError

    """
    # Check if a few of the functions we need are in the library
    functions = ['Create_Session', 'Get_Enum', 'Call_Module',
                 'Destroy_Session']
    for func in functions:
        if not hasattr(libgmt, 'GMT_' + func):
            msg = ' '.join([
                "Error loading libgmt.",
                "Couldn't access function GMT_{}.".format(func),
            ])
            raise GMTCLibError(msg)


def check_status_code(status, function):
    """
    Check if the status code returned by a function is non-zero.

    Parameters
    ----------
    status : int or None
        The status code returned by a GMT C API function.
    function : str
        The name of the GMT function (used to raise the exception if it's a
        non-zero status code).

    Raises
    ------
    GMTCLibError
        If the status code is non-zero.

    """
    if status is None or status != 0:
        raise GMTCLibError(
            'Failed {} with status code {}.'.format(function, status))


def load_libgmt(libname='libgmt'):
    """
    Find and load ``libgmt`` as a ctypes.CDLL.

    If not given the full path to the library, it must be in standard places or
    by discoverable by setting the environment variable ``LD_LIBRARY_PATH``.

    Parameters
    ----------
    libname : str
        The name of the GMT shared library **without the extension**. Can be a
        full path to the library or just the library name.

    Returns
    -------
    ctypes.CDLL object
        The loaded shared library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).

    """
    try:
        libgmt = ctypes.CDLL('.'.join([libname, clib_extension()]))
        check_libgmt(libgmt)
    except OSError as err:
        msg = ' '.join([
            "Couldn't find the GMT shared library '{}'.".format(libname),
            "Have you tried setting the LD_LIBRARY_PATH environment variable?",
            "\nOriginal error message:",
            "\n\n    {}".format(str(err)),
        ])
        raise GMTCLibNotFoundError(msg)
    return libgmt


class LibGMT():
    """
    Load and access the GMT shared library (libgmt).

    Works as a context manager to create a GMT C API session and destroy it in
    the end.

    Functions of the shared library are exposed as methods of this class.

    If creating GMT data structures to communicate data, put that code inside
    this context manager and reuse the same session.

    Examples
    --------

    >>> with LibGMT() as lib:
    ...     lib.call_module('figure', 'my-figure')

    """

    _valid_data_families = [
        'GMT_IS_DATASET',
        'GMT_IS_GRID',
        'GMT_IS_PALETTE',
        'GMT_IS_TEXTSET',
        'GMT_IS_MATRIX',
        'GMT_IS_VECTOR',
    ]
    _valid_vias = ['GMT_VIA_MATRIX', 'GMT_VIA_VECTOR']
    _valid_data_geometries = [
        'GMT_IS_NONE',
        'GMT_IS_POINT',
        'GMT_IS_LINE',
        'GMT_IS_POLYGON',
        'GMT_IS_PLP',
        'GMT_IS_SURFACE',
    ]
    _valid_data_modes = ['GMT_CONTAINER_ONLY', 'GMT_OUTPUT']

    def __init__(self):
        self._libgmt = load_libgmt()
        self._session_id = None
        self._session_name = 'gmt-python-session'

    def __enter__(self):
        """
        Start the GMT session and keep the session argument.
        """
        self._session_id = self._create_session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the session when exiting the context.
        """
        self._destroy_session(self._session_id)
        self._session_id = None

    def _create_session(self):
        """
        Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

        It is a C void pointer containing the current session information and
        cannot be accessed directly.

        Remember to terminate the current session using
        :func:`gmt.clib.LibGMT._destroy_session` before creating a new one.

        Returns
        -------
        api_pointer : C void pointer (returned by ctypes as an integer)
            Used by GMT C API functions.

        """
        c_create_session = self._libgmt.GMT_Create_Session
        c_create_session.argtypes = [ctypes.c_char_p, ctypes.c_uint,
                                     ctypes.c_uint, ctypes.c_void_p]
        c_create_session.restype = ctypes.c_void_p
        # None is passed in place of the print function pointer. It becomes the
        # NULL pointer when passed to C, prompting the C API to use the default
        # print function.
        session = c_create_session(self._session_name.encode(),
                                   self.get_constant('GMT_PAD_DEFAULT'),
                                   self.get_constant('GMT_SESSION_EXTERNAL'),
                                   None)

        if session is None:
            raise GMTCLibError("Failed to create a GMT API void pointer.")

        return session

    def _destroy_session(self, session):
        """
        Terminate and free the memory of a registered ``GMTAPI_CTRL`` session.

        The session is created and consumed by the C API modules and needs to
        be freed before creating a new. Otherwise, some of the configuration
        files might be left behind and can influence subsequent API calls.

        Parameters
        ----------
        session : C void pointer (returned by ctypes as an integer)
            The active session object produced by
            :func:`gmt.clib.LibGMT._create_session`.

        """
        c_destroy_session = self._libgmt.GMT_Destroy_Session
        c_destroy_session.argtypes = [ctypes.c_void_p]
        c_destroy_session.restype = ctypes.c_int

        status = c_destroy_session(session)
        check_status_code(status, 'GMT_Destroy_Session')

    def get_constant(self, name):
        """
        Get the value of a constant (C enum) from gmt_resources.h

        Used to set configuration values for other API calls.

        Parameters
        ----------
        name : str
            The name of the constant (e.g., ``"GMT_SESSION_EXTERNAL"``)

        Returns
        -------
        constant : int
            Integer value of the constant. Do not rely on this value because it
            might change.

        Raises
        ------
        GMTCLibError
            If the constant doesn't exist.

        """
        c_get_enum = self._libgmt.GMT_Get_Enum
        c_get_enum.argtypes = [ctypes.c_char_p]
        c_get_enum.restype = ctypes.c_int

        value = c_get_enum(name.encode())

        if value is None or value == -99999:
            raise GMTCLibError(
                "Constant '{}' doesn't exits in libgmt.".format(name))

        return value

    def call_module(self, module, args):
        """
        Call a GMT module with the given arguments.

        Makes a call to ``GMT_Call_Module`` from the C API using mode
        ``GMT_MODULE_CMD`` (arguments passed as a single string).

        Most interactions with the C API are done through this function.

        Parameters
        ----------
        module : str
            Module name (``'pscoast'``, ``'psbasemap'``, etc).
        args : str
            String with the command line arguments that will be passed to the
            module (for example, ``'-R0/5/0/10 -JM'``).

        Raises
        ------
        GMTCLibError
            If the returned status code of the functions is non-zero.

        """
        c_call_module = self._libgmt.GMT_Call_Module
        c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                  ctypes.c_int, ctypes.c_void_p]
        c_call_module.restype = ctypes.c_int

        mode = self.get_constant('GMT_MODULE_CMD')
        status = c_call_module(self._session_id, module.encode(), mode,
                               args.encode())
        check_status_code(status, 'GMT_Call_Module')

    def create_data(self, family, geometry, mode, **kwargs):
        """
        Create an empty GMT data container.

        Parameters
        ----------
        family : str

        """
        # Parse and check input arguments
        family_int = self._parse_data_family(family)
        geometry_int = self._parse_data_geometry(geometry)
        mode_int = self._parse_data_mode(mode)
        registration = kwargs.get('registration',
                                  self.get_constant('GMT_GRID_NODE_REG'))
        pad = kwargs.get('pad', self.get_constant('GMT_PAD_DEFAULT'))

        dim, ranges, inc = self._parse_data_dim_range_inc(kwargs)

        # Get the C function and set the argument types
        c_create_data = self._libgmt.GMT_Create_Data
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
            self._session_id, family_int, geometry_int, mode_int, dim, ranges,
            inc, registration, pad, None)

        if data_ptr is None:
            raise GMTCLibError("Failed to create an empty GMT data pointer.")

        return data_ptr

    def _parse_data_dim_range_inc(self, kwargs):  # pylint: disable=no-self-use
        """
        """
        # Check if dim, range and int are giving correctly
        if 'dim' in kwargs:
            int_array_4 = ctypes.c_uint64*4
            dim = int_array_4(*kwargs['dim'])
        else:
            dim = None
        if 'range' in kwargs:
            double_array_4 = ctypes.c_double*4
            ranges = double_array_4(*kwargs['range'])
        else:
            ranges = None
        if 'inc' in kwargs:
            double_array_2 = ctypes.c_double*2
            inc = double_array_2(*kwargs['inc'])
        else:
            inc = None
        return dim, ranges, inc

    def _parse_data_mode(self, mode):
        """
        """
        if mode not in self._valid_data_modes:
            raise GMTCLibError("Invalid data creation mode '{}'.".format(mode))
        return self.get_constant(mode)

    def _parse_data_geometry(self, geometry):
        """
        """
        if geometry not in self._valid_data_geometries:
            raise GMTCLibError("Invalid data geometry '{}'.".format(geometry))
        return self.get_constant(geometry)

    def _parse_data_family(self, family):
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
        if family_name not in self._valid_data_families:
            raise GMTCLibError(
                "Invalid data family '{}'.".format(family_name))
        family_value = self.get_constant(family_name)
        if len(parts) == 2:
            via_name = parts[1]
            if via_name not in self._valid_vias:
                raise GMTCLibError(
                    "Invalid data family (via) '{}'.".format(via_name))
            via_value = self.get_constant(via_name)
        else:
            via_value = 0
        return family_value + via_value
