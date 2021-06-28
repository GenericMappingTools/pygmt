"""
Defines the Session class to create and destroy a GMT API session and provides
access to the API functions.

Uses ctypes to wrap most of the core functions from the C API.
"""
import ctypes as ctp
import sys
from contextlib import contextmanager

import numpy as np
import pandas as pd
from packaging.version import Version
from pygmt.clib.conversion import (
    array_to_datetime,
    as_c_contiguous,
    dataarray_to_matrix,
    kwargs_to_ctypes_array,
    vectors_to_arrays,
)
from pygmt.clib.loading import load_libgmt
from pygmt.exceptions import (
    GMTCLibError,
    GMTCLibNoSessionError,
    GMTInvalidInput,
    GMTVersionError,
)
from pygmt.helpers import data_kind, dummy_context, fmt_docstring, tempfile_from_geojson

FAMILIES = [
    "GMT_IS_DATASET",
    "GMT_IS_GRID",
    "GMT_IS_PALETTE",
    "GMT_IS_MATRIX",
    "GMT_IS_VECTOR",
]

VIAS = ["GMT_VIA_MATRIX", "GMT_VIA_VECTOR"]

GEOMETRIES = [
    "GMT_IS_NONE",
    "GMT_IS_POINT",
    "GMT_IS_LINE",
    "GMT_IS_POLYGON",
    "GMT_IS_PLP",
    "GMT_IS_SURFACE",
]

METHODS = ["GMT_IS_DUPLICATE", "GMT_IS_REFERENCE"]

MODES = ["GMT_CONTAINER_ONLY", "GMT_IS_OUTPUT"]

REGISTRATIONS = ["GMT_GRID_PIXEL_REG", "GMT_GRID_NODE_REG"]

DTYPES = {
    np.float64: "GMT_DOUBLE",
    np.float32: "GMT_FLOAT",
    np.int64: "GMT_LONG",
    np.int32: "GMT_INT",
    np.uint64: "GMT_ULONG",
    np.uint32: "GMT_UINT",
    np.datetime64: "GMT_DATETIME",
    np.str_: "GMT_TEXT",
}


