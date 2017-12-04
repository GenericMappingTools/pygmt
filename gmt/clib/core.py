"""
ctypes wrappers for core functions from the C API
"""
import os
import ctypes
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

from ..exceptions import GMTCLibError, GMTCLibNoSessionError
from .utils import load_libgmt, kwargs_to_ctypes_array


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

    Parameters
    ----------
    libname : str
        The name of the GMT shared library **without the extension**. Can be a
        full path to the library or just the library name.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).
    GMTCLibNoSessionError
        If you try to call a method outside of a 'with' block.

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

    # Map numpy dtypes to GMT types
    _dtypes = {
        'float64': 'GMT_DOUBLE',
        'float32': 'GMT_FLOAT',
        'int64': 'GMT_LONG',
        'int32': 'GMT_INT',
        'uint64': 'GMT_ULONG',
        'uint32': 'GMT_UINT',
    }

    def __init__(self, libname='libgmt'):
        self._logfile = None
        self._session_id = None
        self._libgmt = None
        self._c_get_enum = None
        self._c_create_session = None
        self._c_destroy_session = None
        self._c_call_module = None
        self._c_create_data = None
        self._c_handle_messages = None
        self._c_put_vector = None
        self._c_put_matrix = None
        self._c_write_data = None
        self._c_open_virtualfile = None
        self._c_close_virtualfile = None
        self._bind_clib_functions(libname)

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

    def _bind_clib_functions(self, libname):
        """
        Loads libgmt and binds the library functions to class attributes.

        Sets the argument and return types for the functions.
        """
        self._libgmt = load_libgmt(libname)

        self._c_create_session = self._libgmt.GMT_Create_Session
        self._c_create_session.argtypes = [ctypes.c_char_p, ctypes.c_uint,
                                           ctypes.c_uint, ctypes.c_void_p]
        self._c_create_session.restype = ctypes.c_void_p

        self._c_destroy_session = self._libgmt.GMT_Destroy_Session
        self._c_destroy_session.argtypes = [ctypes.c_void_p]
        self._c_destroy_session.restype = ctypes.c_int

        self._c_get_enum = self._libgmt.GMT_Get_Enum
        self._c_get_enum.argtypes = [ctypes.c_char_p]
        self._c_get_enum.restype = ctypes.c_int

        self._c_call_module = self._libgmt.GMT_Call_Module
        self._c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                        ctypes.c_int, ctypes.c_void_p]
        self._c_call_module.restype = ctypes.c_int

        self._c_create_data = self._libgmt.GMT_Create_Data
        self._c_create_data.argtypes = [
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
        self._c_create_data.restype = ctypes.c_void_p

        self._c_handle_messages = self._libgmt.GMT_Handle_Messages
        self._c_handle_messages.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                            ctypes.c_uint, ctypes.c_char_p]
        self._c_handle_messages.restype = ctypes.c_int

        self._c_put_vector = self._libgmt.GMT_Put_Vector
        self._c_put_vector.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_uint, ctypes.c_uint,
                                       ctypes.c_void_p]
        self._c_put_vector.restype = ctypes.c_int

        self._c_put_matrix = self._libgmt.GMT_Put_Matrix
        self._c_put_matrix.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_uint, ctypes.c_void_p]
        self._c_put_matrix.restype = ctypes.c_int

        self._c_write_data = self._libgmt.GMT_Write_Data
        self._c_write_data.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                       ctypes.c_uint, ctypes.c_uint,
                                       ctypes.c_uint,
                                       ctypes.POINTER(ctypes.c_double),
                                       ctypes.c_char_p, ctypes.c_void_p]
        self._c_write_data.restype = ctypes.c_int

        self._c_open_virtualfile = self._libgmt.GMT_Open_VirtualFile
        self._c_open_virtualfile.argtypes = [ctypes.c_void_p,
                                             ctypes.c_uint,
                                             ctypes.c_uint,
                                             ctypes.c_uint,
                                             ctypes.c_void_p,
                                             ctypes.c_char_p]
        self._c_open_virtualfile.restype = ctypes.c_int

        self._c_close_virtualfile = self._libgmt.GMT_Close_VirtualFile
        self._c_close_virtualfile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self._c_close_virtualfile.restype = ctypes.c_int

    def __enter__(self):
        """
        Start the GMT session and keep the session argument.
        """
        self.current_session = self.create_session('gmt-python-session')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the session when exiting the context.
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
        # None is passed in place of the print function pointer. It becomes the
        # NULL pointer when passed to C, prompting the C API to use the default
        # print function.
        print_func = None
        padding = self.get_constant('GMT_PAD_DEFAULT')
        session_type = self.get_constant('GMT_SESSION_EXTERNAL')
        session = self._c_create_session(session_name.encode(), padding,
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
        libgmt : ctypes.CDLL
            The ``ctypes.CDLL`` instance for the libgmt shared library.

        """
        status = self._c_destroy_session(session)
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
        value = self._c_get_enum(name.encode())

        if value is None or value == -99999:
            raise GMTCLibError(
                "Constant '{}' doesn't exits in libgmt.".format(name))

        return value

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
        ...         status = lib._c_call_module(lib.current_session,
        ...                                     'info'.encode(),
        ...                                     mode,
        ...                                     'bogus-file.bla'.encode())
        ...         with open(logfile) as flog:
        ...             print(flog.read().strip())
        gmtinfo [ERROR]: Error for input file: No such file (bogus-file.bla)

        """
        if logfile is None:
            tmp_file = NamedTemporaryFile(prefix='gmt-python-', suffix='.log',
                                          delete=False)
            logfile = tmp_file.name
            tmp_file.close()

        status = self._c_handle_messages(self.current_session,
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
        mode = self.get_constant('GMT_MODULE_CMD')
        # If there is no open session, this will raise an exception. Can' let
        # it happen inside the 'with' otherwise the logfile won't be deleted.
        session = self.current_session
        with self.log_to_file() as logfile:
            status = self._c_call_module(session, module.encode(), mode,
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
            The node registration (what the coordinates mean). Also a very
            complex argument. See the C function documentation. Defaults to
            ``GMT_GRID_NODE_REG``.
        pad : int
            The grid padding. Defaults to ``GMT_PAD_DEFAULT``.

        Returns
        -------
        data_ptr : int
            A ctypes pointer (an integer) to the allocated ``GMT_Dataset``
            object.

        Raises
        ------
        GMTCLibError
            In case of invalid inputs or data_ptr being NULL.

        """
        # Parse and check input arguments
        family_int = self._parse_data_family(family)
        if mode not in self.data_modes:
            raise GMTCLibError("Invalid data creation mode '{}'.".format(mode))
        geometry_int = self._parse_data_geometry(geometry)
        # dim is required (get a segmentation fault if passing it as None
        if 'dim' not in kwargs:
            kwargs['dim'] = [0]*4
        # Convert dim, ranges, and inc to ctypes arrays if given
        dim = kwargs_to_ctypes_array('dim', kwargs, ctypes.c_uint64*4)
        ranges = kwargs_to_ctypes_array('ranges', kwargs, ctypes.c_double*4)
        inc = kwargs_to_ctypes_array('inc', kwargs, ctypes.c_double*2)
        pad = self._parse_pad(family, kwargs)

        # Use the GMT defaults if no value is given
        registration = kwargs.get('registration',
                                  self.get_constant('GMT_GRID_NODE_REG'))

        data_ptr = self._c_create_data(
            self.current_session,
            family_int,
            geometry_int,
            self.get_constant(mode),
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

    def _parse_data_geometry(self, geometry):
        """
        Parse the geometry argument for GMT data manipulation functions.

        Converts the string name to the corresponding integer value.

        Parameters
        ----------
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). See the
            ``data_geometries`` attribute for valid names.

        Returns
        -------
        geometry_int : int
            The converted geometry.

        Raises
        ------
        GMTCLibError
            If the geometry name is invalid.

        """
        if geometry not in self.data_geometries:
            raise GMTCLibError("Invalid data geometry '{}'.".format(geometry))
        return self.get_constant(geometry)

    def _parse_data_family(self, family):
        """
        Parse the data family string into an integer number.

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
        if family_name not in self.data_families:
            raise GMTCLibError(
                "Invalid data family '{}'.".format(family_name))
        family_value = self.get_constant(family_name)
        if len(parts) == 2:
            via_name = parts[1]
            if via_name not in self.data_vias:
                raise GMTCLibError(
                    "Invalid data family (via) '{}'.".format(via_name))
            via_value = self.get_constant(via_name)
        else:
            via_value = 0
        return family_value + via_value

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

        """
        if array.dtype.name not in self._dtypes:
            raise GMTCLibError(
                "Unsupported numpy data type '{}'.".format(array.dtype.name)
            )
        if array.ndim != ndim:
            raise GMTCLibError(
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
        dataset : ctypes.c_void_p
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
        gmt_type = self._check_dtype_and_dim(vector, ndim=1)
        vector_pointer = vector.ctypes.data_as(ctypes.c_void_p)
        status = self._c_put_vector(self.current_session,
                                    dataset,
                                    column,
                                    gmt_type,
                                    vector_pointer)
        if status != 0:
            raise GMTCLibError(
                ' '.join([
                    "Failed to put vector of type {}".format(vector.dtype),
                    "in column {} of dataset.".format(column),
                ])
            )

    def put_matrix(self, dataset, matrix):
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
        dataset : ctypes.c_void_p
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`~gmt.clib.LibGMT.create_data`.
        matrix : numpy 2d-array
            The array that will be attached to the dataset. Must be a 1d C
            contiguous array.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Matrix`` exits with status !=
            0.

        """
        gmt_type = self._check_dtype_and_dim(matrix, ndim=2)
        matrix_pointer = matrix.ctypes.data_as(ctypes.c_void_p)
        status = self._c_put_matrix(self.current_session,
                                    dataset,
                                    gmt_type,
                                    matrix_pointer)
        if status != 0:
            raise GMTCLibError(
                "Failed to put matrix of type {}.".format(matrix.dtype))

    # pylint: disable=too-many-arguments
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
        data : ctypes.c_void_p
            Pointer to the data container created by
            :meth:`~gmt.clib.LibGMT.create_data`.

        Raises
        ------
        GMTCLibError
            For invalid input arguments or if the GMT API functions returns a
            non-zero status code.

        """
        family_int = self._parse_data_family(family)
        geometry_int = self._parse_data_geometry(geometry)
        status = self._c_write_data(self.current_session,
                                    family_int,
                                    self.get_constant('GMT_IS_FILE'),
                                    geometry_int,
                                    self.get_constant(mode),
                                    (ctypes.c_double*6)(*wesn),
                                    output.encode(),
                                    data)
        if status != 0:
            raise GMTCLibError(
                "Failed to write dataset to '{}'".format(output))
            # Can't test this if by giving a bad file name because if
            # output=='', GMT will just write to stdout and spaces are valid
            # file names.

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
        ...         # Send the output to a file so that we can read it
        ...         ofile = 'virtual_file_example.txt'
        ...         lib.call_module('info', '{} ->{}'.format(vfile, ofile))
        >>> with open(ofile) as f:
        ...     # Replace tabs with spaces
        ...     print(f.read().strip().replace('\\t', ' '))
        <vector memory>: N = 5 <0/4> <5/9>
        >>> # Clean up the output file
        >>> os.remove(ofile)

        """
        family_int = self._parse_data_family(family)
        geometry_int = self._parse_data_geometry(geometry)
        if direction not in ('GMT_IN', 'GMT_OUT'):
            raise GMTCLibError("Invalid direction '{}'.".format(direction))
        direction_int = self.get_constant(direction)

        buff = ctypes.create_string_buffer(self.get_constant('GMT_STR16'))

        status = self._c_open_virtualfile(self.current_session, family_int,
                                          geometry_int, direction_int, data,
                                          buff)

        if status != 0:
            raise GMTCLibError("Failed to create a virtual file.")

        vfname = buff.value.decode()

        try:
            yield vfname
        finally:
            status = self._c_close_virtualfile(self.current_session,
                                               vfname.encode())
            if status != 0:
                raise GMTCLibError(
                    "Failed to close virtual file '{}'.".format(vfname))
