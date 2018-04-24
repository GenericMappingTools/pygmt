"""
ctypes wrappers for core functions from the C API
"""
import os
import ctypes
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

from packaging.version import Version
import numpy as np

from ..exceptions import GMTCLibError, GMTCLibNoSessionError, \
    GMTInvalidInput, GMTVersionError
from .utils import load_libgmt, kwargs_to_ctypes_array, vectors_to_arrays, \
    dataarray_to_matrix, as_c_contiguous


class LibGMT():  # pylint: disable=too-many-instance-attributes
    """
    Load and access the GMT shared library (libgmt).

    Works as a context manager to create a GMT C API session and destroy it in
    the end. The context manager feature eliminates the need for the
    ``GMT_Create_Session`` and ``GMT_Destroy_Session`` functions. Thus, they
    are not exposed in the Python API. If you need the void pointer to the GMT
    session, use the ``current_session`` attribute.

    Functions of the shared library are exposed as methods of this class. Most
    methods MUST be used inside the context manager 'with' block.

    If creating GMT data structures to communicate data, put that code inside
    this context manager to reuse the same session.

    Requires a minimum version of GMT (see ``LibGMT.required_version``). Will
    check for the version when entering the ``with`` block. A
    ``GMTVersionError`` exception will be raised if the minimum version
    requirements aren't met.

    By default, will look for the shared library in the directory specified by
    the environment variable ``GMT_LIBRARY_PATH``. If the variable is not set,
    will let ctypes try to find the library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).
    GMTCLibNoSessionError
        If you try to call a method outside of a 'with' block.
    GMTVersionError
        If the minimum required version of GMT is not found.

    Examples
    --------

    >>> with LibGMT() as lib:
    ...     lib.call_module('figure', 'my-figure')

    """

    data_families = [
        'GMT_IS_DATASET',
        'GMT_IS_GRID',
        'GMT_IS_PALETTE',
        'GMT_IS_MATRIX',
        'GMT_IS_VECTOR',
    ]

    data_vias = [
        'GMT_VIA_MATRIX',
        'GMT_VIA_VECTOR',
    ]

    data_geometries = [
        'GMT_IS_NONE',
        'GMT_IS_POINT',
        'GMT_IS_LINE',
        'GMT_IS_POLYGON',
        'GMT_IS_PLP',
        'GMT_IS_SURFACE',
    ]

    data_modes = [
        'GMT_CONTAINER_ONLY',
        'GMT_OUTPUT',
    ]

    grid_registrations = [
        'GMT_GRID_PIXEL_REG',
        'GMT_GRID_NODE_REG',
    ]

    # The minimum version of GMT required
    required_version = '6.0.0'

    # Map numpy dtypes to GMT types
    _dtypes = {
        'float64': 'GMT_DOUBLE',
        'float32': 'GMT_FLOAT',
        'int64': 'GMT_LONG',
        'int32': 'GMT_INT',
        'uint64': 'GMT_ULONG',
        'uint32': 'GMT_UINT',
    }

    def __init__(self):
        self._logfile = None
        self._session_id = None
        self._libgmt = load_libgmt()

    @property
    def current_session(self):
        """
        The C void pointer for the current open GMT session.

        Raises
        ------
        GMTCLibNoSessionError
            If trying to access without a currently open GMT session (i.e.,
            outside of the context manager).

        """
        if self._session_id is None:
            raise GMTCLibNoSessionError(' '.join([
                "No currently open session.",
                "Call methods only inside a 'with' block."]))
        return self._session_id

    @current_session.setter
    def current_session(self, session):
        """
        Set the session void pointer.
        """
        self._session_id = session

    @property
    def info(self):
        """
        Dictionary with the GMT version and default paths and parameters.
        """
        infodict = {
            'version': self.get_default('API_VERSION'),
            'padding': self.get_default("API_PAD"),
            'binary dir': self.get_default("API_BINDIR"),
            'share dir': self.get_default("API_SHAREDIR"),
            # This segfaults for some reason
            # 'data dir': self.get_default("API_DATADIR"),
            'plugin dir': self.get_default("API_PLUGINDIR"),
            'library path': self.get_default("API_LIBRARY"),
            'cores': self.get_default("API_CORES"),
            'image layout': self.get_default("API_IMAGE_LAYOUT"),
            'grid layout': self.get_default("API_GRID_LAYOUT"),
        }
        return infodict

    def __enter__(self):
        """
        Start the GMT session and keep the session argument.
        """
        self.current_session = self.create_session('gmt-python-session')
        # Need to store the version info because 'get_default' won't work after
        # the session is destroyed.
        version = self.info['version']
        if Version(version) < Version(self.required_version):
            self._cleanup_session()
            raise GMTVersionError(
                "Using an incompatible GMT version {}. Must be newer than {}."
                .format(version, self.required_version))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the session when exiting the context.
        """
        self._cleanup_session()

    def _cleanup_session(self):
        """
        Destroy the current session and set the stored session to None
        """
        try:
            self.destroy_session(self.current_session)
        finally:
            self.current_session = None

    def create_session(self, session_name):
        """
        Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

        It is a C void pointer containing the current session information and
        cannot be accessed directly.

        Remember to terminate the current session using
        :func:`gmt.clib.LibGMT.destroy_session` before creating a new one.

        Parameters
        ----------
        session_name : str
            A name for this session. Doesn't really affect the outcome.

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
        print_func = None
        padding = self.get_constant('GMT_PAD_DEFAULT')
        session_type = self.get_constant('GMT_SESSION_EXTERNAL')
        session = c_create_session(session_name.encode(), padding,
                                   session_type, print_func)

        if session is None:
            raise GMTCLibError("Failed to create a GMT API void pointer.")

        return session

    def destroy_session(self, session):
        """
        Terminate and free the memory of a registered ``GMTAPI_CTRL`` session.

        The session is created and consumed by the C API modules and needs to
        be freed before creating a new. Otherwise, some of the configuration
        files might be left behind and can influence subsequent API calls.

        Parameters
        ----------
        session : C void pointer (returned by ctypes as an integer)
            The active session object produced by
            :func:`gmt.clib.LibGMT.create_session`.
        libgmt : :py:class:`ctypes.CDLL`
            The :py:class:`ctypes.CDLL` instance for the libgmt shared library.

        """
        c_destroy_session = self._libgmt.GMT_Destroy_Session
        c_destroy_session.argtypes = [ctypes.c_void_p]
        c_destroy_session.restype = ctypes.c_int

        status = c_destroy_session(session)
        if status:
            raise GMTCLibError('Failed to destroy GMT API session')

    def get_constant(self, name):
        """
        Get the value of a constant (C enum) from gmt_resources.h

        Used to set configuration values for other API calls. Wraps
        ``GMT_Get_Enum``.

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

    def get_default(self, name):
        """
        Get the value of a GMT default parameter (library version, paths, etc).

        Possible default parameter names include:

        * ``"API_VERSION"``: The GMT version
        * ``"API_PAD"``: The grid padding setting
        * ``"API_BINDIR"``: The binary file directory
        * ``"API_SHAREDIR"``: The share directory
        * ``"API_DATADIR"``: The data directory
        * ``"API_PLUGINDIR"``: The plugin directory
        * ``"API_LIBRARY"``: The core library path
        * ``"API_CORES"``: The number of cores
        * ``"API_IMAGE_LAYOUT"``: The image/band layout
        * ``"API_GRID_LAYOUT"``: The grid layout

        Parameters
        ----------
        name : str
            The name of the default parameter (e.g., ``"API_VERSION"``)

        Returns
        -------
        value : str
            The default value for the parameter.

        Raises
        ------
        GMTCLibError
            If the parameter doesn't exist.

        """
        c_get_default = self._libgmt.GMT_Get_Default
        c_get_default.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                  ctypes.c_char_p]
        c_get_default.restype = ctypes.c_int

        # Make a string buffer to get a return value
        value = ctypes.create_string_buffer(10000)

        status = c_get_default(self.current_session, name.encode(), value)

        if status != 0:
            raise GMTCLibError(
                "Error getting default value for '{}' (error code {})."
                .format(name, status))

        return value.value.decode()

    @contextmanager
    def log_to_file(self, logfile=None):
        """
        Set the next API call in this session to log to a file.

        Use it as a context manager (in a ``with`` block) to capture the error
        messages from GMT API calls. Mostly useful with ``GMT_Call_Module``
        because most others don't print error messages.

        The log file will be deleted when exiting the ``with`` block.

        Calls the GMT API function ``GMT_Handle_Messages`` using
        ``GMT_LOG_ONCE`` mode (to only log errors from the next API call).
        Only works for a **single API call**, so make calls like
        ``get_constant`` outside of the ``with`` block.

        Parameters
        ----------
        * logfile : str or None
            The name of the logfile. If ``None`` (default),
            the file name is automatically generated by the tempfile module.

        Examples
        --------

        >>> with LibGMT() as lib:
        ...     mode = lib.get_constant('GMT_MODULE_CMD')
        ...     with lib.log_to_file() as logfile:
        ...         status = lib._libgmt.GMT_Call_Module(
        ...             lib.current_session, 'info'.encode(), mode,
        ...             'bogus-file.bla'.encode())
        ...         with open(logfile) as flog:
        ...             print(flog.read().strip())
        gmtinfo [ERROR]: Error for input file: No such file (bogus-file.bla)

        """
        c_handle_messages = self._libgmt.GMT_Handle_Messages
        c_handle_messages.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                      ctypes.c_uint, ctypes.c_char_p]
        c_handle_messages.restype = ctypes.c_int

        if logfile is None:
            tmp_file = NamedTemporaryFile(prefix='gmt-python-', suffix='.log',
                                          delete=False)
            logfile = tmp_file.name
            tmp_file.close()

        status = c_handle_messages(self.current_session,
                                   self.get_constant('GMT_LOG_ONCE'),
                                   self.get_constant('GMT_IS_FILE'),
                                   logfile.encode())
        if status != 0:
            msg = "Failed to set logging to file '{}' (error: {}).".format(
                logfile, status)
            raise GMTCLibError(msg)

        # The above is called when entering a 'with' statement
        yield logfile

        # Clean up when exiting the 'with' statement
        os.remove(logfile)

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
            If the returned status code of the function is non-zero.

        """
        c_call_module = self._libgmt.GMT_Call_Module
        c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                  ctypes.c_int, ctypes.c_void_p]
        c_call_module.restype = ctypes.c_int

        mode = self.get_constant('GMT_MODULE_CMD')
        # If there is no open session, this will raise an exception. Can' let
        # it happen inside the 'with' otherwise the logfile won't be deleted.
        session = self.current_session
        with self.log_to_file() as logfile:
            status = c_call_module(session, module.encode(), mode,
                                   args.encode())
            # Get the error message inside the with block before the log file
            # is deleted
            with open(logfile) as flog:
                log = flog.read().strip()
        # Raise the exception outside the log 'with' to make sure the logfile
        # is cleaned.
        if status != 0:
            if log == '':
                msg = "Invalid GMT module name '{}'.".format(module)
            else:
                msg = '\n'.join([
                    "Command '{}' failed:".format(module),
                    "---------- Error log ----------",
                    log,
                    "-------------------------------",
                ])
            raise GMTCLibError(msg)

    def create_data(self, family, geometry, mode, **kwargs):
        """
        Create an empty GMT data container.

        Parameters
        ----------
        family : str
            A valid GMT data family name (e.g., ``'GMT_IS_DATASET'``). See the
            ``data_families`` attribute for valid names.
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). See the
            ``data_geometries`` attribute for valid names.
        mode : str
            A valid GMT data mode (e.g., ``'GMT_OUTPUT'``). See the
            ``data_modes`` attribute for valid names.
        dim : list of 4 integers
            The dimensions of the dataset. See the documentation for the GMT C
            API function ``GMT_Create_Data`` (``src/gmt_api.c``) for the full
            range of options regarding 'dim'. If ``None``, will pass in the
            NULL pointer.
        ranges : list of 4 floats
            The dataset extent. Also a bit of a complicated argument. See the C
            function documentation. It's called ``range`` in the C function but
            it would conflict with the Python built-in ``range`` function.
        inc : list of 2 floats
            The increments between points of the dataset. See the C function
            documentation.
        registration : int
            The node registration (what the coordinates mean). Can be
            ``'GMT_GRID_PIXEL_REG'`` or ``'GMT_GRID_NODE_REG'``. Defaults to
            ``'GMT_GRID_NODE_REG'``.
        pad : int
            The grid padding. Defaults to ``GMT_PAD_DEFAULT``.

        Returns
        -------
        data_ptr : int
            A ctypes pointer (an integer) to the allocated ``GMT_Dataset``
            object.

        """
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

        family_int = self._parse_constant(family, valid=self.data_families,
                                          valid_modifiers=self.data_vias)
        mode_int = self._parse_constant(mode, valid=self.data_modes)
        geometry_int = self._parse_constant(
            geometry, valid=self.data_geometries)
        registration_int = self._parse_constant(
            kwargs.get('registration', 'GMT_GRID_NODE_REG'),
            valid=self.grid_registrations)

        # Convert dim, ranges, and inc to ctypes arrays if given (will be None
        # if not given to represent NULL pointers)
        dim = kwargs_to_ctypes_array('dim', kwargs, ctypes.c_uint64*4)
        ranges = kwargs_to_ctypes_array('ranges', kwargs, ctypes.c_double*4)
        inc = kwargs_to_ctypes_array('inc', kwargs, ctypes.c_double*2)

        # Use a NULL pointer (None) for existing data to indicate that the
        # container should be created empty. Fill it in later using put_vector
        # and put_matrix.
        data_ptr = c_create_data(
            self.current_session,
            family_int,
            geometry_int,
            mode_int,
            dim,
            ranges,
            inc,
            registration_int,
            self._parse_pad(family, kwargs),
            None)

        if data_ptr is None:
            raise GMTCLibError("Failed to create an empty GMT data pointer.")

        return data_ptr

    def _parse_pad(self, family, kwargs):
        """
        Parse and return an appropriate value for pad if none is given.

        Pad is a bit tricky because, for matrix types, pad control the matrix
        ordering (row or column major). Using the default pad will set it to
        column major and mess things up with the numpy arrays.
        """
        pad = kwargs.get('pad', None)
        if pad is None:
            if 'MATRIX' in family:
                pad = 0
            else:
                pad = self.get_constant('GMT_PAD_DEFAULT')
        return pad

    def _parse_constant(self, constant, valid, valid_modifiers=None):
        """
        Parse a constant, convert it to an int, and validate it.

        The GMT C API takes certain defined constants, like ``'GMT_IS_GRID'``,
        that need to be validated and converted to integer values using
        :meth:`~gmt.clib.LibGMT.get_constant`.

        The constants can also take a modifier by appending another constant
        name, e.g. ``'GMT_IS_GRID|GMT_VIA_MATRIX'``. The two parts must be
        converted separately and their values are added.

        If valid modifiers are not given, then will assume that modifiers are
        not allowed. In this case, will raise a
        :class:`~gmt.exceptions.GMTInvalidInput` exception if given a modifier.

        Parameters
        ----------
        constant : str
            The name of a valid GMT API constant, with an optional modifier.
        valid : list of str
            A list of valid values for the constant. Will raise a
            :class:`~gmt.exceptions.GMTInvalidInput` exception if the given
            value is not on the list.
        """
        parts = constant.split('|')
        name = parts[0]
        nmodifiers = len(parts) - 1
        if nmodifiers > 1:
            raise GMTInvalidInput(
                "Only one modifier is allowed in constants, {} given: '{}'"
                .format(nmodifiers, constant))
        if nmodifiers > 0 and valid_modifiers is None:
            raise GMTInvalidInput(
                "Constant modifiers not allowed since valid values were not " +
                "given: '{}'".format(constant))
        if name not in valid:
            raise GMTInvalidInput(
                "Invalid constant argument '{}'. Must be one of {}."
                .format(name, str(valid)))
        if nmodifiers > 0 and valid_modifiers is not None \
                and parts[1] not in valid_modifiers:
            raise GMTInvalidInput(
                "Invalid constant modifier '{}'. Must be one of {}."
                .format(parts[1], str(valid_modifiers)))
        integer_value = sum(self.get_constant(part) for part in parts)
        return integer_value

    def _check_dtype_and_dim(self, array, ndim):
        """
        Check that a numpy array has the given dimensions and is a valid data
        type.

        Parameters
        ----------
        array : numpy array
            The array to be tested.
        ndim : int
            The desired dimension of the array.

        Returns
        -------
        gmt_type : int
            The GMT constant value representing this data type.

        Raises
        ------
        GMTCLibError
            If the array has the wrong dimensions or is an unsupported data
            type.

        Examples
        --------

        >>> import numpy as np
        >>> data = np.array([1, 2, 3], dtype='float64')
        >>> with LibGMT() as lib:
        ...     gmttype = lib._check_dtype_and_dim(data, ndim=1)
        ...     gmttype == lib.get_constant('GMT_DOUBLE')
        True
        >>> data = np.ones((5, 2), dtype='float32')
        >>> with LibGMT() as lib:
        ...     gmttype = lib._check_dtype_and_dim(data, ndim=2)
        ...     gmttype == lib.get_constant('GMT_FLOAT')
        True

        """
        if array.dtype.name not in self._dtypes:
            raise GMTInvalidInput(
                "Unsupported numpy data type '{}'.".format(array.dtype.name)
            )
        if array.ndim != ndim:
            raise GMTInvalidInput(
                "Expected a numpy 1d array, got {}d.".format(array.ndim)
            )
        return self.get_constant(self._dtypes[array.dtype.name])

    def put_vector(self, dataset, column, vector):
        """
        Attach a numpy 1D array as a column on a GMT dataset.

        Use this functions to attach numpy array data to a GMT dataset and pass
        it to GMT modules. Wraps ``GMT_Put_Vector``.

        The dataset must be created by :meth:`~gmt.clib.LibGMT.create_data`
        first. Use ``family='GMT_IS_DATASET|GMT_VIA_VECTOR'``.

        Not at all numpy dtypes are supported, only: float64, float32, int64,
        int32, uint64, and uint32.

        .. warning::
            The numpy array must be C contiguous in memory. If it comes from a
            column slice of a 2d array, for example, you will have to make a
            copy. Use :func:`numpy.ascontiguousarray` to make sure your vector
            is contiguous (it won't copy if it already is).

        Parameters
        ----------
        dataset : :py:class:`ctypes.c_void_p`
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`~gmt.clib.LibGMT.create_data`.
        column : int
            The column number of this vector in the dataset (starting from 0).
        vector : numpy 1d-array
            The array that will be attached to the dataset. Must be a 1d C
            contiguous array.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Vector`` exits with status !=
            0.

        """
        c_put_vector = self._libgmt.GMT_Put_Vector
        c_put_vector.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                 ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
        c_put_vector.restype = ctypes.c_int

        gmt_type = self._check_dtype_and_dim(vector, ndim=1)
        vector_pointer = vector.ctypes.data_as(ctypes.c_void_p)
        status = c_put_vector(self.current_session, dataset, column, gmt_type,
                              vector_pointer)
        if status != 0:
            raise GMTCLibError(
                ' '.join([
                    "Failed to put vector of type {}".format(vector.dtype),
                    "in column {} of dataset.".format(column),
                ])
            )

    def put_matrix(self, dataset, matrix, pad=0):
        """
        Attach a numpy 2D array to a GMT dataset.

        Use this functions to attach numpy array data to a GMT dataset and pass
        it to GMT modules. Wraps ``GMT_Put_Matrix``.

        The dataset must be created by :meth:`~gmt.clib.LibGMT.create_data`
        first. Use ``|GMT_VIA_MATRIX'`` in the family.

        Not at all numpy dtypes are supported, only: float64, float32, int64,
        int32, uint64, and uint32.

        .. warning::
            The numpy array must be C contiguous in memory. Use
            :func:`numpy.ascontiguousarray` to make sure your vector is
            contiguous (it won't copy if it already is).

        Parameters
        ----------
        dataset : :py:class:`ctypes.c_void_p`
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`~gmt.clib.LibGMT.create_data`.
        matrix : numpy 2d-array
            The array that will be attached to the dataset. Must be a 2d C
            contiguous array.
        pad : int
            The amount of padding that should be added to the matrix. Use when
            creating grids for modules that require padding.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Matrix`` exits with status !=
            0.

        """
        c_put_matrix = self._libgmt.GMT_Put_Matrix
        c_put_matrix.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                 ctypes.c_uint, ctypes.c_int, ctypes.c_void_p]
        c_put_matrix.restype = ctypes.c_int

        gmt_type = self._check_dtype_and_dim(matrix, ndim=2)
        matrix_pointer = matrix.ctypes.data_as(ctypes.c_void_p)
        status = c_put_matrix(self.current_session, dataset, gmt_type, pad,
                              matrix_pointer)
        if status != 0:
            raise GMTCLibError(
                "Failed to put matrix of type {}.".format(matrix.dtype))

    def write_data(self, family, geometry, mode, wesn, output, data):
        """
        Write a GMT data container to a file.

        The data container should be created by
        :meth:`~gmt.clib.LibGMT.create_data`.

        Wraps ``GMT_Write_Data`` but only allows writing to a file. So the
        ``method`` argument is omitted.

        Parameters
        ----------
        family : str
            A valid GMT data family name (e.g., ``'GMT_IS_DATASET'``). See the
            ``data_families`` attribute for valid names. Don't use the
            ``GMT_VIA_VECTOR`` or ``GMT_VIA_MATRIX`` constructs for this. Use
            ``GMT_IS_VECTOR`` and ``GMT_IS_MATRIX`` instead.
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). See the
            ``data_geometries`` attribute for valid names.
        mode : str
            How the data is to be written to the file. This option varies
            depending on the given family. See the GMT API documentation for
            details.
        wesn : list or numpy array
            [xmin, xmax, ymin, ymax, zmin, zmax] of the data. Must have 6
            elements.
        output : str
            The output file name.
        data : :py:class:`ctypes.c_void_p`
            Pointer to the data container created by
            :meth:`~gmt.clib.LibGMT.create_data`.

        Raises
        ------
        GMTCLibError
            For invalid input arguments or if the GMT API functions returns a
            non-zero status code.

        """
        c_write_data = self._libgmt.GMT_Write_Data
        c_write_data.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint,
                                 ctypes.c_uint, ctypes.c_uint,
                                 ctypes.POINTER(ctypes.c_double),
                                 ctypes.c_char_p, ctypes.c_void_p]
        c_write_data.restype = ctypes.c_int

        family_int = self._parse_constant(family, valid=self.data_families,
                                          valid_modifiers=self.data_vias)
        geometry_int = self._parse_constant(geometry,
                                            valid=self.data_geometries)
        status = c_write_data(self.current_session, family_int,
                              self.get_constant('GMT_IS_FILE'), geometry_int,
                              self.get_constant(mode),
                              (ctypes.c_double*6)(*wesn), output.encode(),
                              data)
        if status != 0:
            raise GMTCLibError(
                "Failed to write dataset to '{}'".format(output))

    @contextmanager
    def open_virtual_file(self, family, geometry, direction, data):
        """
        Open a GMT Virtual File to pass data to and from a module.

        GMT uses a virtual file scheme to pass in data to API modules. Use it
        to pass in your GMT data structure (created using
        :meth:`~gmt.clib.LibGMT.create_data`) to a module that expects an input
        or output file.

        Use in a ``with`` block. Will automatically close the virtual file when
        leaving the ``with`` block. Because of this, no wrapper for
        ``GMT_Close_VirtualFile`` is provided.

        Parameters
        ----------
        family : str
            A valid GMT data family name (e.g., ``'GMT_IS_DATASET'``). Should
            be the same as the one you used to create your data structure.
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). Should
            be the same as the one you used to create your data structure.
        direction : str
            Either ``'GMT_IN'`` or ``'GMT_OUT'`` to indicate if passing data to
            GMT or getting it out of GMT, respectively.
        data : int
            The ctypes void pointer to your GMT data structure.

        Yields
        ------
        vfname : str
            The name of the virtual file that you can pass to a GMT module.

        Examples
        --------

        >>> from gmt.helpers import GMTTempFile
        >>> import os
        >>> import numpy as np
        >>> x = np.array([0, 1, 2, 3, 4])
        >>> y = np.array([5, 6, 7, 8, 9])
        >>> with LibGMT() as lib:
        ...     family = 'GMT_IS_DATASET|GMT_VIA_VECTOR'
        ...     geometry = 'GMT_IS_POINT'
        ...     dataset = lib.create_data(
        ...         family=family,
        ...         geometry=geometry,
        ...         mode='GMT_CONTAINER_ONLY',
        ...         dim=[2, 5, 1, 0],  # columns, lines, segments, type
        ...     )
        ...     lib.put_vector(dataset, column=0, vector=x)
        ...     lib.put_vector(dataset, column=1, vector=y)
        ...     # Add the dataset to a virtual file
        ...     vfargs = (family, geometry, 'GMT_IN', dataset)
        ...     with lib.open_virtual_file(*vfargs) as vfile:
        ...         # Send the output to a temp file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             args = '{} ->{}'.format(vfile, ofile.name)
        ...             lib.call_module('info', args)
        ...             print(ofile.read().strip())
        <vector memory>: N = 5 <0/4> <5/9>

        """
        c_open_virtualfile = self._libgmt.GMT_Open_VirtualFile
        c_open_virtualfile.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                       ctypes.c_uint, ctypes.c_uint,
                                       ctypes.c_void_p, ctypes.c_char_p]
        c_open_virtualfile.restype = ctypes.c_int

        c_close_virtualfile = self._libgmt.GMT_Close_VirtualFile
        c_close_virtualfile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        c_close_virtualfile.restype = ctypes.c_int

        family_int = self._parse_constant(family, valid=self.data_families,
                                          valid_modifiers=self.data_vias)
        geometry_int = self._parse_constant(geometry,
                                            valid=self.data_geometries)
        direction_int = self._parse_constant(
            direction, valid=['GMT_IN', 'GMT_OUT'],
            valid_modifiers=['GMT_IS_REFERENCE'])

        buff = ctypes.create_string_buffer(self.get_constant('GMT_STR16'))

        status = c_open_virtualfile(self.current_session, family_int,
                                    geometry_int, direction_int, data, buff)

        if status != 0:
            raise GMTCLibError("Failed to create a virtual file.")

        vfname = buff.value.decode()

        try:
            yield vfname
        finally:
            status = c_close_virtualfile(self.current_session, vfname.encode())
            if status != 0:
                raise GMTCLibError(
                    "Failed to close virtual file '{}'.".format(vfname))

    @contextmanager
    def vectors_to_vfile(self, *vectors):
        """
        Store 1d arrays in a GMT virtual file to use as a module input.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        Use this instead of creating GMT Datasets and Virtual Files by hand
        with :meth:`~gmt.clib.LibGMT.create_data`,
        :meth:`~gmt.clib.LibGMT.put_vector`, and
        :meth:`~gmt.clib.LibGMT.open_virtual_file`

        The virtual file will contain the arrays as ``GMT Vector`` structures.

        If the arrays are C contiguous blocks of memory, they will be passed
        without copying to GMT. If they are not (e.g., they are columns of a 2D
        array), they will need to be copied to a contiguous block.

        Parameters
        ----------
        vectors : 1d arrays
            The vectors that will be included in the array. All must be of the
            same size.

        Yields
        ------
        vfile : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from gmt.helpers import GMTTempFile
        >>> import numpy as np
        >>> import pandas as pd
        >>> x = [1, 2, 3]
        >>> y = np.array([4, 5, 6])
        >>> z = pd.Series([7, 8, 9])
        >>> with LibGMT() as lib:
        ...     with lib.vectors_to_vfile(x, y, z) as vfile:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             args = '{} ->{}'.format(vfile, ofile.name)
        ...             lib.call_module('info', args)
        ...             print(ofile.read().strip())
        <vector memory>: N = 3 <1/3> <4/6> <7/9>

        """
        # Conversion to a C-contiguous array needs to be done here and not in
        # put_matrix because we need to maintain a reference to the copy while
        # it is being used by the C API. Otherwise, the array would be garbage
        # collected and the memory freed. Creating it in this context manager
        # guarantees that the copy will be around until the virtual file is
        # closed.
        # The conversion is implicit in vectors_to_arrays.
        arrays = vectors_to_arrays(vectors)

        columns = len(arrays)
        rows = len(arrays[0])
        if not all(len(i) == rows for i in arrays):
            raise GMTInvalidInput("All arrays must have same size.")

        family = 'GMT_IS_DATASET|GMT_VIA_VECTOR'
        geometry = 'GMT_IS_POINT'

        dataset = self.create_data(family, geometry, mode='GMT_CONTAINER_ONLY',
                                   dim=[columns, rows, 1, 0])

        for col, array in enumerate(arrays):
            self.put_vector(dataset, column=col, vector=array)

        vf_args = (family, geometry, 'GMT_IN', dataset)
        with self.open_virtual_file(*vf_args) as vfile:
            yield vfile

    @contextmanager
    def matrix_to_vfile(self, matrix):
        """
        Store a 2d array in a GMT virtual file to use as a module input.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        The virtual file will contain the array as a ``GMT_MATRIX``.

        **Not meant for creating GMT Grids**. The grid requires more metadata
        than just the data matrix. This creates a Dataset (table).

        Use this instead of creating GMT Datasets and Virtual Files by hand
        with :meth:`~gmt.clib.LibGMT.create_data`,
        :meth:`~gmt.clib.LibGMT.put_matrix`, and
        :meth:`~gmt.clib.LibGMT.open_virtual_file`

        The matrix must be C contiguous in memory. If it is not (e.g., it is a
        slice of a larger array), the array will be copied to make sure it is.

        It might be more efficient than using
        :meth:`~gmt.clib.LibGMT.vectors_to_vfile` if your data are columns of a
        2D array. In these cases, ``vectors_to_vfile`` will have to duplicate
        the memory of your array in order for columns to be C contiguous.

        Parameters
        ----------
        matrix : 2d array
            The matrix that will be included in the Dataset.

        Yields
        ------
        vfile : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from gmt.helpers import GMTTempFile
        >>> import numpy as np
        >>> data = np.arange(12).reshape((4, 3))
        >>> print(data)
        [[ 0  1  2]
         [ 3  4  5]
         [ 6  7  8]
         [ 9 10 11]]
        >>> with LibGMT() as lib:
        ...     with lib.matrix_to_vfile(data) as vfile:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             args = '{} ->{}'.format(vfile, ofile.name)
        ...             lib.call_module('info', args)
        ...             print(ofile.read().strip())
        <matrix memory>: N = 4 <0/9> <1/10> <2/11>

        """
        # Conversion to a C-contiguous array needs to be done here and not in
        # put_matrix because we need to maintain a reference to the copy while
        # it is being used by the C API. Otherwise, the array would be garbage
        # collected and the memory freed. Creating it in this context manager
        # guarantees that the copy will be around until the virtual file is
        # closed.
        matrix = as_c_contiguous(matrix)
        rows, columns = matrix.shape

        family = 'GMT_IS_DATASET|GMT_VIA_MATRIX'
        geometry = 'GMT_IS_POINT'

        dataset = self.create_data(family, geometry, mode='GMT_CONTAINER_ONLY',
                                   dim=[columns, rows, 1, 0])

        self.put_matrix(dataset, matrix)

        vf_args = (family, geometry, 'GMT_IN', dataset)
        with self.open_virtual_file(*vf_args) as vfile:
            yield vfile

    @contextmanager
    def grid_to_vfile(self, grid):
        """
        Store a grid in a GMT virtual file to use as a module input.

        Used to pass grid data into GMT modules. Grids must be
        ``xarray.DataArray`` instances.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        The virtual file will contain the grid as a ``GMT_MATRIX``.

        Use this instead of creating ``GMT_GRID`` and virtual files by hand
        with :meth:`~gmt.clib.LibGMT.create_data`,
        :meth:`~gmt.clib.LibGMT.put_matrix`, and
        :meth:`~gmt.clib.LibGMT.open_virtual_file`

        The grid data matrix must be C contiguous in memory. If it is not
        (e.g., it is a slice of a larger array), the array will be copied to
        make sure it is.

        Parameters
        ----------
        grid : xarray.DataArraw
            The grid that will be included in the virtual file.

        Yields
        ------
        vfile : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from gmt.datasets import load_earth_relief
        >>> from gmt.helpers import GMTTempFile
        >>> data = load_earth_relief(resolution='60m')
        >>> print(data.shape)
        (181, 361)
        >>> print(data.lon.values.min(), data.lon.values.max())
        -180.0 180.0
        >>> print(data.lat.values.min(), data.lat.values.max())
        -90.0 90.0
        >>> print(data.values.min(), data.values.max())
        -8425.0 5551.0
        >>> with LibGMT() as lib:
        ...     with lib.grid_to_vfile(data) as vfile:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             args = '{} -L0 -Cn ->{}'.format(vfile, ofile.name)
        ...             lib.call_module('grdinfo', args)
        ...             print(ofile.read().strip())
        -180 180 -90 90 -8425 5551 1 1 361 181
        >>> # The output is: w e s n z0 z1 dx dy n_columns n_rows

        """
        # Conversion to a C-contiguous array needs to be done here and not in
        # put_matrix because we need to maintain a reference to the copy while
        # it is being used by the C API. Otherwise, the array would be garbage
        # collected and the memory freed. Creating it in this context manager
        # guarantees that the copy will be around until the virtual file is
        # closed.
        # The conversion is implicit in dataarray_to_matrix.
        matrix, region, inc = dataarray_to_matrix(grid)
        family = 'GMT_IS_GRID|GMT_VIA_MATRIX'
        geometry = 'GMT_IS_SURFACE'
        gmt_grid = self.create_data(family, geometry,
                                    mode='GMT_CONTAINER_ONLY',
                                    ranges=region, inc=inc)
        self.put_matrix(gmt_grid, matrix)
        args = (family, geometry, 'GMT_IN|GMT_IS_REFERENCE', gmt_grid)
        with self.open_virtual_file(*args) as vfile:
            yield vfile

    def extract_region(self):
        """
        Extract the WESN bounding box of the currently active figure.

        Retrieves the information from the PostScript file, so it works for
        country codes as well.

        Returns
        -------
        * wesn : 1d array
            A 1D numpy array with the west, east, south, and north dimensions
            of the current figure.

        Examples
        --------

        >>> import gmt
        >>> fig = gmt.Figure()
        >>> fig.coast(region=[0, 10, -20, -10], projection="M6i", frame=True,
        ...           land='black')
        >>> with LibGMT() as lib:
        ...     wesn = lib.extract_region()
        >>> print(', '.join(['{:.2f}'.format(x) for x in wesn]))
        0.00, 10.00, -20.00, -10.00

        Using ISO country codes for the regions (for example ``'US.HI'`` for
        Hawaii):

        >>> fig = gmt.Figure()
        >>> fig.coast(region='US.HI', projection="M6i", frame=True,
        ...           land='black')
        >>> with LibGMT() as lib:
        ...     wesn = lib.extract_region()
        >>> print(', '.join(['{:.2f}'.format(x) for x in wesn]))
        -164.71, -154.81, 18.91, 23.58

        The country codes can have an extra argument that rounds the region a
        multiple of the argument (for example, ``'US.HI+r5'`` will round the
        region to multiples of 5):

        >>> fig = gmt.Figure()
        >>> fig.coast(region='US.HI+r5', projection="M6i", frame=True,
        ...           land='black')
        >>> with LibGMT() as lib:
        ...     wesn = lib.extract_region()
        >>> print(', '.join(['{:.2f}'.format(x) for x in wesn]))
        -165.00, -150.00, 15.00, 25.00

        """
        c_extract_region = self._libgmt.GMT_Extract_Region
        c_extract_region.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                     ctypes.POINTER(ctypes.c_double)]
        c_extract_region.restype = ctypes.c_int

        wesn = np.empty(4, dtype=np.float64)
        # Use NaNs so that we can know if GMT didn't change the array
        wesn[:] = np.nan
        wesn_pointer = wesn.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        # The second argument to GMT_Extract_Region is a file pointer to a
        # PostScript file. It's only valid in classic mode. Use None to get a
        # NULL pointer instead.
        status = c_extract_region(self.current_session, None, wesn_pointer)
        if status != 0:
            raise GMTCLibError("Failed to extract region from current figure.")
        return wesn