class Session:
    """
    A GMT API session where most operations involving the C API happen.

    Works as a context manager (for use in a ``with`` block) to create a GMT C
    API session and destroy it in the end to clean up memory.

    Functions of the shared library are exposed as methods of this class. Most
    methods MUST be used with an open session (inside a ``with`` block). If
    creating GMT data structures to communicate data, put that code inside the
    same ``with`` block as the API calls that will use the data.

    By default, will let :mod:`ctypes` try to find the GMT shared library
    (``libgmt``). If the environment variable ``GMT_LIBRARY_PATH`` is set, will
    look for the shared library in the directory specified by it.

    A ``GMTVersionError`` exception will be raised if the GMT shared library
    reports a version older than the required minimum GMT version.

    The ``session_pointer`` attribute holds a ctypes pointer to the currently
    open session.

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

    >>> from pygmt.datasets import load_earth_relief
    >>> from pygmt.helpers import GMTTempFile
    >>> grid = load_earth_relief()
    >>> type(grid)
    <class 'xarray.core.dataarray.DataArray'>
    >>> # Create a session and destroy it automatically when exiting the "with"
    >>> # block.
    >>> with Session() as ses:
    ...     # Create a virtual file and link to the memory block of the grid.
    ...     with ses.virtualfile_from_grid(grid) as fin:
    ...         # Create a temp file to use as output.
    ...         with GMTTempFile() as fout:
    ...             # Call the grdinfo module with the virtual file as input
    ...             # and the temp file as output.
    ...             ses.call_module(
    ...                 "grdinfo", "{} -C ->{}".format(fin, fout.name)
    ...             )
    ...             # Read the contents of the temp file before it's deleted.
    ...             print(fout.read().strip())
    ...
    -180 180 -90 90 -8182 5651.5 1 1 360 180 1 1
    """

    # The minimum version of GMT required
    required_version = "6.2.0"

    @property
    def session_pointer(self):
        """
        The :class:`ctypes.c_void_p` pointer to the current open GMT session.

        Raises
        ------
        GMTCLibNoSessionError
            If trying to access without a currently open GMT session (i.e.,
            outside of the context manager).
        """
        if not hasattr(self, "_session_pointer") or self._session_pointer is None:
            raise GMTCLibNoSessionError("No currently open GMT API session.")
        return self._session_pointer

    @session_pointer.setter
    def session_pointer(self, session):
        """
        Set the session void pointer.
        """
        self._session_pointer = session

    @property
    def info(self):
        """
        Dictionary with the GMT version and default paths and parameters.
        """
        if not hasattr(self, "_info"):
            self._info = {
                "version": self.get_default("API_VERSION"),
                "padding": self.get_default("API_PAD"),
                "binary dir": self.get_default("API_BINDIR"),
                "share dir": self.get_default("API_SHAREDIR"),
                # This segfaults for some reason
                # 'data dir': self.get_default("API_DATADIR"),
                "plugin dir": self.get_default("API_PLUGINDIR"),
                "library path": self.get_default("API_LIBRARY"),
                "cores": self.get_default("API_CORES"),
                # API_IMAGE_LAYOUT not defined if GMT is not compiled with GDAL
                # "image layout": self.get_default("API_IMAGE_LAYOUT"),
                "grid layout": self.get_default("API_GRID_LAYOUT"),
            }
        return self._info

    def __enter__(self):
        """
        Create a GMT API session and check the libgmt version.

        Calls :meth:`pygmt.clib.Session.create`.

        Raises
        ------
        GMTVersionError
            If the version reported by libgmt is less than
            ``Session.required_version``. Will destroy the session before
            raising the exception.
        """
        self.create("pygmt-session")
        # Need to store the version info because 'get_default' won't work after
        # the session is destroyed.
        version = self.info["version"]
        if Version(version) < Version(self.required_version):
            self.destroy()
            raise GMTVersionError(
                "Using an incompatible GMT version {}. Must be equal or newer than {}.".format(
                    version, self.required_version
                )
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the currently open GMT API session.

        Calls :meth:`pygmt.clib.Session.destroy`.
        """
        self.destroy()

    def __getitem__(self, name):
        """
        Get the value of a GMT constant (C enum) from gmt_resources.h.

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
        c_get_enum = self.get_libgmt_func(
            "GMT_Get_Enum", argtypes=[ctp.c_void_p, ctp.c_char_p], restype=ctp.c_int
        )

        # The C lib introduced the void API pointer to GMT_Get_Enum so that
        # it's consistent with other functions. It doesn't use the pointer so
        # we can pass in None (NULL pointer). We can't give it the actual
        # pointer because we need to call GMT_Get_Enum when creating a new API
        # session pointer (chicken-and-egg type of thing).
        session = None

        value = c_get_enum(session, name.encode())

        if value is None or value == -99999:
            raise GMTCLibError(f"Constant '{name}' doesn't exist in libgmt.")

        return value

    def get_libgmt_func(self, name, argtypes=None, restype=None):
        """
        Get a ctypes function from the libgmt shared library.

        Assigns the argument and return type conversions for the function.

        Use this method to access a C function from libgmt.

        Parameters
        ----------
        name : str
            The name of the GMT API function.
        argtypes : list
            List of ctypes types used to convert the Python input arguments for
            the API function.
        restype : ctypes type
            The ctypes type used to convert the input returned by the function
            into a Python type.

        Returns
        -------
        function
            The GMT API function.

        Examples
        --------

        >>> from ctypes import c_void_p, c_int
        >>> with Session() as lib:
        ...     func = lib.get_libgmt_func(
        ...         "GMT_Destroy_Session", argtypes=[c_void_p], restype=c_int
        ...     )
        ...
        >>> type(func)
        <class 'ctypes.CDLL.__init__.<locals>._FuncPtr'>
        """
        if not hasattr(self, "_libgmt"):
            self._libgmt = load_libgmt()
        function = getattr(self._libgmt, name)
        if argtypes is not None:
            function.argtypes = argtypes
        if restype is not None:
            function.restype = restype
        return function

    def create(self, name):
        """
        Create a new GMT C API session.

        This is required before most other methods of
        :class:`pygmt.clib.Session` can be called.

        .. warning::

            Usage of :class:`pygmt.clib.Session` as a context manager in a
            ``with`` block is preferred over calling
            :meth:`pygmt.clib.Session.create` and
            :meth:`pygmt.clib.Session.destroy` manually.

        Calls ``GMT_Create_Session`` and generates a new ``GMTAPI_CTRL``
        struct, which is a :class:`ctypes.c_void_p` pointer. Sets the
        ``session_pointer`` attribute to this pointer.

        Remember to terminate the current session using
        :meth:`pygmt.clib.Session.destroy` before creating a new one.

        Parameters
        ----------
        name : str
            A name for this session. Doesn't really affect the outcome.
        """
        try:
            # Won't raise an exception if there is a currently open session
            self.session_pointer  # pylint: disable=pointless-statement
            # In this case, fail to create a new session until the old one is
            # destroyed
            raise GMTCLibError(
                "Failed to create a GMT API session: There is a currently open session."
                " Must destroy it fist."
            )
        # If the exception is raised, this means that there is no open session
        # and we're free to create a new one.
        except GMTCLibNoSessionError:
            pass

        c_create_session = self.get_libgmt_func(
            "GMT_Create_Session",
            argtypes=[ctp.c_char_p, ctp.c_uint, ctp.c_uint, ctp.c_void_p],
            restype=ctp.c_void_p,
        )

        # Capture the output printed by GMT into this list. Will use it later
        # to generate error messages for the exceptions raised by API calls.
        self._error_log = []

        @ctp.CFUNCTYPE(ctp.c_int, ctp.c_void_p, ctp.c_char_p)
        def print_func(file_pointer, message):  # pylint: disable=unused-argument
            """
            Callback function that the GMT C API will use to print log and
            error messages.

            We'll capture the messages and print them to stderr so that they
            will show up on the Jupyter notebook.
            """
            message = message.decode().strip()
            self._error_log.append(message)
            # flush to make sure the messages are printed even if we have a
            # crash.
            print(message, file=sys.stderr, flush=True)
            return 0

        # Need to store a copy of the function because ctypes doesn't and it
        # will be garbage collected otherwise
        self._print_callback = print_func

        padding = self["GMT_PAD_DEFAULT"]
        session_type = self["GMT_SESSION_EXTERNAL"]

        session = c_create_session(name.encode(), padding, session_type, print_func)

        if session is None:
            raise GMTCLibError(
                "Failed to create a GMT API session:\n{}".format(self._error_message)
            )

        self.session_pointer = session

    @property
    def _error_message(self):
        """
        A string with all error messages emitted by the C API.

        Only includes messages with the string ``"[ERROR]"`` in them.
        """
        msg = ""
        if hasattr(self, "_error_log"):
            msg = "\n".join(line for line in self._error_log if "[ERROR]" in line)
        return msg

    def destroy(self):
        """
        Destroy the currently open GMT API session.

        .. warning::

            Usage of :class:`pygmt.clib.Session` as a context manager in a
            ``with`` block is preferred over calling
            :meth:`pygmt.clib.Session.create` and
            :meth:`pygmt.clib.Session.destroy` manually.

        Calls ``GMT_Destroy_Session`` to terminate and free the memory of a
        registered ``GMTAPI_CTRL`` session (the pointer for this struct is
        stored in the ``session_pointer`` attribute).

        Always use this method after you are done using a C API session. The
        session needs to be destroyed before creating a new one. Otherwise,
        some of the configuration files might be left behind and can influence
        subsequent API calls.

        Sets the ``session_pointer`` attribute to ``None``.
        """
        c_destroy_session = self.get_libgmt_func(
            "GMT_Destroy_Session", argtypes=[ctp.c_void_p], restype=ctp.c_int
        )

        status = c_destroy_session(self.session_pointer)
        if status:
            raise GMTCLibError(
                "Failed to destroy GMT API session:\n{}".format(self._error_message)
            )

        self.session_pointer = None

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
        c_get_default = self.get_libgmt_func(
            "GMT_Get_Default",
            argtypes=[ctp.c_void_p, ctp.c_char_p, ctp.c_char_p],
            restype=ctp.c_int,
        )

        # Make a string buffer to get a return value
        value = ctp.create_string_buffer(10000)

        status = c_get_default(self.session_pointer, name.encode(), value)

        if status != 0:
            raise GMTCLibError(
                "Error getting default value for '{}' (error code {}).".format(
                    name, status
                )
            )

        return value.value.decode()

    def call_module(self, module, args):
        """
        Call a GMT module with the given arguments.

        Makes a call to ``GMT_Call_Module`` from the C API using mode
        ``GMT_MODULE_CMD`` (arguments passed as a single string).

        Most interactions with the C API are done through this function.

        Parameters
        ----------
        module : str
            Module name (``'coast'``, ``'basemap'``, etc).
        args : str
            String with the command line arguments that will be passed to the
            module (for example, ``'-R0/5/0/10 -JM'``).

        Raises
        ------
        GMTCLibError
            If the returned status code of the function is non-zero.
        """
        c_call_module = self.get_libgmt_func(
            "GMT_Call_Module",
            argtypes=[ctp.c_void_p, ctp.c_char_p, ctp.c_int, ctp.c_void_p],
            restype=ctp.c_int,
        )

        mode = self["GMT_MODULE_CMD"]
        status = c_call_module(
            self.session_pointer, module.encode(), mode, args.encode()
        )
        if status != 0:
            raise GMTCLibError(
                "Module '{}' failed with status code {}:\n{}".format(
                    module, status, self._error_message
                )
            )

    def create_data(self, family, geometry, mode, **kwargs):
        """
        Create an empty GMT data container.

        Parameters
        ----------
        family : str
            A valid GMT data family name (e.g., ``'GMT_IS_DATASET'``). See the
            ``FAMILIES`` attribute for valid names.
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). See the
            ``GEOMETRIES`` attribute for valid names.
        mode : str
            A valid GMT data mode (e.g., ``'GMT_IS_OUTPUT'``). See the
            ``MODES`` attribute for valid names.
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
        registration : str
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
        c_create_data = self.get_libgmt_func(
            "GMT_Create_Data",
            argtypes=[
                ctp.c_void_p,  # API
                ctp.c_uint,  # family
                ctp.c_uint,  # geometry
                ctp.c_uint,  # mode
                ctp.POINTER(ctp.c_uint64),  # dim
                ctp.POINTER(ctp.c_double),  # range
                ctp.POINTER(ctp.c_double),  # inc
                ctp.c_uint,  # registration
                ctp.c_int,  # pad
                ctp.c_void_p,
            ],  # data
            restype=ctp.c_void_p,
        )

        family_int = self._parse_constant(family, valid=FAMILIES, valid_modifiers=VIAS)
        mode_int = self._parse_constant(
            mode,
            valid=MODES,
            valid_modifiers=["GMT_GRID_IS_CARTESIAN", "GMT_GRID_IS_GEO"],
        )
        geometry_int = self._parse_constant(geometry, valid=GEOMETRIES)
        registration_int = self._parse_constant(
            kwargs.get("registration", "GMT_GRID_NODE_REG"), valid=REGISTRATIONS
        )

        # Convert dim, ranges, and inc to ctypes arrays if given (will be None
        # if not given to represent NULL pointers)
        dim = kwargs_to_ctypes_array("dim", kwargs, ctp.c_uint64 * 4)
        ranges = kwargs_to_ctypes_array("ranges", kwargs, ctp.c_double * 4)
        inc = kwargs_to_ctypes_array("inc", kwargs, ctp.c_double * 2)

        # Use a NULL pointer (None) for existing data to indicate that the
        # container should be created empty. Fill it in later using put_vector
        # and put_matrix.
        data_ptr = c_create_data(
            self.session_pointer,
            family_int,
            geometry_int,
            mode_int,
            dim,
            ranges,
            inc,
            registration_int,
            self._parse_pad(family, kwargs),
            None,
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
        pad = kwargs.get("pad", None)
        if pad is None:
            if "MATRIX" in family:
                pad = 0
            else:
                pad = self["GMT_PAD_DEFAULT"]
        return pad

    def _parse_constant(self, constant, valid, valid_modifiers=None):
        """
        Parse a constant, convert it to an int, and validate it.

        The GMT C API takes certain defined constants, like ``'GMT_IS_GRID'``,
        that need to be validated and converted to integer values using
        :meth:`pygmt.clib.Session.__getitem__`.

        The constants can also take a modifier by appending another constant
        name, e.g. ``'GMT_IS_GRID|GMT_VIA_MATRIX'``. The two parts must be
        converted separately and their values are added.

        If valid modifiers are not given, then will assume that modifiers are
        not allowed. In this case, will raise a
        :class:`pygmt.exceptions.GMTInvalidInput` exception if given a
        modifier.

        Parameters
        ----------
        constant : str
            The name of a valid GMT API constant, with an optional modifier.
        valid : list of str
            A list of valid values for the constant. Will raise a
            :class:`pygmt.exceptions.GMTInvalidInput` exception if the given
            value is not on the list.
        """
        parts = constant.split("|")
        name = parts[0]
        nmodifiers = len(parts) - 1
        if nmodifiers > 1:
            raise GMTInvalidInput(
                "Only one modifier is allowed in constants, {} given: '{}'".format(
                    nmodifiers, constant
                )
            )
        if nmodifiers > 0 and valid_modifiers is None:
            raise GMTInvalidInput(
                "Constant modifiers not allowed since valid values were not "
                + "given: '{}'".format(constant)
            )
        if name not in valid:
            raise GMTInvalidInput(
                "Invalid constant argument '{}'. Must be one of {}.".format(
                    name, str(valid)
                )
            )
        if (
            nmodifiers > 0
            and valid_modifiers is not None
            and parts[1] not in valid_modifiers
        ):
            raise GMTInvalidInput(
                "Invalid constant modifier '{}'. Must be one of {}.".format(
                    parts[1], str(valid_modifiers)
                )
            )
        integer_value = sum(self[part] for part in parts)
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
        >>> data = np.array([1, 2, 3], dtype="float64")
        >>> with Session() as ses:
        ...     gmttype = ses._check_dtype_and_dim(data, ndim=1)
        ...     gmttype == ses["GMT_DOUBLE"]
        ...
        True
        >>> data = np.ones((5, 2), dtype="float32")
        >>> with Session() as ses:
        ...     gmttype = ses._check_dtype_and_dim(data, ndim=2)
        ...     gmttype == ses["GMT_FLOAT"]
        ...
        True
        """
        # check the array has the given dimension
        if array.ndim != ndim:
            raise GMTInvalidInput(f"Expected a numpy 1d array, got {array.ndim}d.")

        # check the array has a valid/known data type
        if array.dtype.type not in DTYPES:
            try:
                # Try to convert any unknown numpy data types to np.datetime64
                array = np.asarray(array, dtype=np.datetime64)
            except ValueError as e:
                raise GMTInvalidInput(
                    f"Unsupported numpy data type '{array.dtype.type}'."
                ) from e
        return self[DTYPES[array.dtype.type]]

    def put_vector(self, dataset, column, vector):
        r"""
        Attach a numpy 1D array as a column on a GMT dataset.

        Use this function to attach numpy array data to a GMT dataset and pass
        it to GMT modules. Wraps ``GMT_Put_Vector``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data`
        first. Use ``family='GMT_IS_DATASET|GMT_VIA_VECTOR'``.

        Not at all numpy dtypes are supported, only: float64, float32, int64,
        int32, uint64, uint32, datetime64 and str\_.

        .. warning::
            The numpy array must be C contiguous in memory. If it comes from a
            column slice of a 2d array, for example, you will have to make a
            copy. Use :func:`numpy.ascontiguousarray` to make sure your vector
            is contiguous (it won't copy if it already is).

        Parameters
        ----------
        dataset : :class:`ctypes.c_void_p`
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`pygmt.clib.Session.create_data`.
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
        c_put_vector = self.get_libgmt_func(
            "GMT_Put_Vector",
            argtypes=[ctp.c_void_p, ctp.c_void_p, ctp.c_uint, ctp.c_uint, ctp.c_void_p],
            restype=ctp.c_int,
        )

        gmt_type = self._check_dtype_and_dim(vector, ndim=1)
        if gmt_type in (self["GMT_TEXT"], self["GMT_DATETIME"]):
            vector_pointer = (ctp.c_char_p * len(vector))()
            if gmt_type == self["GMT_DATETIME"]:
                vector_pointer[:] = np.char.encode(
                    np.datetime_as_string(array_to_datetime(vector))
                )
            else:
                vector_pointer[:] = np.char.encode(vector)
        else:
            vector_pointer = vector.ctypes.data_as(ctp.c_void_p)
        status = c_put_vector(
            self.session_pointer, dataset, column, gmt_type, vector_pointer
        )
        if status != 0:
            raise GMTCLibError(
                (
                    f"Failed to put vector of type {vector.dtype} "
                    f"in column {column} of dataset."
                )
            )

    def put_strings(self, dataset, family, strings):
        """
        Attach a numpy 1D array of dtype str as a column on a GMT dataset.

        Use this function to attach string type numpy array data to a GMT
        dataset and pass it to GMT modules. Wraps ``GMT_Put_Strings``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data`
        first.

        .. warning::
            The numpy array must be C contiguous in memory. If it comes from a
            column slice of a 2d array, for example, you will have to make a
            copy. Use :func:`numpy.ascontiguousarray` to make sure your vector
            is contiguous (it won't copy if it already is).

        Parameters
        ----------
        dataset : :class:`ctypes.c_void_p`
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`pygmt.clib.Session.create_data`.
        family : str
            The family type of the dataset. Can be either ``GMT_IS_VECTOR`` or
            ``GMT_IS_MATRIX``.
        strings : numpy 1d-array
            The array that will be attached to the dataset. Must be a 1d C
            contiguous array.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Strings`` exits with status !=
            0.
        """
        c_put_strings = self.get_libgmt_func(
            "GMT_Put_Strings",
            argtypes=[
                ctp.c_void_p,
                ctp.c_uint,
                ctp.c_void_p,
                ctp.POINTER(ctp.c_char_p),
            ],
            restype=ctp.c_int,
        )

        strings_pointer = (ctp.c_char_p * len(strings))()
        strings_pointer[:] = np.char.encode(strings)

        family_int = self._parse_constant(
            family, valid=FAMILIES, valid_modifiers=METHODS
        )

        status = c_put_strings(
            self.session_pointer, family_int, dataset, strings_pointer
        )
        if status != 0:
            raise GMTCLibError(
                f"Failed to put strings of type {strings.dtype} into dataset"
            )

    def put_matrix(self, dataset, matrix, pad=0):
        """
        Attach a numpy 2D array to a GMT dataset.

        Use this function to attach numpy array data to a GMT dataset and pass
        it to GMT modules. Wraps ``GMT_Put_Matrix``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data`
        first. Use ``|GMT_VIA_MATRIX'`` in the family.

        Not at all numpy dtypes are supported, only: float64, float32, int64,
        int32, uint64, and uint32.

        .. warning::
            The numpy array must be C contiguous in memory. Use
            :func:`numpy.ascontiguousarray` to make sure your vector is
            contiguous (it won't copy if it already is).

        Parameters
        ----------
        dataset : :class:`ctypes.c_void_p`
            The ctypes void pointer to a ``GMT_Dataset``. Create it with
            :meth:`pygmt.clib.Session.create_data`.
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
        c_put_matrix = self.get_libgmt_func(
            "GMT_Put_Matrix",
            argtypes=[ctp.c_void_p, ctp.c_void_p, ctp.c_uint, ctp.c_int, ctp.c_void_p],
            restype=ctp.c_int,
        )

        gmt_type = self._check_dtype_and_dim(matrix, ndim=2)
        matrix_pointer = matrix.ctypes.data_as(ctp.c_void_p)
        status = c_put_matrix(
            self.session_pointer, dataset, gmt_type, pad, matrix_pointer
        )
        if status != 0:
            raise GMTCLibError("Failed to put matrix of type {}.".format(matrix.dtype))

    def write_data(self, family, geometry, mode, wesn, output, data):
        """
        Write a GMT data container to a file.

        The data container should be created by
        :meth:`pygmt.clib.Session.create_data`.

        Wraps ``GMT_Write_Data`` but only allows writing to a file. So the
        ``method`` argument is omitted.

        Parameters
        ----------
        family : str
            A valid GMT data family name (e.g., ``'GMT_IS_DATASET'``). See the
            ``FAMILIES`` attribute for valid names. Don't use the
            ``GMT_VIA_VECTOR`` or ``GMT_VIA_MATRIX`` constructs for this. Use
            ``GMT_IS_VECTOR`` and ``GMT_IS_MATRIX`` instead.
        geometry : str
            A valid GMT data geometry name (e.g., ``'GMT_IS_POINT'``). See the
            ``GEOMETRIES`` attribute for valid names.
        mode : str
            How the data is to be written to the file. This option varies
            depending on the given family. See the GMT API documentation for
            details.
        wesn : list or numpy array
            [xmin, xmax, ymin, ymax, zmin, zmax] of the data. Must have 6
            elements.
        output : str
            The output file name.
        data : :class:`ctypes.c_void_p`
            Pointer to the data container created by
            :meth:`pygmt.clib.Session.create_data`.

        Raises
        ------
        GMTCLibError
            For invalid input arguments or if the GMT API functions returns a
            non-zero status code.
        """
        c_write_data = self.get_libgmt_func(
            "GMT_Write_Data",
            argtypes=[
                ctp.c_void_p,
                ctp.c_uint,
                ctp.c_uint,
                ctp.c_uint,
                ctp.c_uint,
                ctp.POINTER(ctp.c_double),
                ctp.c_char_p,
                ctp.c_void_p,
            ],
            restype=ctp.c_int,
        )

        family_int = self._parse_constant(family, valid=FAMILIES, valid_modifiers=VIAS)
        geometry_int = self._parse_constant(geometry, valid=GEOMETRIES)
        status = c_write_data(
            self.session_pointer,
            family_int,
            self["GMT_IS_FILE"],
            geometry_int,
            self[mode],
            (ctp.c_double * 6)(*wesn),
            output.encode(),
            data,
        )
        if status != 0:
            raise GMTCLibError("Failed to write dataset to '{}'".format(output))

    @contextmanager
    def open_virtual_file(self, family, geometry, direction, data):
        """
        Open a GMT Virtual File to pass data to and from a module.

        GMT uses a virtual file scheme to pass in data to API modules. Use it
        to pass in your GMT data structure (created using
        :meth:`pygmt.clib.Session.create_data`) to a module that expects an
        input or output file.

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
            By default, GMT can modify the data you pass in. Add modifier
            ``'GMT_IS_REFERENCE'`` to tell GMT the data are read-only, or
            ``'GMT_IS_DUPLICATE'`` to tell GMT to duplicate the data.
        data : int
            The ctypes void pointer to your GMT data structure.

        Yields
        ------
        vfname : str
            The name of the virtual file that you can pass to a GMT module.

        Examples
        --------

        >>> from pygmt.helpers import GMTTempFile
        >>> import os
        >>> import numpy as np
        >>> x = np.array([0, 1, 2, 3, 4])
        >>> y = np.array([5, 6, 7, 8, 9])
        >>> with Session() as lib:
        ...     family = "GMT_IS_DATASET|GMT_VIA_VECTOR"
        ...     geometry = "GMT_IS_POINT"
        ...     dataset = lib.create_data(
        ...         family=family,
        ...         geometry=geometry,
        ...         mode="GMT_CONTAINER_ONLY",
        ...         dim=[2, 5, 1, 0],  # columns, lines, segments, type
        ...     )
        ...     lib.put_vector(dataset, column=0, vector=x)
        ...     lib.put_vector(dataset, column=1, vector=y)
        ...     # Add the dataset to a virtual file
        ...     vfargs = (family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset)
        ...     with lib.open_virtual_file(*vfargs) as vfile:
        ...         # Send the output to a temp file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             args = "{} ->{}".format(vfile, ofile.name)
        ...             lib.call_module("info", args)
        ...             print(ofile.read().strip())
        ...
        <vector memory>: N = 5 <0/4> <5/9>
        """
        c_open_virtualfile = self.get_libgmt_func(
            "GMT_Open_VirtualFile",
            argtypes=[
                ctp.c_void_p,
                ctp.c_uint,
                ctp.c_uint,
                ctp.c_uint,
                ctp.c_void_p,
                ctp.c_char_p,
            ],
            restype=ctp.c_int,
        )

        c_close_virtualfile = self.get_libgmt_func(
            "GMT_Close_VirtualFile",
            argtypes=[ctp.c_void_p, ctp.c_char_p],
            restype=ctp.c_int,
        )

        family_int = self._parse_constant(family, valid=FAMILIES, valid_modifiers=VIAS)
        geometry_int = self._parse_constant(geometry, valid=GEOMETRIES)
        direction_int = self._parse_constant(
            direction, valid=["GMT_IN", "GMT_OUT"], valid_modifiers=METHODS
        )

        buff = ctp.create_string_buffer(self["GMT_VF_LEN"])

        status = c_open_virtualfile(
            self.session_pointer, family_int, geometry_int, direction_int, data, buff
        )

        if status != 0:
            raise GMTCLibError("Failed to create a virtual file.")

        vfname = buff.value.decode()

        try:
            yield vfname
        finally:
            status = c_close_virtualfile(self.session_pointer, vfname.encode())
            if status != 0:
                raise GMTCLibError("Failed to close virtual file '{}'.".format(vfname))

    @contextmanager
    def virtualfile_from_vectors(self, *vectors):
        """
        Store 1d arrays as columns of a table inside a virtual file.

        Use the virtual file name to pass in the data in your vectors to a GMT
        module.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        Use this instead of creating the data container and virtual file by
        hand with :meth:`pygmt.clib.Session.create_data`,
        :meth:`pygmt.clib.Session.put_vector`, and
        :meth:`pygmt.clib.Session.open_virtual_file`.

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
        fname : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from pygmt.helpers import GMTTempFile
        >>> import numpy as np
        >>> import pandas as pd
        >>> x = [1, 2, 3]
        >>> y = np.array([4, 5, 6])
        >>> z = pd.Series([7, 8, 9])
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_vectors(x, y, z) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module(
        ...                 "info", "{} ->{}".format(fin, fout.name)
        ...             )
        ...             print(fout.read().strip())
        ...
        <vector memory>: N = 3 <1/3> <4/6> <7/9>
        """
        # Conversion to a C-contiguous array needs to be done here and not in
        # put_vector or put_strings because we need to maintain a reference to
        # the copy while it is being used by the C API. Otherwise, the array
        # would be garbage collected and the memory freed. Creating it in this
        # context manager guarantees that the copy will be around until the
        # virtual file is closed. The conversion is implicit in
        # vectors_to_arrays.
        arrays = vectors_to_arrays(vectors)

        columns = len(arrays)
        # Find arrays that are of string dtype from column 3 onwards
        # Assumes that first 2 columns contains coordinates like longitude
        # latitude, or datetime string types.
        for col, array in enumerate(arrays[2:]):
            if pd.api.types.is_string_dtype(array.dtype):
                columns = col + 2
                break

        rows = len(arrays[0])
        if not all(len(i) == rows for i in arrays):
            raise GMTInvalidInput("All arrays must have same size.")

        family = "GMT_IS_DATASET|GMT_VIA_VECTOR"
        geometry = "GMT_IS_POINT"

        dataset = self.create_data(
            family, geometry, mode="GMT_CONTAINER_ONLY", dim=[columns, rows, 1, 0]
        )

        # Use put_vector for columns with numerical type data
        for col, array in enumerate(arrays[:columns]):
            self.put_vector(dataset, column=col, vector=array)

        # Use put_strings for last column(s) with string type data
        # Have to use modifier "GMT_IS_DUPLICATE" to duplicate the strings
        string_arrays = arrays[columns:]
        if string_arrays:
            if len(string_arrays) == 1:
                strings = string_arrays[0]
            elif len(string_arrays) > 1:
                strings = np.apply_along_axis(
                    func1d=" ".join, axis=0, arr=string_arrays
                )
            strings = np.asanyarray(a=strings, dtype=str)
            self.put_strings(
                dataset, family="GMT_IS_VECTOR|GMT_IS_DUPLICATE", strings=strings
            )

        with self.open_virtual_file(
            family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset
        ) as vfile:
            yield vfile

    @contextmanager
    def virtualfile_from_matrix(self, matrix):
        """
        Store a 2d array as a table inside a virtual file.

        Use the virtual file name to pass in the data in your matrix to a GMT
        module.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        The virtual file will contain the array as a ``GMT_MATRIX`` pretending
        to be a ``GMT_DATASET``.

        **Not meant for creating ``GMT_GRID``**. The grid requires more
        metadata than just the data matrix. Use
        :meth:`pygmt.clib.Session.virtualfile_from_grid` instead.

        Use this instead of creating the data container and virtual file by
        hand with :meth:`pygmt.clib.Session.create_data`,
        :meth:`pygmt.clib.Session.put_matrix`, and
        :meth:`pygmt.clib.Session.open_virtual_file`

        The matrix must be C contiguous in memory. If it is not (e.g., it is a
        slice of a larger array), the array will be copied to make sure it is.

        Parameters
        ----------
        matrix : 2d array
            The matrix that will be included in the GMT data container.

        Yields
        ------
        fname : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from pygmt.helpers import GMTTempFile
        >>> import numpy as np
        >>> data = np.arange(12).reshape((4, 3))
        >>> print(data)
        [[ 0  1  2]
         [ 3  4  5]
         [ 6  7  8]
         [ 9 10 11]]
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_matrix(data) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module(
        ...                 "info", "{} ->{}".format(fin, fout.name)
        ...             )
        ...             print(fout.read().strip())
        ...
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

        family = "GMT_IS_DATASET|GMT_VIA_MATRIX"
        geometry = "GMT_IS_POINT"

        dataset = self.create_data(
            family, geometry, mode="GMT_CONTAINER_ONLY", dim=[columns, rows, 1, 0]
        )

        self.put_matrix(dataset, matrix)

        with self.open_virtual_file(
            family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset
        ) as vfile:
            yield vfile

    @contextmanager
    def virtualfile_from_grid(self, grid):
        """
        Store a grid in a virtual file.

        Use the virtual file name to pass in the data in your grid to a GMT
        module. Grids must be :class:`xarray.DataArray` instances.

        Context manager (use in a ``with`` block). Yields the virtual file name
        that you can pass as an argument to a GMT module call. Closes the
        virtual file upon exit of the ``with`` block.

        The virtual file will contain the grid as a ``GMT_MATRIX`` with extra
        metadata.

        Use this instead of creating a data container and virtual file by hand
        with :meth:`pygmt.clib.Session.create_data`,
        :meth:`pygmt.clib.Session.put_matrix`, and
        :meth:`pygmt.clib.Session.open_virtual_file`

        The grid data matrix must be C contiguous in memory. If it is not
        (e.g., it is a slice of a larger array), the array will be copied to
        make sure it is.

        Parameters
        ----------
        grid : :class:`xarray.DataArray`
            The grid that will be included in the virtual file.

        Yields
        ------
        fname : str
            The name of virtual file. Pass this as a file name argument to a
            GMT module.

        Examples
        --------

        >>> from pygmt.datasets import load_earth_relief
        >>> from pygmt.helpers import GMTTempFile
        >>> data = load_earth_relief(resolution="01d")
        >>> print(data.shape)
        (180, 360)
        >>> print(data.lon.values.min(), data.lon.values.max())
        -179.5 179.5
        >>> print(data.lat.values.min(), data.lat.values.max())
        -89.5 89.5
        >>> print(data.values.min(), data.values.max())
        -8182.0 5651.5
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_grid(data) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             args = "{} -L0 -Cn ->{}".format(fin, fout.name)
        ...             ses.call_module("grdinfo", args)
        ...             print(fout.read().strip())
        ...
        -180 180 -90 90 -8182 5651.5 1 1 360 180 1 1
        >>> # The output is: w e s n z0 z1 dx dy n_columns n_rows reg gtype
        """
        _gtype = {0: "GMT_GRID_IS_CARTESIAN", 1: "GMT_GRID_IS_GEO"}[grid.gmt.gtype]
        _reg = {0: "GMT_GRID_NODE_REG", 1: "GMT_GRID_PIXEL_REG"}[grid.gmt.registration]

        # Conversion to a C-contiguous array needs to be done here and not in
        # put_matrix because we need to maintain a reference to the copy while
        # it is being used by the C API. Otherwise, the array would be garbage
        # collected and the memory freed. Creating it in this context manager
        # guarantees that the copy will be around until the virtual file is
        # closed. The conversion is implicit in dataarray_to_matrix.
        matrix, region, inc = dataarray_to_matrix(grid)

        family = "GMT_IS_GRID|GMT_VIA_MATRIX"
        geometry = "GMT_IS_SURFACE"
        gmt_grid = self.create_data(
            family,
            geometry,
            mode=f"GMT_CONTAINER_ONLY|{_gtype}",
            ranges=region,
            inc=inc,
            registration=_reg,
        )
        self.put_matrix(gmt_grid, matrix)
        args = (family, geometry, "GMT_IN|GMT_IS_REFERENCE", gmt_grid)
        with self.open_virtual_file(*args) as vfile:
            yield vfile

    @fmt_docstring
    def virtualfile_from_data(
        self, check_kind=None, data=None, x=None, y=None, z=None, extra_arrays=None
    ):
        """
        Store any data inside a virtual file.

        This convenience function automatically detects the kind of data passed
        into it, and produces a virtualfile that can be passed into GMT later
        on.

        Parameters
        ----------
        check_kind : str
            Used to validate the type of data that can be passed in. Choose
            from 'raster', 'vector' or None. Default is None (no validation).
        data : str or xarray.DataArray or {table-like} or None
            Any raster or vector data format. This could be a file name, a
            raster grid, a vector matrix/arrays, or other supported data input.
        x/y/z : 1d arrays or None
            x, y and z columns as numpy arrays.
        extra_arrays : list of 1d arrays
            Optional. A list of numpy arrays in addition to x, y and z. All
            of these arrays must be of the same size as the x/y/z arrays.

        Returns
        -------
        file_context : contextlib._GeneratorContextManager
            The virtual file stored inside a context manager. Access the file
            name of this virtualfile using ``with file_context as fname: ...``.

        Examples
        --------
        >>> from pygmt.helpers import GMTTempFile
        >>> import xarray as xr
        >>> data = xr.Dataset(
        ...     coords=dict(index=[0, 1, 2]),
        ...     data_vars=dict(
        ...         x=("index", [9, 8, 7]),
        ...         y=("index", [6, 5, 4]),
        ...         z=("index", [3, 2, 1]),
        ...     ),
        ... )
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_data(
        ...         check_kind="vector", data=data
        ...     ) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module("info", fin + " ->" + fout.name)
        ...             print(fout.read().strip())
        ...
        <vector memory>: N = 3 <7/9> <4/6> <1/3>
        """
        kind = data_kind(data, x, y, z)

        if check_kind == "raster" and kind not in ("file", "grid"):
            raise GMTInvalidInput(f"Unrecognized data type for grid: {type(data)}")
        if check_kind == "vector" and kind not in (
            "file",
            "matrix",
            "vectors",
            "geojson",
        ):
            raise GMTInvalidInput(f"Unrecognized data type for vector: {type(data)}")

        # Decide which virtualfile_from_ function to use
        _virtualfile_from = {
            "file": dummy_context,
            "geojson": tempfile_from_geojson,
            "grid": self.virtualfile_from_grid,
            # Note: virtualfile_from_matrix is not used because a matrix can be
            # converted to vectors instead, and using vectors allows for better
            # handling of string type inputs (e.g. for datetime data types)
            "matrix": self.virtualfile_from_vectors,
            "vectors": self.virtualfile_from_vectors,
        }[kind]

        # Ensure the data is an iterable (Python list or tuple)
        if kind in ("file", "geojson", "grid"):
            _data = (data,)
        elif kind == "vectors":
            _data = [np.atleast_1d(x), np.atleast_1d(y)]
            if z is not None:
                _data.append(np.atleast_1d(z))
            if extra_arrays:
                _data.extend(extra_arrays)
        elif kind == "matrix":  # turn 2D arrays into list of vectors
            try:
                # pandas.Series will be handled below like a 1d numpy ndarray
                assert not hasattr(data, "to_frame")
                # pandas.DataFrame and xarray.Dataset types
                _data = [array for _, array in data.items()]
            except (AttributeError, AssertionError):
                try:
                    # Just use virtualfile_from_matrix for 2D numpy.ndarray
                    # which are signed integer (i), unsigned integer (u) or
                    # floating point (f) types
                    assert data.ndim == 2 and data.dtype.kind in "iuf"
                    _virtualfile_from = self.virtualfile_from_matrix
                    _data = (data,)
                except (AssertionError, AttributeError):
                    # Python list, tuple, numpy ndarray and pandas.Series types
                    _data = np.atleast_2d(np.asanyarray(data).T)

        # Finally create the virtualfile from the data, to be passed into GMT
        file_context = _virtualfile_from(*_data)

        return file_context

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

        >>> import pygmt
        >>> fig = pygmt.Figure()
        >>> fig.coast(
        ...     region=[0, 10, -20, -10],
        ...     projection="M6i",
        ...     frame=True,
        ...     land="black",
        ... )
        >>> with Session() as lib:
        ...     wesn = lib.extract_region()
        ...
        >>> print(", ".join(["{:.2f}".format(x) for x in wesn]))
        0.00, 10.00, -20.00, -10.00

        Using ISO country codes for the regions (for example ``'US.HI'`` for
        Hawaii):

        >>> fig = pygmt.Figure()
        >>> fig.coast(
        ...     region="US.HI", projection="M6i", frame=True, land="black"
        ... )
        >>> with Session() as lib:
        ...     wesn = lib.extract_region()
        ...
        >>> print(", ".join(["{:.2f}".format(x) for x in wesn]))
        -164.71, -154.81, 18.91, 23.58

        The country codes can have an extra argument that rounds the region a
        multiple of the argument (for example, ``'US.HI+r5'`` will round the
        region to multiples of 5):

        >>> fig = pygmt.Figure()
        >>> fig.coast(
        ...     region="US.HI+r5", projection="M6i", frame=True, land="black"
        ... )
        >>> with Session() as lib:
        ...     wesn = lib.extract_region()
        ...
        >>> print(", ".join(["{:.2f}".format(x) for x in wesn]))
        -165.00, -150.00, 15.00, 25.00
        """
        c_extract_region = self.get_libgmt_func(
            "GMT_Extract_Region",
            argtypes=[ctp.c_void_p, ctp.c_char_p, ctp.POINTER(ctp.c_double)],
            restype=ctp.c_int,
        )

        wesn = np.empty(4, dtype=np.float64)
        wesn_pointer = wesn.ctypes.data_as(ctp.POINTER(ctp.c_double))
        # The second argument to GMT_Extract_Region is a file pointer to a
        # PostScript file. It's only valid in classic mode. Use None to get a
        # NULL pointer instead.
        status = c_extract_region(self.session_pointer, None, wesn_pointer)
        if status != 0:
            raise GMTCLibError("Failed to extract region from current figure.")
        return wesn
