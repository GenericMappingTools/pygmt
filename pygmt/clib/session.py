"""
Defines the Session class to create and destroy a GMT API session and provides access to
the API functions.

Uses ctypes to wrap most of the core functions from the C API.
"""

import contextlib
import ctypes as ctp
import io
import sys
import warnings
from collections.abc import Callable, Generator, Sequence
from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr
from pygmt.clib.conversion import (
    dataarray_to_matrix,
    sequence_to_ctypes_array,
    strings_to_ctypes_array,
    vectors_to_arrays,
)
from pygmt.clib.loading import get_gmt_version, load_libgmt
from pygmt.datatypes import _GMT_DATASET, _GMT_GRID, _GMT_IMAGE
from pygmt.exceptions import (
    GMTCLibError,
    GMTCLibNoSessionError,
    GMTInvalidInput,
    GMTTypeError,
    GMTValueError,
)
from pygmt.helpers import (
    _validate_data_input,
    data_kind,
    deprecate_parameter,
    tempfile_from_geojson,
    tempfile_from_image,
)

FAMILIES = [
    "GMT_IS_DATASET",  # Entity is a data table
    "GMT_IS_GRID",  # Entity is a grid
    "GMT_IS_IMAGE",  # Entity is a 1- or 3-band unsigned char image
    "GMT_IS_PALETTE",  # Entity is a color palette table
    "GMT_IS_POSTSCRIPT",  # Entity is a PostScript content struct
    "GMT_IS_MATRIX",  # Entity is a user matrix
    "GMT_IS_VECTOR",  # Entity is a set of user vectors
    "GMT_IS_CUBE",  # Entity is a 3-D data cube
]

VIAS = [
    "GMT_VIA_MATRIX",  # dataset is passed as a matrix
    "GMT_VIA_VECTOR",  # dataset is passed as a set of vectors
]

GEOMETRIES = [
    "GMT_IS_NONE",  # items without geometry (e.g., CPT)
    "GMT_IS_POINT",  # items are points
    "GMT_IS_LINE",  # items are lines
    "GMT_IS_POLY",  # items are polygons
    "GMT_IS_LP",  # items could be any one of LINE or POLY
    "GMT_IS_PLP",  # items could be any one of POINT, LINE, or POLY
    "GMT_IS_SURFACE",  # items are 2-D grid
    "GMT_IS_VOLUME",  # items are 3-D grid
    "GMT_IS_TEXT",  # Text strings which triggers ASCII text reading
]

METHODS = [
    "GMT_IS_DUPLICATE",  # tell GMT the data are read-only
    "GMT_IS_REFERENCE",  # tell GMT to duplicate the data
]

DIRECTIONS = ["GMT_IN", "GMT_OUT"]

MODES = [
    "GMT_CONTAINER_AND_DATA",  # Create/Read/Write both container and the data array
    "GMT_CONTAINER_ONLY",  # Cread/Read/Write the container but no data array
    "GMT_DATA_ONLY",  # Create/Read/Write the container's data array only
    "GMT_IS_OUTPUT",  # For creating a resource as a container for output
]
MODE_MODIFIERS = [
    "GMT_GRID_IS_CARTESIAN",  # Grid is not geographic but Cartesian
    "GMT_GRID_IS_GEO",  # Grid is geographic, not Cartesian
    "GMT_WITH_STRINGS",  # Allocate string array for GMT_DATASET/GMT_VECTOR/GMT_MATRIX
]

REGISTRATIONS = ["GMT_GRID_NODE_REG", "GMT_GRID_PIXEL_REG"]

# Dictionary for mapping numpy dtypes to GMT data types.
DTYPES_NUMERIC = {
    np.int8: "GMT_CHAR",
    np.int16: "GMT_SHORT",
    np.int32: "GMT_INT",
    np.int64: "GMT_LONG",
    np.longlong: "GMT_LONG",
    np.uint8: "GMT_UCHAR",
    np.uint16: "GMT_USHORT",
    np.uint32: "GMT_UINT",
    np.uint64: "GMT_ULONG",
    np.ulonglong: "GMT_ULONG",
    np.float32: "GMT_FLOAT",
    np.float64: "GMT_DOUBLE",
    np.timedelta64: "GMT_LONG",
}
DTYPES_TEXT = {
    np.str_: "GMT_TEXT",
    np.datetime64: "GMT_DATETIME",
}
DTYPES = DTYPES_NUMERIC | DTYPES_TEXT

# Dictionary for storing the values of GMT constants.
GMT_CONSTANTS = {}

# Load the GMT library outside the Session class to avoid repeated loading.
_libgmt = load_libgmt()
__gmt_version__ = get_gmt_version(_libgmt)


class Session:
    """
    A GMT API session where most operations involving the C API happen.

    Works as a context manager (for use in a ``with`` block) to create a GMT C API
    session and destroy it in the end to clean up memory.

    Functions of the shared library are exposed as methods of this class. Most methods
    MUST be used with an open session (inside a ``with`` block). If creating GMT data
    structures to communicate data, put that code inside the same ``with`` block as the
    API calls that will use the data.

    By default, will let :mod:`ctypes` try to find the GMT shared library (``libgmt``).
    If the environment variable :term:`GMT_LIBRARY_PATH` is set, will look for the
    shared library in the directory specified by it.

    The ``session_pointer`` attribute holds a ctypes pointer to the currently open
    session.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or couldn't
        access the functions).
    GMTCLibNoSessionError
        If you try to call a method outside of a ``with`` block.

    Examples
    --------

    >>> from pygmt.helpers.testing import load_static_earth_relief
    >>> from pygmt.helpers import GMTTempFile
    >>> grid = load_static_earth_relief()
    >>> type(grid)
    <class 'xarray.core.dataarray.DataArray'>
    >>> # Create a session and destroy it automatically when exiting the "with" block.
    >>> with Session() as lib:
    ...     # Create a virtual file and link to the memory block of the grid.
    ...     with lib.virtualfile_from_grid(grid) as fin:
    ...         # Create a temp file to use as output.
    ...         with GMTTempFile() as fout:
    ...             # Call the grdinfo module with the virtual file as input and the
    ...             # temp file as output.
    ...             lib.call_module("grdinfo", [fin, "-C", f"->{fout.name}"])
    ...             # Read the contents of the temp file before it's deleted.
    ...             print(fout.read().strip())
    -55 -47 -24 -10 190 981 1 1 8 14 1 1
    """

    @property
    def session_pointer(self) -> ctp.c_void_p:
        """
        The :class:`ctypes.c_void_p` pointer to the current open GMT session.

        Raises
        ------
        GMTCLibNoSessionError
            If trying to access without a currently open GMT session (i.e., outside of
            the context manager).
        """
        if getattr(self, "_session_pointer", None) is None:
            msg = "No currently open GMT API session."
            raise GMTCLibNoSessionError(msg)
        return self._session_pointer

    @session_pointer.setter
    def session_pointer(self, session: ctp.c_void_p):
        """
        Set the session void pointer.
        """
        self._session_pointer = session

    @property
    def info(self) -> dict[str, str]:
        """
        Dictionary with the GMT version and default paths and parameters.
        """
        if not hasattr(self, "_info"):
            self._info = {
                "version": self.get_default("API_VERSION"),
                "padding": self.get_default("API_PAD"),
                # API_BINDIR points to the directory of the Python interpreter
                # "binary dir": self.get_default("API_BINDIR"),
                "share dir": self.get_default("API_SHAREDIR"),
                # This segfaults for some reason
                # 'data dir': self.get_default("API_DATADIR"),
                "plugin dir": self.get_default("API_PLUGINDIR"),
                "library path": self.get_default("API_LIBRARY"),
                "cores": self.get_default("API_CORES"),
                "grid layout": self.get_default("API_GRID_LAYOUT"),
                "image layout": self.get_default("API_IMAGE_LAYOUT"),
                "binary version": self.get_default("API_BIN_VERSION"),
            }
        return self._info

    def __enter__(self):
        """
        Create a GMT API session.

        Calls :meth:`pygmt.clib.Session.create`.
        """
        self.create("pygmt-session")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the currently open GMT API session.

        Calls :meth:`pygmt.clib.Session.destroy`.
        """
        self.destroy()

    def __getitem__(self, name: str) -> int:
        """
        Get the value of a GMT constant.

        Parameters
        ----------
        name
            The name of the constant (e.g., ``"GMT_SESSION_EXTERNAL"``).

        Returns
        -------
        value
            Integer value of the constant. Do not rely on this value because it might
            change.
        """
        if name not in GMT_CONSTANTS:
            GMT_CONSTANTS[name] = self.get_enum(name)
        return GMT_CONSTANTS[name]

    def get_enum(self, name: str) -> int:
        """
        Get the value of a GMT constant (C enum) from ``gmt_resources.h``.

        Used to set configuration values for other API calls. Wraps ``GMT_Get_Enum``.

        Parameters
        ----------
        name
            The name of the constant (e.g., ``"GMT_SESSION_EXTERNAL"``).

        Returns
        -------
        value
            Integer value of the constant. Do not rely on this value because it might
            change.

        Raises
        ------
        GMTCLibError
            If the constant doesn't exist.
        """
        c_get_enum = self.get_libgmt_func(
            "GMT_Get_Enum", argtypes=[ctp.c_void_p, ctp.c_char_p], restype=ctp.c_int
        )

        # The C library introduced the void API pointer to GMT_Get_Enum so that it's
        # consistent with other functions. It doesn't use the pointer so we can pass
        # in None (NULL pointer). We can't give it the actual pointer because we need
        # to call GMT_Get_Enum when creating a new API session pointer (chicken-and-egg
        # type of thing).
        session = None
        value = c_get_enum(session, name.encode())
        if value is None or value == -99999:
            msg = f"Constant '{name}' doesn't exist in libgmt."
            raise GMTCLibError(msg)
        return value

    def get_libgmt_func(
        self, name: str, argtypes: list | None = None, restype=None
    ) -> Callable:
        """
        Get a ctypes function from the libgmt shared library.

        Assigns the argument and return type conversions for the function.

        Use this method to access a C function from libgmt.

        Parameters
        ----------
        name
            The name of the GMT API function.
        argtypes
            List of ctypes types used to convert the Python input arguments for the API
            function.
        restype : ctypes type
            The ctypes type used to convert the input returned by the function into a
            Python type.

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
        >>> type(func)
        <class 'ctypes.CDLL.__init__.<locals>._FuncPtr'>
        """
        if not hasattr(self, "_libgmt"):
            self._libgmt = _libgmt
        function = getattr(self._libgmt, name)
        if argtypes is not None:
            function.argtypes = argtypes
        if restype is not None:
            function.restype = restype
        return function

    def create(self, name: str) -> None:
        """
        Create a new GMT C API session.

        This is required before most other methods of :class:`pygmt.clib.Session` can be
        called.

        .. warning::

            Usage of :class:`pygmt.clib.Session` as a context manager in a ``with``
            block is preferred over calling :meth:`pygmt.clib.Session.create` and
            :meth:`pygmt.clib.Session.destroy` manually.

        Calls ``GMT_Create_Session`` and generates a new ``GMTAPI_CTRL`` struct, which
        is a :class:`ctypes.c_void_p` pointer. Sets the ``session_pointer`` attribute to
        this pointer.

        Remember to terminate the current session using
        :meth:`pygmt.clib.Session.destroy` before creating a new one.

        Parameters
        ----------
        name
            A name for this session. Doesn't really affect the outcome.
        """
        # Check if there is a currently open session by accessing the "session_pointer"
        # attribute. If not, it will raise the GMTCLibNoSessionError exception and we're
        # free to create a new one. Otherwise, we will raise a GMTCLibError exception.
        try:
            _ = self.session_pointer
            msg = (
                "Failed to create a GMT API session: "
                "There is currently an open session. Must destroy it first."
            )
            raise GMTCLibError(msg)
        except GMTCLibNoSessionError:
            pass

        c_create_session = self.get_libgmt_func(
            "GMT_Create_Session",
            argtypes=[ctp.c_char_p, ctp.c_uint, ctp.c_uint, ctp.c_void_p],
            restype=ctp.c_void_p,
        )

        # Capture the output printed by GMT into this list. Will use it later to
        # generate error messages for the exceptions raised by API calls.
        self._error_log: list[str] = []

        @ctp.CFUNCTYPE(ctp.c_int, ctp.c_void_p, ctp.c_char_p)
        def print_func(file_pointer, message):  # noqa: ARG001
            """
            Callback function that the GMT C API will use to print log and error
            messages.

            We'll capture the messages and print them to stderr so that they will show
            up on the Jupyter notebook.
            """
            # TODO(GMT>6.5.0): Remove the workaround for upstream bug in GMT<=6.5.0.
            # Have to use try..except due to upstream GMT bug in GMT<=6.5.0.
            # See https://github.com/GenericMappingTools/pygmt/issues/3205.
            try:
                message = message.decode().strip()
            except UnicodeDecodeError:
                return 0
            self._error_log.append(message)
            # Flush to make sure the messages are printed even if we have a crash.
            print(message, file=sys.stderr, flush=True)  # noqa: T201
            return 0

        # Need to store a copy of the function because ctypes doesn't and it will be
        # garbage collected otherwise
        self._print_callback = print_func

        padding = self["GMT_PAD_DEFAULT"]
        # GMT_SESSION_EXTERNAL: GMT is called by an external wrapper.
        # GMT_SESSION_NOGDALCLOSE: Do not call GDALDestroyDriverManager when using GDAL.
        session_type = self["GMT_SESSION_EXTERNAL"] + self["GMT_SESSION_NOGDALCLOSE"]
        session = c_create_session(name.encode(), padding, session_type, print_func)

        if session is None:
            msg = f"Failed to create a GMT API session:\n{self._error_message}"
            raise GMTCLibError(msg)

        self.session_pointer = session

    @property
    def _error_message(self) -> str:
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

            Usage of :class:`pygmt.clib.Session` as a context manager in a ``with``
            block is preferred over calling :meth:`pygmt.clib.Session.create` and
            :meth:`pygmt.clib.Session.destroy` manually.

        Calls ``GMT_Destroy_Session`` to terminate and free the memory of a registered
        ``GMTAPI_CTRL`` session (the pointer for this struct is stored in the
        ``session_pointer`` attribute).

        Always use this method after you are done using a C API session. The session
        needs to be destroyed before creating a new one. Otherwise, some of the
        configuration files might be left behind and can influence subsequent API calls.

        Sets the ``session_pointer`` attribute to ``None``.
        """
        c_destroy_session = self.get_libgmt_func(
            "GMT_Destroy_Session", argtypes=[ctp.c_void_p], restype=ctp.c_int
        )

        status = c_destroy_session(self.session_pointer)
        if status:
            msg = f"Failed to destroy GMT API session:\n{self._error_message}"
            raise GMTCLibError(msg)

        self.session_pointer = None

    def get_default(self, name: str) -> str:
        """
        Get the value of a GMT configuration parameter or a GMT API parameter.

        In addition to the long list of GMT configuration parameters, the following API
        parameter names are also supported:

        * ``"API_VERSION"``: The GMT API version
        * ``"API_PAD"``: The grid padding setting
        * ``"API_BINDIR"``: The binary file directory
        * ``"API_SHAREDIR"``: The share directory
        * ``"API_DATADIR"``: The data directory
        * ``"API_PLUGINDIR"``: The plugin directory
        * ``"API_LIBRARY"``: The core library path
        * ``"API_CORES"``: The number of cores
        * ``"API_IMAGE_LAYOUT"``: The image/band layout
        * ``"API_GRID_LAYOUT"``: The grid layout
        * ``"API_BIN_VERSION"``: The GMT binary version (with git information)

        Parameters
        ----------
        name
            The name of the GMT configuration parameter (e.g., ``"PROJ_LENGTH_UNIT"``)
            or a GMT API parameter (e.g., ``"API_VERSION"``).

        Returns
        -------
        value
            The current value for the parameter.

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
        value = ctp.create_string_buffer(4096)
        status = c_get_default(self.session_pointer, name.encode(), value)
        if status != 0:
            msg = f"Error getting value for '{name}' (error code {status})."
            raise GMTCLibError(msg)
        return value.value.decode()

    def get_common(self, option: str) -> bool | int | float | np.ndarray:
        """
        Inquire if a GMT common option has been set and return its current value if
        possible.

        Parameters
        ----------
        option
            The GMT common option to check. Valid options are ``"B"``, ``"I"``, ``"J"``,
            ``"R"``, ``"U"``, ``"V"``, ``"X"``, ``"Y"``, ``"a"``, ``"b"``, ``"f"``,
            ``"g"``, ``"h"``, ``"i"``, ``"n"``, ``"o"``, ``"p"``, ``"r"``, ``"s"``,
            ``"t"``, and ``":"``.

        Returns
        -------
        value
            Whether the option was set or its value. If the option was not set, return
            ``False``. Otherwise, the return value depends on the choice of the option.

            - options ``"B"``, ``"J"``, ``"U"``, ``"g"``, ``"n"``, ``"p"``, and ``"s"``:
              return ``True`` if set, else ``False`` (bool)
            - ``"I"``: 2-element array for the increments (float)
            - ``"R"``: 4-element array for the region (float)
            - ``"V"``: the verbose level (int)
            - ``"X"``: the xshift (float)
            - ``"Y"``: the yshift (float)
            - ``"a"``: geometry of the dataset (int)
            - ``"b"``: return 0 if ``-bi`` was set and 1 if ``-bo`` was set (int)
            - ``"f"``: return 0 if ``-fi`` was set and 1 if ``-fo`` was set (int)
            - ``"h"``: whether to delete existing header records (int)
            - ``"i"``: number of input columns (int)
            - ``"o"``: number of output columns (int)
            - ``"r"``: registration type (int)
            - ``"t"``: 2-element array for the transparency (float)
            - ``":"``: return 0 if ``-:i`` was set and 1 if ``-:o`` was set (int)

        Examples
        --------
        >>> with Session() as lib:
        ...     lib.call_module(
        ...         "basemap", ["-R0/10/10/15", "-JX5i/2.5i", "-Baf", "-Ve"]
        ...     )
        ...     region = lib.get_common("R")
        ...     projection = lib.get_common("J")
        ...     timestamp = lib.get_common("U")
        ...     verbose = lib.get_common("V")
        ...     lib.call_module("plot", ["-T", "-Xw+1i", "-Yh-1i"])
        ...     xshift = lib.get_common("X")  # xshift/yshift are in inches
        ...     yshift = lib.get_common("Y")
        >>> print(region, projection, timestamp, verbose, xshift, yshift)
        [ 0. 10. 10. 15.] True False 3 6.0 1.5
        >>> with Session() as lib:
        ...     lib.call_module("basemap", ["-R0/10/10/15", "-JX5i/2.5i", "-Baf"])
        ...     lib.get_common("A")
        Traceback (most recent call last):
        ...
        pygmt.exceptions.GMTValueError: Invalid GMT common option: 'A'. Expected ...
        """
        valid_options = "BIJRUVXYabfghinoprst:"
        if option not in valid_options:
            raise GMTValueError(
                option, description="GMT common option", choices=valid_options
            )

        c_get_common = self.get_libgmt_func(
            "GMT_Get_Common",
            argtypes=[ctp.c_void_p, ctp.c_uint, ctp.POINTER(ctp.c_double)],
            restype=ctp.c_int,
        )
        value = np.empty(6, np.float64)  # numpy array to store the value of the option
        status = c_get_common(
            self.session_pointer,
            ord(option),
            value.ctypes.data_as(ctp.POINTER(ctp.c_double)),
        )

        if status == self["GMT_NOTSET"]:  # GMT_NOTSET (-1) means the option is not set
            return False
        if status == 0:  # Option is set and no other value is returned.
            return True

        # Otherwise, option is set and values are returned.
        match option:
            case "I" | "R" | "t":
                # Option values (in double type) are returned via the 'value' array.
                # 'status' is number of valid values in the array.
                return value[:status]
            case "X" | "Y":  # Only one valid element in the array.
                return value[0]
            case _:  # 'status' is the option value (in integer type).
                return status

    def call_module(self, module: str, args: str | list[str]) -> None:
        """
        Call a GMT module with the given arguments.

        Wraps ``GMT_Call_Module``.

        The ``GMT_Call_Module`` API function supports passing module arguments in three
        different ways:

        1. Pass a single string that contains whitespace-separated module arguments.
        2. Pass a list of strings and each string contains a module argument.
        3. Pass a list of ``GMT_OPTION`` data structure.

        Both options 1 and 2 are implemented in this function, but option 2 is preferred
        because it can correctly handle special characters like whitespaces and
        quotation marks in module arguments.

        Parameters
        ----------
        module
            The GMT module name to be called (``"coast"``, ``"basemap"``, etc).
        args
            Module arguments that will be passed to the GMT module. It can be either
            a single string (e.g., ``"-R0/5/0/10 -JX10c -BWSen+t'My Title'"``) or a list
            of strings (e.g., ``["-R0/5/0/10", "-JX10c", "-BWSEN+tMy Title"]``).

        Raises
        ------
        GMTTypeError
            If the ``args`` argument is not a string or a list of strings.
        GMTCLibError
            If the returned status code of the function is non-zero.
        """
        c_call_module = self.get_libgmt_func(
            "GMT_Call_Module",
            argtypes=[ctp.c_void_p, ctp.c_char_p, ctp.c_int, ctp.c_void_p],
            restype=ctp.c_int,
        )

        # 'args' can be (1) a single string or (2) a list of strings.
        argv: bytes | ctp.Array[ctp.c_char_p] | None
        if isinstance(args, list):
            # 'args' is a list of strings and each string contains a module argument.
            # In this way, GMT can correctly handle option arguments with whitespaces or
            # quotation marks. This is the preferred way to pass arguments to the GMT
            # API and is used for PyGMT >= v0.12.0.
            mode = len(args)  # 'mode' is the number of arguments.
            # Pass a null pointer if no arguments are specified.
            argv = strings_to_ctypes_array(args) if mode != 0 else None
        elif isinstance(args, str):
            # 'args' is a single string that contains whitespace-separated arguments.
            # In this way, we need to correctly handle option arguments that contain
            # whitespaces or quotation marks. It's used in PyGMT <= v0.11.0 but is no
            # longer recommended.
            mode = self["GMT_MODULE_CMD"]
            argv = args.encode()
        else:
            raise GMTTypeError(
                type(args),
                reason="Parameter 'args' must either be a list of strings (recommended) or a string.",
            )

        status = c_call_module(self.session_pointer, module.encode(), mode, argv)
        if status != 0:
            msg = f"Module '{module}' failed with status code {status}:\n{self._error_message}"
            raise GMTCLibError(msg)

    def create_data(
        self,
        family: str,
        geometry: str,
        mode: str,
        dim: Sequence[int] | None = None,
        ranges: Sequence[float] | None = None,
        inc: Sequence[float] | None = None,
        registration: Literal[
            "GMT_GRID_NODE_REG", "GMT_GRID_PIXEL_REG"
        ] = "GMT_GRID_NODE_REG",
        pad: int | None = None,
    ) -> ctp.c_void_p:
        """
        Create an empty GMT data container and allocate space to hold data.

        Valid data families and geometries are in ``FAMILIES`` and ``GEOMETRIES``.

        There are two ways to define the dimensions needed to actually allocate memory:

        1. Via ``ranges``, ``inc`` and ``registration``.
        2. Via ``dim`` and ``registration``.

           ``dim`` contains up to 4 values and they have different meanings for
           different GMT data families:

           For ``GMT_DATASET``:

           - 0: number of tables
           - 1: number of segments per table
           - 2: number of rows per segment
           - 3: number of columns per row

           For ``GMT_VECTOR``:

           - 0: number of columns
           - 1: number of rows [optional, can be 0 if unknown]
           - 2: data type (e.g., ``GMT_DOUBLE``) [Will be overwritten by ``put_vector``]

           For ``GMT_GRID``/``GMT_IMAGE``/``GMT_CUBE``/``GMT_MATRIX``:

           - 0: number of columns
           - 1: number of rows
           - 2: number of bands or layers [Ignored for ``GMT_GRID``]
           - 3: data type (e.g., ``GMT_DOUBLE``) [For ``GMT_MATRIX`` only, but will be
             overwritten by ``put_matrix``]

           In other words, ``inc`` is assumed to be 1.0, and ``ranges`` is
           [0, dim[0], 0, dim[1]] for pixel registration or
           [0, dim[0]-1.0, 0, dim[1]-1.0] for grid registration.


        When creating a grid/image/cube, you can do it in one or two steps:

        1. Call this function with ``mode="GMT_CONTAINER_AND_DATA"``. This creates
           a header and allocates a grid or an image
        2. Call this function twice:

           1. First with ``mode="GMT_CONTAINER_ONLY"``, to create a header only and
              compute the dimensions based on other parameters
           2. Second with ``mode="GMT_DATA_ONLY"``, to allocate the grid/image/cube
              array based on the dimensions already set. This time, you pass NULL for
              ``dim``/``ranges``/``inc``/``registration``/``pad`` and let ``data`` be
              the void pointer returned in the first step.

           **Note**: This is not implemented yet, since this function doesn't have the
           ``data`` parameter.

        Parameters
        ----------
        family
            A valid GMT data family name (e.g., ``"GMT_IS_DATASET"``). See ``FAMILIES``
            for valid names.
        geometry
            A valid GMT data geometry name (e.g., ``"GMT_IS_POINT"``). See
            ``GEOMETRIES`` for valid names.
        mode
            A valid GMT data mode. See ``MODES`` for valid names. For
            ``GMT_IS_DATASET``/``GMT_IS_MATRIX``/``GMT_IS_VECTOR``, adding
            ``GMT_WITH_STRINGS`` to the ``mode`` will allocate the corresponding arrays
            of string pointers.
        dim
            The dimensions of the dataset, as explained above. If ``None``, will pass in
            the NULL pointer.
        ranges
            The data extent.
        inc
            The increments between points of the dataset.
        registration
            The node registration. Can be ``"GMT_GRID_PIXEL_REG"`` or
            ``"GMT_GRID_NODE_REG"``.
        pad
            The padding for ``GMT_IS_GRID``/``GMT_IS_IMAGE``/``GMT_IS_CUBE``. If
            ``None``, defaults to ``"GMT_PAD_DEFAULT"``.

            For ``GMT_IS_MATRIX``, it can be:

            - 0: default row/col orientation [Default]
            - 1: row-major format (C)
            - 2: column-major format (FORTRAN)

        Returns
        -------
        data_ptr
            A ctypes pointer (an integer) to the allocated GMT data container.
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
                ctp.c_void_p,  # data
            ],
            restype=ctp.c_void_p,
        )

        family_int = self._parse_constant(family, valid=FAMILIES, valid_modifiers=VIAS)
        mode_int = self._parse_constant(
            mode,
            valid=MODES,
            valid_modifiers=MODE_MODIFIERS,
        )
        geometry_int = self._parse_constant(geometry, valid=GEOMETRIES)
        registration_int = self._parse_constant(registration, valid=REGISTRATIONS)

        # Convert dim, ranges, and inc to ctypes arrays if given (will be None if not
        # given to represent NULL pointers)
        dim_ctp = sequence_to_ctypes_array(dim, ctp.c_uint64, 4)
        ranges_ctp = sequence_to_ctypes_array(ranges, ctp.c_double, 4)
        inc_ctp = sequence_to_ctypes_array(inc, ctp.c_double, 2)

        # Use a NULL pointer (None) for existing data to indicate that the container
        # should be created empty. Fill it in later using put_vector and put_matrix.
        data_ptr = c_create_data(
            self.session_pointer,
            family_int,
            geometry_int,
            mode_int,
            dim_ctp,
            ranges_ctp,
            inc_ctp,
            registration_int,
            self._parse_pad(family, pad),
            None,
        )

        if data_ptr is None:
            msg = "Failed to create an empty GMT data pointer."
            raise GMTCLibError(msg)
        return data_ptr

    def _parse_pad(self, family: str, pad: int | None) -> int:
        """
        Parse and return an appropriate value for pad if ``None`` is given.

        Pad is a bit tricky because, for matrix types, pad control the matrix ordering
        (row or column major). Using the default pad will set it to column major and
        mess things up with the numpy arrays.
        """
        if pad is None:
            pad = 0 if "MATRIX" in family else self["GMT_PAD_DEFAULT"]
        return pad

    def _parse_constant(
        self,
        constant: str,
        valid: Sequence[str],
        valid_modifiers: Sequence[str] | None = None,
    ) -> int:
        """
        Parse a constant, convert it to an integer, and validate it.

        The GMT C API takes certain defined constants, like ``"GMT_IS_GRID"``, that need
        to be validated and converted to integer values using
        :meth:`pygmt.clib.Session.__getitem__`.

        The constants can also take a modifier by appending another constant name, e.g.,
        ``"GMT_IS_GRID|GMT_VIA_MATRIX"``. The two parts must be converted separately and
        their values are added.

        If no valid modifiers are given, then will assume that modifiers are not
        allowed. In this case, will raise a :class:`pygmt.exceptions.GMTValueError`
        exception if given a modifier.

        Parameters
        ----------
        constant
            The name of a valid GMT API constant, with an optional modifier.
        valid
            A list of valid values for the constant. Will raise a GMTValueError
            exception if the given value is not in the list.
        valid_modifiers
            A list of valid modifiers that can be added to the constant. If ``None``,
            no modifiers are allowed.
        """
        parts = constant.split("|")
        name = parts[0]
        nmodifiers = len(parts) - 1

        if name not in valid:
            raise GMTValueError(name, description="constant name", choices=valid)

        match nmodifiers:
            case 1 if valid_modifiers is None:
                raise GMTValueError(
                    constant,
                    reason="Constant modifiers are not allowed since valid values were not given.",
                )
            case 1 if valid_modifiers is not None and parts[1] not in valid_modifiers:
                raise GMTValueError(
                    parts[1], description="constant modifier", choices=valid_modifiers
                )
            case n if n > 1:
                raise GMTValueError(
                    constant,
                    reason=f"Only one modifier is allowed in constants but {nmodifiers} given.",
                )

        integer_value = sum(self[part] for part in parts)
        return integer_value

    def _check_dtype_and_dim(self, array: np.ndarray, ndim: int) -> int:
        """
        Check that a numpy array has the given number of dimensions and is a valid data
        type.

        Parameters
        ----------
        array
            The array to be tested.
        ndim
            The desired number of array dimensions.

        Returns
        -------
        gmt_type
            The GMT constant value representing this data type.

        Raises
        ------
        GMTValueError
            If the array has the wrong number of dimensions.
        GMTTypeError
            If the array is an unsupported data type.

        Examples
        --------
        >>> import numpy as np
        >>> data = np.array([1, 2, 3], dtype=np.float64)
        >>> with Session() as lib:
        ...     gmttype = lib._check_dtype_and_dim(data, ndim=1)
        ...     gmttype == lib["GMT_DOUBLE"]
        True
        >>> data = np.ones((5, 2), dtype=np.float32)
        >>> with Session() as lib:
        ...     gmttype = lib._check_dtype_and_dim(data, ndim=2)
        ...     gmttype == lib["GMT_FLOAT"]
        True
        """
        # Check that the array has the given number of dimensions.
        if array.ndim != ndim:
            raise GMTValueError(
                array.ndim,
                description="array dimension",
                reason=f"Expected a numpy {ndim}-D array, got {array.ndim}-D.",
            )

        # 1-D arrays can be numeric or text, 2-D arrays can only be numeric.
        valid_dtypes = DTYPES if ndim == 1 else DTYPES_NUMERIC
        if (dtype := array.dtype.type) not in valid_dtypes:
            raise GMTTypeError(dtype)
        return self[DTYPES[dtype]]

    def put_vector(
        self, dataset: ctp.c_void_p, column: int, vector: np.ndarray
    ) -> None:
        r"""
        Attach a 1-D numpy array as a column on a GMT dataset.

        Use this function to attach numpy array data to a GMT dataset and pass it to GMT
        modules. Wraps ``GMT_Put_Vector``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data` first with
        ``family="GMT_IS_DATASET|GMT_VIA_VECTOR"``.

        Not all numpy dtypes are supported, only: int8, int16, int32, int64, longlong,
        uint8, uint16, uint32, uint64, ulonglong, float32, float64, str\_, datetime64,
        and timedelta64.

        .. warning::
            The numpy array must be C contiguous in memory. Use
            :func:`numpy.ascontiguousarray` to make sure your vector is contiguous (it
            won't copy if it already is).

        Parameters
        ----------
        dataset
            The ctypes void pointer to a ``GMT_VECTOR`` data container. Create it with
            :meth:`pygmt.clib.Session.create_data`.
        column
            The column number of this vector in the dataset (starting from 0).
        vector
            The array that will be attached to the dataset. Must be a 1-D C contiguous
            array.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Vector`` exits with a non-zero status.
        """
        c_put_vector = self.get_libgmt_func(
            "GMT_Put_Vector",
            argtypes=[ctp.c_void_p, ctp.c_void_p, ctp.c_uint, ctp.c_uint, ctp.c_void_p],
            restype=ctp.c_int,
        )

        vector_pointer: ctp.Array | ctp.c_void_p
        gmt_type = self._check_dtype_and_dim(vector, ndim=1)
        if gmt_type in {self["GMT_TEXT"], self["GMT_DATETIME"]}:
            if gmt_type == self["GMT_DATETIME"]:
                vector = np.datetime_as_string(vector)
            vector_pointer = strings_to_ctypes_array(vector)
        else:
            vector_pointer = vector.ctypes.data_as(ctp.c_void_p)
        status = c_put_vector(
            self.session_pointer, dataset, column, gmt_type, vector_pointer
        )
        if status != 0:
            msg = (
                f"Failed to put vector of type {vector.dtype} in column {column} of "
                "dataset."
            )
            raise GMTCLibError(msg)

    def put_strings(
        self, dataset: ctp.c_void_p, family: str, strings: np.ndarray
    ) -> None:
        """
        Attach a 1-D numpy array of dtype str as a column on a GMT dataset.

        Use this function to attach string type numpy array data to a GMT dataset and
        pass it to GMT modules. Wraps ``GMT_Put_Strings``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data` first.

        .. warning::
            The numpy array must be C contiguous in memory. If it comes from a column
            slice of a 2-D array, for example, you will have to make a copy. Use
            :func:`numpy.ascontiguousarray` to make sure your vector is contiguous (it
            won't copy if it already is).

        Parameters
        ----------
        dataset
            The ctypes void pointer to a ``GMT_VECTOR``/``GMT_MATRIX`` data container.
            Create it with :meth:`pygmt.clib.Session.create_data`.
        family
            The family type of the dataset. Can be either ``GMT_IS_VECTOR`` or
            ``GMT_IS_MATRIX``.
        strings
            The array that will be attached to the dataset. Must be a 1-D C contiguous
            array.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Strings`` exits with a non-zero status.
        """
        c_put_strings = self.get_libgmt_func(
            "GMT_Put_Strings",
            argtypes=[
                ctp.c_void_p,  # V_API
                ctp.c_uint,  # family
                ctp.c_void_p,  # object
                ctp.POINTER(ctp.c_char_p),  # array
            ],
            restype=ctp.c_int,
        )

        family_int = self._parse_constant(
            family, valid=FAMILIES, valid_modifiers=METHODS
        )
        strings_pointer = strings_to_ctypes_array(strings)
        status = c_put_strings(
            self.session_pointer, family_int, dataset, strings_pointer
        )
        if status != 0:
            msg = f"Failed to put strings of type {strings.dtype} into dataset."
            raise GMTCLibError(msg)

    def put_matrix(
        self, dataset: ctp.c_void_p, matrix: np.ndarray, pad: int = 0
    ) -> None:
        """
        Attach a 2-D numpy array to a GMT dataset.

        Use this function to attach numpy array data to a GMT dataset and pass it to GMT
        modules. Wraps ``GMT_Put_Matrix``.

        The dataset must be created by :meth:`pygmt.clib.Session.create_data` first with
        ``family="GMT_IS_DATASET|GMT_VIA_MATRIX"``.

        Not all numpy dtypes are supported, only: int8, int16, int32, int64, longlong,
        uint8, uint16, uint32, uint64, ulonglong, float32, and float64.

        .. warning::
            The numpy array must be C contiguous in memory. Use
            :func:`numpy.ascontiguousarray` to make sure your matrix is contiguous (it
            won't copy if it already is).

        Parameters
        ----------
        dataset
            The ctypes void pointer to a ``GMT_MATRIX`` data container. Create it with
            :meth:`pygmt.clib.Session.create_data`.
        matrix
            The array that will be attached to the dataset. Must be a 2-D C contiguous
            array.
        pad
            The amount of padding that should be added to the matrix. Use when creating
            grids for modules that require padding.

        Raises
        ------
        GMTCLibError
            If given invalid input or ``GMT_Put_Matrix`` exits with a non-zero status.
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
            msg = f"Failed to put matrix of type {matrix.dtype}."
            raise GMTCLibError(msg)

    def read_data(
        self,
        infile: str,
        kind: Literal["dataset", "grid", "image"],
        family: str | None = None,
        geometry: str | None = None,
        mode: str = "GMT_READ_NORMAL",
        region: Sequence[float] | None = None,
        data=None,
    ):
        """
        Read a data file into a GMT data container.

        Wraps ``GMT_Read_Data`` but only allows reading from a file. The function
        definition is different from the original C API function.

        Parameters
        ----------
        infile
            The input file name.
        kind
            The data kind of the input file. Valid values are ``"dataset"``, ``"grid"``
            and ``"image"``.
        family
            A valid GMT data family name (e.g., ``"GMT_IS_DATASET"``). See the
            ``FAMILIES`` attribute for valid names. If ``None``, will determine the data
            family from the ``kind`` parameter.
        geometry
            A valid GMT data geometry name (e.g., ``"GMT_IS_POINT"``). See the
            ``GEOMETRIES`` attribute for valid names. If ``None``, will determine the
            data geometry from the ``kind`` parameter.
        mode
            How the data is to be read from the file. This option varies depending on
            the given family. See the
            :gmt-docs:`GMT API documentation <devdocs/api.html#import-from-a-file-stream-or-handle>`
            for details. Default is ``GMT_READ_NORMAL`` which corresponds to the default
            read mode value of 0 in the ``GMT_enum_read`` enum.
        region
            Subregion of the data, in the form of [xmin, xmax, ymin, ymax, zmin, zmax].
            If ``None``, the whole data is read.
        data
            ``None`` or the pointer returned by this function after a first call. It's
            useful when reading grids/images/cubes in two steps (get a grid/image/cube
            structure with a header, then read the data).

        Returns
        -------
        Pointer to the data container, or ``None`` if there were errors.

        Raises
        ------
        GMTCLibError
            If the GMT API function fails to read the data.
        """  # noqa: W505
        c_read_data = self.get_libgmt_func(
            "GMT_Read_Data",
            argtypes=[
                ctp.c_void_p,  # V_API
                ctp.c_uint,  # family
                ctp.c_uint,  # method
                ctp.c_uint,  # geometry
                ctp.c_uint,  # mode
                ctp.POINTER(ctp.c_double),  # wesn
                ctp.c_char_p,  # infile
                ctp.c_void_p,  # data
            ],
            restype=ctp.c_void_p,  # data_ptr
        )

        # Determine the family, geometry and data container from kind
        _family, _geometry, dtype = {
            "dataset": ("GMT_IS_DATASET", "GMT_IS_PLP", _GMT_DATASET),
            "grid": ("GMT_IS_GRID", "GMT_IS_SURFACE", _GMT_GRID),
            "image": ("GMT_IS_IMAGE", "GMT_IS_SURFACE", _GMT_IMAGE),
        }[kind]
        if family is None:
            family = _family
        if geometry is None:
            geometry = _geometry

        data_ptr = c_read_data(
            self.session_pointer,
            self[family],
            self["GMT_IS_FILE"],  # Reading from a file
            self[geometry],
            self[mode],
            sequence_to_ctypes_array(region, ctp.c_double, 6),
            infile.encode(),
            data,
        )
        if data_ptr is None:
            msg = f"Failed to read dataset from '{infile}'."
            raise GMTCLibError(msg)
        return ctp.cast(data_ptr, ctp.POINTER(dtype))

    def write_data(self, family, geometry, mode, wesn, output, data) -> None:
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
            sequence_to_ctypes_array(wesn, ctp.c_double, 6),
            output.encode(),
            data,
        )
        if status != 0:
            msg = f"Failed to write dataset to '{output}'."
            raise GMTCLibError(msg)

    @contextlib.contextmanager
    def open_virtualfile(
        self,
        family: str,
        geometry: str,
        direction: str,
        data: ctp.c_void_p | None,
    ) -> Generator[str, None, None]:
        """
        Open a GMT virtual file associated with a data object for reading or writing.

        GMT uses a virtual file scheme to pass in data or get data from API modules. Use
        it to pass in your GMT data structure (created using
        :meth:`pygmt.clib.Session.create_data`) to a module that expects an input file,
        or get the output from a module that writes to a file.

        Use in a ``with`` block. Will automatically close the virtual file when leaving
        the ``with`` block. Because of this, no wrapper for ``GMT_Close_VirtualFile``
        is provided.

        Parameters
        ----------
        family
            A valid GMT data family name (e.g., ``"GMT_IS_DATASET"``). Should be the
            same as the one you used to create your data structure.
        geometry
            A valid GMT data geometry name (e.g., ``"GMT_IS_POINT"``). Should be the
            same as the one you used to create your data structure.
        direction
            Either ``"GMT_IN"`` or ``"GMT_OUT"`` to indicate if passing data to GMT or
            getting it out of GMT, respectively. By default, GMT can modify the data you
            pass in. Add modifier ``"GMT_IS_REFERENCE"`` to tell GMT the data are
            read-only, or ``"GMT_IS_DUPLICATE"`` to tell GMT to duplicate the data.
        data
            The ctypes void pointer to the GMT data structure. For output (i.e.,
            ``direction="GMT_OUT"``), it can be ``None`` to have GMT automatically
            allocate the output GMT data structure.

        Yields
        ------
        vfname
            The name of the virtual file that you can pass to a GMT module.

        Examples
        --------

        >>> from pygmt.helpers import GMTTempFile
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
        ...         dim=[2, 5, lib["GMT_INT"], 0],  # ncolumns, nrows, dtype, unused
        ...     )
        ...     lib.put_vector(dataset, column=0, vector=x)
        ...     lib.put_vector(dataset, column=1, vector=y)
        ...     # Add the dataset to a virtual file
        ...     vfargs = (family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset)
        ...     with lib.open_virtualfile(*vfargs) as vfile:
        ...         # Send the output to a temp file so that we can read it
        ...         with GMTTempFile() as ofile:
        ...             lib.call_module("info", [vfile, f"->{ofile.name}"])
        ...             print(ofile.read().strip())
        <vector memory>: N = 5 <0/4> <5/9>
        """
        c_open_virtualfile = self.get_libgmt_func(
            "GMT_Open_VirtualFile",
            argtypes=[
                ctp.c_void_p,  # V_API
                ctp.c_uint,  # family
                ctp.c_uint,  # geometry
                ctp.c_uint,  # direction
                ctp.c_void_p,  # data
                ctp.c_char_p,  # name
            ],
            restype=ctp.c_int,
        )

        c_close_virtualfile = self.get_libgmt_func(
            "GMT_Close_VirtualFile",
            argtypes=[ctp.c_void_p, ctp.c_char_p],  # V_API, name
            restype=ctp.c_int,
        )

        family_int = self._parse_constant(family, valid=FAMILIES, valid_modifiers=VIAS)
        geometry_int = self._parse_constant(geometry, valid=GEOMETRIES)
        direction_int = self._parse_constant(
            direction, valid=DIRECTIONS, valid_modifiers=METHODS
        )

        buff = ctp.create_string_buffer(self["GMT_VF_LEN"])
        status = c_open_virtualfile(
            self.session_pointer, family_int, geometry_int, direction_int, data, buff
        )
        if status != 0:
            msg = (
                f"Failed to create a virtual file with {family=}, {geometry=}, "
                f"{direction=}."
            )
            raise GMTCLibError(msg)

        vfname = buff.value.decode()
        try:
            yield vfname
        finally:
            status = c_close_virtualfile(self.session_pointer, vfname.encode())
            if status != 0:
                msg = f"Failed to close virtual file '{vfname}'."
                raise GMTCLibError(msg)

    @contextlib.contextmanager
    def virtualfile_from_vectors(self, vectors: Sequence) -> Generator[str, None, None]:
        """
        Store a sequence of 1-D vectors as columns of a dataset inside a virtual file.

        Use the virtual file name to pass the dataset with your vectors to a GMT module.

        Context manager (use in a ``with`` block). Yields the virtual file name that you
        can pass as an argument to a GMT module call. Closes the virtual file upon exit
        of the ``with`` block.

        Use this instead of creating the data container and virtual file by hand with
        :meth:`pygmt.clib.Session.create_data`, :meth:`pygmt.clib.Session.put_vector`,
        and :meth:`pygmt.clib.Session.open_virtualfile`.

        If the arrays are C contiguous blocks of memory, they will be passed without
        copying to GMT. If they are not (e.g., they are columns of a 2-D array), they
        will need to be copied to a contiguous block.

        Parameters
        ----------
        vectors
            A sequence of vectors that will be stored in the dataset. All must be of the
            same size.

        Yields
        ------
        fname
            The name of virtual file. Pass this as a file name argument to a GMT module.

        Examples
        --------

        >>> from pygmt.helpers import GMTTempFile
        >>> import numpy as np
        >>> import pandas as pd
        >>> x = [1, 2, 3]
        >>> y = np.array([4, 5, 6])
        >>> z = pd.Series([7, 8, 9])
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_vectors((x, y, z)) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module("info", [fin, f"->{fout.name}"])
        ...             print(fout.read().strip())
        <vector memory>: N = 3 <1/3> <4/6> <7/9>
        """
        # Conversion to a C-contiguous array needs to be done here and not in put_vector
        # or put_strings because we need to maintain a reference to the copy while it is
        # being used by the C API. Otherwise, the array would be garbage collected and
        # the memory freed. Creating it in this context manager guarantees that the copy
        # will be around until the virtual file is closed. The conversion is implicit in
        # vectors_to_arrays.
        arrays = vectors_to_arrays(vectors)

        columns = len(arrays)
        # Find arrays that are of string dtype from column 3 onwards. Assumes that first
        # 2 columns contains coordinates like longitude, latitude, or datetime string
        # types.
        for col, array in enumerate(arrays[2:]):
            if np.issubdtype(array.dtype, np.str_):
                columns = col + 2
                break

        rows = len(arrays[0])
        if not all(len(i) == rows for i in arrays):
            msg = "All arrays must have same size."
            raise GMTInvalidInput(msg)

        family = "GMT_IS_DATASET|GMT_VIA_VECTOR"
        geometry = "GMT_IS_POINT"

        dataset = self.create_data(
            family,
            geometry,
            mode="GMT_CONTAINER_ONLY",
            dim=[columns, rows, self["GMT_DOUBLE"], 0],
        )

        # Use put_vector for columns with numerical type data
        for col, array in enumerate(arrays[:columns]):
            self.put_vector(dataset, column=col, vector=array)

        # Use put_strings for last column(s) with string type data.
        # Have to use modifier "GMT_IS_DUPLICATE" to duplicate the strings.
        string_arrays = arrays[columns:]
        if string_arrays:
            if len(string_arrays) == 1:
                strings = string_arrays[0]
            elif len(string_arrays) > 1:
                strings = np.array(
                    [" ".join(vals) for vals in zip(*string_arrays, strict=True)],
                    dtype=np.str_,
                )
            self.put_strings(
                dataset, family="GMT_IS_VECTOR|GMT_IS_DUPLICATE", strings=strings
            )

        with self.open_virtualfile(
            family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset
        ) as vfile:
            yield vfile

    @contextlib.contextmanager
    def virtualfile_from_matrix(self, matrix: np.ndarray) -> Generator[str, None, None]:
        """
        Store a 2-D numpy array as a matrix inside a virtual file.

        Use the virtual file name to pass in the data in your matrix to a GMT module.

        Context manager (use in a ``with`` block). Yields the virtual file name that you
        can pass as an argument to a GMT module call. Closes the virtual file upon exit
        of the ``with`` block.

        The virtual file will contain the array as a ``GMT_MATRIX`` data container
        pretending to be a ``GMT_DATASET`` data container.

        **Not meant for creating ``GMT_GRID``**. The grid requires more metadata than
        just the data matrix. Use :meth:`pygmt.clib.Session.virtualfile_from_grid`
        instead.

        Use this instead of creating the data container and virtual file by hand with
        :meth:`pygmt.clib.Session.create_data`, :meth:`pygmt.clib.Session.put_matrix`,
        and :meth:`pygmt.clib.Session.open_virtualfile`.

        The matrix must be C contiguous in memory. If it is not (e.g., it is a slice of
        a larger array), the array will be copied to make sure it is.

        Parameters
        ----------
        matrix
            The matrix that will be included in the GMT data container.

        Yields
        ------
        fname
            The name of virtual file. Pass this as a file name argument to a GMT module.

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
        ...             ses.call_module("info", [fin, f"->{fout.name}"])
        ...             print(fout.read().strip())
        <matrix memory>: N = 4 <0/9> <1/10> <2/11>
        """
        # Conversion to a C-contiguous array needs to be done here and not in put_matrix
        # because we need to maintain a reference to the copy while it is being used by
        # the C API. Otherwise, the array would be garbage collected and the memory
        # freed. Creating it in this context manager guarantees that the copy will be
        # around until the virtual file is closed.
        matrix = np.ascontiguousarray(matrix)
        rows, columns = matrix.shape
        layers = 1

        family = "GMT_IS_DATASET|GMT_VIA_MATRIX"
        geometry = "GMT_IS_POINT"

        dataset = self.create_data(
            family, geometry, mode="GMT_CONTAINER_ONLY", dim=[columns, rows, layers, 0]
        )

        self.put_matrix(dataset, matrix)

        with self.open_virtualfile(
            family, geometry, "GMT_IN|GMT_IS_REFERENCE", dataset
        ) as vfile:
            yield vfile

    @contextlib.contextmanager
    def virtualfile_from_grid(self, grid: xr.DataArray) -> Generator[str, None, None]:
        """
        Store a grid in a virtual file.

        Use the virtual file name to pass in the data in your grid to a GMT module.
        Grids must be :class:`xarray.DataArray` instances.

        Context manager (use in a ``with`` block). Yields the virtual file name that you
        can pass as an argument to a GMT module call. Closes the virtual file upon exit
        of the ``with`` block.

        The virtual file will contain the grid as a ``GMT_MATRIX`` data container with
        extra metadata.

        Use this instead of creating a data container and virtual file by hand with
        :meth:`pygmt.clib.Session.create_data`, :meth:`pygmt.clib.Session.put_matrix`,
        and :meth:`pygmt.clib.Session.open_virtualfile`.

        The grid data matrix must be C contiguous in memory. If it is not (e.g., it is a
        slice of a larger array), the array will be copied to make sure it is.

        Parameters
        ----------
        grid
            The grid that will be included in the virtual file.

        Yields
        ------
        fname
            The name of virtual file. Pass this as a file name argument to a GMT module.

        Examples
        --------

        >>> from pygmt.helpers.testing import load_static_earth_relief
        >>> from pygmt.helpers import GMTTempFile
        >>> data = load_static_earth_relief()
        >>> print(data.shape)
        (14, 8)
        >>> print(data.lon.values.min(), data.lon.values.max())
        -54.5 -47.5
        >>> print(data.lat.values.min(), data.lat.values.max())
        -23.5 -10.5
        >>> print(data.values.min(), data.values.max())
        190.0 981.0
        >>> with Session() as ses:
        ...     with ses.virtualfile_from_grid(data) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module(
        ...                 "grdinfo", [fin, "-L0", "-Cn", f"->{fout.name}"]
        ...             )
        ...             print(fout.read().strip())
        -55 -47 -24 -10 190 981 1 1 8 14 1 1
        >>> # The output is: w e s n z0 z1 dx dy n_columns n_rows reg gtype
        """
        _gtype = {0: "GMT_GRID_IS_CARTESIAN", 1: "GMT_GRID_IS_GEO"}[grid.gmt.gtype]
        _reg = {0: "GMT_GRID_NODE_REG", 1: "GMT_GRID_PIXEL_REG"}[grid.gmt.registration]

        # Conversion to a C-contiguous array needs to be done here and not in put_matrix
        # because we need to maintain a reference to the copy while it is being used by
        # the C API. Otherwise, the array would be garbage collected and the memory
        # freed. Creating it in this context manager guarantees that the copy will be
        # around until the virtual file is closed. The conversion is implicit in
        # dataarray_to_matrix.
        matrix, region, inc = dataarray_to_matrix(grid)

        family = "GMT_IS_GRID|GMT_VIA_MATRIX"
        geometry = "GMT_IS_SURFACE"
        gmt_grid = self.create_data(
            family,
            geometry,
            mode=f"GMT_CONTAINER_ONLY|{_gtype}",
            ranges=region,
            inc=inc,
            registration=_reg,  # type: ignore[arg-type]
        )
        self.put_matrix(gmt_grid, matrix)
        with self.open_virtualfile(
            family, geometry, "GMT_IN|GMT_IS_REFERENCE", gmt_grid
        ) as vfile:
            yield vfile

    @contextlib.contextmanager
    def virtualfile_from_stringio(
        self, stringio: io.StringIO
    ) -> Generator[str, None, None]:
        r"""
        Store a :class:`io.StringIO` object in a virtual file.

        Store the contents of a :class:`io.StringIO` object in a GMT_DATASET container
        and create a virtual file to pass to a GMT module.

        For simplicity, currently we make following assumptions in the StringIO object

        - ``"#"`` indicates a comment line.
        - ``">"`` indicates a segment header.

        Parameters
        ----------
        stringio
            The :class:`io.StringIO` object containing the data to be stored in the
            virtual file.

        Yields
        ------
        fname
            The name of the virtual file.

        Examples
        --------
        >>> import io
        >>> from pygmt.clib import Session
        >>> # A StringIO object containing legend specifications
        >>> stringio = io.StringIO(
        ...     "# Comment\n"
        ...     "H 24p Legend\n"
        ...     "N 2\n"
        ...     "S 0.1i c 0.15i p300/12 0.25p 0.3i My circle\n"
        ... )
        >>> with Session() as lib:
        ...     with lib.virtualfile_from_stringio(stringio) as fin:
        ...         lib.virtualfile_to_dataset(vfname=fin, output_type="pandas")
                                                     0
        0                                 H 24p Legend
        1                                          N 2
        2  S 0.1i c 0.15i p300/12 0.25p 0.3i My circle
        """
        # Parse the io.StringIO object.
        segments = []
        current_segment = {"header": "", "data": []}
        for line in stringio.getvalue().splitlines():
            if line.startswith("#"):  # Skip comments
                continue
            if line.startswith(">"):  # Segment header
                if current_segment["data"]:  # If we have data, start a new segment
                    segments.append(current_segment)
                    current_segment = {"header": "", "data": []}
                current_segment["header"] = line.strip(">").lstrip()
            else:
                current_segment["data"].append(line)  # type: ignore[attr-defined]
        if current_segment["data"]:  # Add the last segment if it has data
            segments.append(current_segment)

        # One table with one or more segments.
        # n_rows is the maximum number of rows/records for all segments.
        # n_columns is the number of numeric data columns, so it's 0 here.
        n_tables = 1
        n_segments = len(segments)
        n_rows = max(len(segment["data"]) for segment in segments)
        n_columns = 0

        # Create the GMT_DATASET container
        family, geometry = "GMT_IS_DATASET", "GMT_IS_TEXT"
        dataset = self.create_data(
            family,
            geometry,
            mode="GMT_CONTAINER_ONLY|GMT_WITH_STRINGS",
            dim=[n_tables, n_segments, n_rows, n_columns],
        )
        table = ctp.cast(dataset, ctp.POINTER(_GMT_DATASET)).contents.table[0].contents
        for i, segment in enumerate(segments):
            seg = table.segment[i].contents
            if segment["header"]:
                seg.header = segment["header"].encode()  # type: ignore[attr-defined]
            seg.text = strings_to_ctypes_array(segment["data"])

        with self.open_virtualfile(family, geometry, "GMT_IN", dataset) as vfile:
            try:
                yield vfile
            finally:
                # Must set the pointers to None to avoid double freeing the memory.
                # Maybe upstream bug.
                for i in range(n_segments):
                    seg = table.segment[i].contents
                    seg.header = None
                    seg.text = None

    # TODO(PyGMT>=0.20.0): Remove the deprecated parameter 'required_z'.
    # TODO(PyGMT>=0.20.0): Remove the deprecated parameter 'extra_arrays'.
    # TODO(PyGMT>=0.20.0): Remove the deprecated parameter 'required_data'.
    @deprecate_parameter(
        "required_data", "required", "v0.16.0", remove_version="v0.20.0"
    )
    def virtualfile_in(  # noqa: PLR0912
        self,
        check_kind=None,
        data=None,
        x=None,
        y=None,
        z=None,
        required=True,
        mincols=2,
        required_z=False,
        extra_arrays=None,
    ):
        """
        Store any data inside a virtual file.

        This convenience function automatically detects the kind of data passed
        into it, and produces a virtualfile that can be passed into GMT later
        on.

        Parameters
        ----------
        check_kind : str or None
            Used to validate the type of data that can be passed in. Choose
            from 'raster', 'vector', or None. Default is None (no validation).
        data
            Any raster or vector data format. This could be a file name or
            path, a raster grid, a vector matrix/arrays, or other supported
            data input.
        x/y/z : 1-D arrays or None
            x, y, and z columns as numpy arrays.
        required : bool
            Set to True when 'data' or ('x' and 'y') is required. Set to False when
            dealing with optional virtual files. Default is True.

            .. versionchanged:: v0.16.0
               The parameter 'required_data' is renamed to 'required'. The parameter
               'required_data' is deprecated in v0.16.0 and will be removed in v0.20.0.
        mincols
            Number of minimum required columns. Default is 2 (i.e. require x and y
            columns).
        required_z : bool
            State whether the 'z' column is required.

            .. deprecated:: v0.16.0
               The parameter 'required_z' will be removed in v0.20.0. Use parameter
               'mincols' instead. E.g., ``required_z=True`` is equivalent to
               ``mincols=3``.
        extra_arrays : list of 1-D arrays
            A list of numpy arrays in addition to x, y, and z. All of these arrays must
            be of the same size as the x/y/z arrays.

            .. deprecated:: v0.16.0
               The parameter 'extra_arrays' will be removed in v0.20.0. Prepare and pass
               a dictionary of arrays instead to the `data` parameter. E.g.,
               ``data={"x": x, "y": y, "size": size}``.

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
        ...     with ses.virtualfile_in(check_kind="vector", data=data) as fin:
        ...         # Send the output to a file so that we can read it
        ...         with GMTTempFile() as fout:
        ...             ses.call_module("info", [fin, f"->{fout.name}"])
        ...             print(fout.read().strip())
        <vector memory>: N = 3 <7/9> <4/6> <1/3>
        """
        if required_z is True:
            warnings.warn(
                "The parameter 'required_z' is deprecated in v0.16.0 and will be "
                "removed in v0.20.0. Use parameter 'mincols' instead. E.g., "
                "``required_z=True`` is equivalent to ``mincols=3``.",
                category=FutureWarning,
                stacklevel=1,
            )
            mincols = 3

        kind = data_kind(data, required=required)
        _validate_data_input(
            data=data,
            x=x,
            y=y,
            z=z,
            required=required,
            mincols=mincols,
            kind=kind,
        )

        if check_kind:
            valid_kinds = ("file", "arg") if required is False else ("file",)
            if check_kind == "raster":
                valid_kinds += ("grid", "image")
            elif check_kind == "vector":
                valid_kinds += ("empty", "matrix", "vectors", "geojson")
            if kind not in valid_kinds:
                raise GMTTypeError(
                    type(data),
                    reason=f"Unrecognized data type for {check_kind!r} kind.",
                )

        # Decide which virtualfile_from_ function to use
        _virtualfile_from = {
            "arg": contextlib.nullcontext,
            "empty": self.virtualfile_from_vectors,
            "file": contextlib.nullcontext,
            "geojson": tempfile_from_geojson,
            "grid": self.virtualfile_from_grid,
            "image": tempfile_from_image,
            "stringio": self.virtualfile_from_stringio,
            "matrix": self.virtualfile_from_matrix,
            "vectors": self.virtualfile_from_vectors,
        }[kind]

        # "_data" is the data that will be passed to the _virtualfile_from function.
        # "_data" defaults to "data" but should be adjusted for some cases.
        _data = data
        match kind:
            case "image" if data.dtype != "uint8":
                msg = (
                    f"Input image has dtype: {data.dtype} which is unsupported, and "
                    "may result in an incorrect output. Please recast image to a uint8 "
                    "dtype and/or scale to 0-255 range, e.g. using a histogram "
                    "equalization function like skimage.exposure.equalize_hist."
                )
                warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
            case "empty":  # data is None, so data must be given via x/y/z.
                _data = [x, y]
                if z is not None:
                    _data.append(z)
                if extra_arrays:
                    msg = (
                        "The parameter 'extra_arrays' will be removed in v0.20.0. "
                        "Prepare and pass a dictionary of arrays instead to the `data` "
                        "parameter. E.g., `data={'x': x, 'y': y, 'size': size}`"
                    )
                    warnings.warn(message=msg, category=FutureWarning, stacklevel=1)
                    _data.extend(extra_arrays)
            case "vectors":
                if hasattr(data, "items") and not hasattr(data, "to_frame"):
                    # Dictionary, pandas.DataFrame or xarray.Dataset types.
                    # pandas.Series will be handled below like a 1-D numpy.ndarray.
                    _data = [array for _, array in data.items()]
                else:
                    # Python list, tuple, numpy.ndarray, and pandas.Series types
                    _data = np.atleast_2d(np.asanyarray(data).T)
            case "matrix" if data.dtype.kind not in "iuf":
                # GMT can only accept a 2-D matrix which are signed integer (i),
                # unsigned integer (u) or floating point (f) types. For other data
                # types, we need to use virtualfile_from_vectors instead, which turns
                # the matrix into a list of vectors and allows for better handling of
                # non-integer/float type inputs (e.g. for string or datetime data types)
                _virtualfile_from = self.virtualfile_from_vectors
                _data = data.T

        # Finally create the virtualfile from the data, to be passed into GMT
        file_context = _virtualfile_from(_data)
        return file_context

    @contextlib.contextmanager
    def virtualfile_out(
        self,
        kind: Literal["dataset", "grid", "image"] = "dataset",
        fname: str | None = None,
    ) -> Generator[str, None, None]:
        r"""
        Create a virtual file or an actual file for storing output data.

        If ``fname`` is not given, a virtual file will be created to store the output
        data into a GMT data container and the function yields the name of the virtual
        file. Otherwise, the output data will be written into the specified file and the
        function simply yields the actual file name.

        Parameters
        ----------
        kind
            The data kind of the virtual file to create. Valid values are ``"dataset"``,
            ``"grid"``, and ``"image"``. Ignored if ``fname`` is specified.
        fname
            The name of the actual file to write the output data. No virtual file will
            be created.

        Yields
        ------
        vfile
            Name of the virtual file or the actual file.

        Examples
        --------
        >>> from pathlib import Path
        >>> from pygmt.clib import Session
        >>> from pygmt.datatypes import _GMT_DATASET
        >>> from pygmt.helpers import GMTTempFile
        >>>
        >>> with GMTTempFile(suffix=".txt") as tmpfile:
        ...     with Path(tmpfile.name).open(mode="w") as fp:
        ...         print("1.0 2.0 3.0 TEXT", file=fp)
        ...
        ...     # Create a virtual file for storing the output table.
        ...     with Session() as lib:
        ...         with lib.virtualfile_out(kind="dataset") as vouttbl:
        ...             lib.call_module("read", [tmpfile.name, vouttbl, "-Td"])
        ...             ds = lib.read_virtualfile(vouttbl, kind="dataset")
        ...             assert isinstance(ds.contents, _GMT_DATASET)
        ...
        ...     # Write data to an actual file without creating a virtual file.
        ...     with Session() as lib:
        ...         with lib.virtualfile_out(fname=tmpfile.name) as vouttbl:
        ...             assert vouttbl == tmpfile.name
        ...             lib.call_module("read", [tmpfile.name, vouttbl, "-Td"])
        ...         line = Path(vouttbl).read_text()
        ...         assert line == "1\t2\t3\tTEXT\n"
        """
        if fname is not None:  # Yield the actual file name.
            yield fname
        else:  # Create a virtual file for storing the output data.
            # Determine the family and geometry from kind
            family, geometry = {
                "dataset": ("GMT_IS_DATASET", "GMT_IS_PLP"),
                "grid": ("GMT_IS_GRID", "GMT_IS_SURFACE"),
                "image": ("GMT_IS_IMAGE", "GMT_IS_SURFACE"),
            }[kind]
            direction = "GMT_OUT|GMT_IS_REFERENCE" if kind == "image" else "GMT_OUT"
            with self.open_virtualfile(family, geometry, direction, None) as vfile:
                yield vfile

    def inquire_virtualfile(self, vfname: str) -> int:
        """
        Get the family of a virtual file.

        Parameters
        ----------
        vfname
            Name of the virtual file to inquire.

        Returns
        -------
        family
            The integer value for the family of the virtual file.

        Examples
        --------
        >>> from pygmt.clib import Session
        >>> with Session() as lib:
        ...     with lib.virtualfile_out(kind="dataset") as vfile:
        ...         family = lib.inquire_virtualfile(vfile)
        ...         assert family == lib["GMT_IS_DATASET"]
        """
        c_inquire_virtualfile = self.get_libgmt_func(
            "GMT_Inquire_VirtualFile",
            argtypes=[ctp.c_void_p, ctp.c_char_p],
            restype=ctp.c_int,
        )
        return c_inquire_virtualfile(self.session_pointer, vfname.encode())

    def read_virtualfile(
        self,
        vfname: str,
        kind: Literal["dataset", "grid", "image", "cube", None] = None,
    ):
        """
        Read data from a virtual file and optionally cast into a GMT data container.

        Parameters
        ----------
        vfname
            Name of the virtual file to read.
        kind
            Cast the data into a GMT data container. Valid values are ``"dataset"``,
            ``"grid"``, ``"image"`` and ``None``. If ``None``, will return a ctypes void
            pointer.

        Returns
        -------
        pointer
            Pointer to the GMT data container. If ``kind`` is ``None``, returns a ctypes
            void pointer instead.

        Examples
        --------
        >>> from pathlib import Path
        >>> from pygmt.clib import Session
        >>> from pygmt.helpers import GMTTempFile
        >>>
        >>> # Read dataset from a virtual file
        >>> with Session() as lib:
        ...     with GMTTempFile(suffix=".txt") as tmpfile:
        ...         with Path(tmpfile.name).open(mode="w") as fp:
        ...             print("1.0 2.0 3.0 TEXT", file=fp)
        ...         with lib.virtualfile_out(kind="dataset") as vouttbl:
        ...             lib.call_module("read", [tmpfile.name, vouttbl, "-Td"])
        ...             # Read the virtual file as a void pointer
        ...             void_pointer = lib.read_virtualfile(vouttbl)
        ...             assert isinstance(void_pointer, int)  # void pointer is an int
        ...             # Read the virtual file as a dataset
        ...             data_pointer = lib.read_virtualfile(vouttbl, kind="dataset")
        ...             assert isinstance(data_pointer, ctp.POINTER(_GMT_DATASET))
        >>>
        >>> # Read grid from a virtual file
        >>> with Session() as lib:
        ...     with lib.virtualfile_out(kind="grid") as voutgrd:
        ...         lib.call_module("read", ["@earth_relief_01d_g", voutgrd, "-Tg"])
        ...         # Read the virtual file as a void pointer
        ...         void_pointer = lib.read_virtualfile(voutgrd)
        ...         assert isinstance(void_pointer, int)  # void pointer is an int
        ...         data_pointer = lib.read_virtualfile(voutgrd, kind="grid")
        ...         assert isinstance(data_pointer, ctp.POINTER(_GMT_GRID))

        """
        c_read_virtualfile = self.get_libgmt_func(
            "GMT_Read_VirtualFile",
            argtypes=[ctp.c_void_p, ctp.c_char_p],
            restype=ctp.c_void_p,
        )
        pointer = c_read_virtualfile(self.session_pointer, vfname.encode())
        # The GMT C API function GMT_Read_VirtualFile returns a void pointer. It usually
        # needs to be cast into a pointer to a GMT data container (e.g., _GMT_GRID or
        # _GMT_DATASET).
        if kind is None:  # Return the ctypes void pointer
            return pointer
        if kind == "cube":
            msg = f"kind={kind} is not supported yet."
            raise NotImplementedError(msg)
        dtype = {"dataset": _GMT_DATASET, "grid": _GMT_GRID, "image": _GMT_IMAGE}[kind]
        return ctp.cast(pointer, ctp.POINTER(dtype))

    def virtualfile_to_dataset(
        self,
        vfname: str,
        output_type: Literal["pandas", "numpy", "file", "strings"] = "pandas",
        header: int | None = None,
        column_names: list[str] | None = None,
        dtype: type | dict[str, type] | None = None,
        index_col: str | int | None = None,
    ) -> pd.DataFrame | np.ndarray | None:
        """
        Output a tabular dataset stored in a virtual file to a different format.

        The format of the dataset is determined by the ``output_type`` parameter.

        Parameters
        ----------
        vfname
            The virtual file name that stores the result data.
        output_type
            Desired output type of the result data.

            - ``"pandas"`` will return a :class:`pandas.DataFrame` object.
            - ``"numpy"`` will return a :class:`numpy.ndarray` object.
            - ``"file"`` means the result was saved to a file and will return ``None``.
            - ``"strings"`` will return the trailing text only as an array of strings.
        header
            Row number containing column names for the :class:`pandas.DataFrame` output.
            ``header=None`` means not to parse the column names from table header.
            Ignored if the row number is larger than the number of headers in the table.
        column_names
            The column names for the :class:`pandas.DataFrame` output.
        dtype
            Data type for the columns of the :class:`pandas.DataFrame` output. Can be a
            single type for all columns or a dictionary mapping column names to types.
        index_col
            Column to set as the index of the :class:`pandas.DataFrame` output.

        Returns
        -------
        result
            The result dataset. If ``output_type="file"`` returns ``None``.

        Examples
        --------
        >>> from pathlib import Path
        >>> import numpy as np
        >>> import pandas as pd
        >>>
        >>> from pygmt.helpers import GMTTempFile
        >>> from pygmt.clib import Session
        >>>
        >>> with GMTTempFile(suffix=".txt") as tmpfile:
        ...     # prepare the sample data file
        ...     with Path(tmpfile.name).open(mode="w") as fp:
        ...         print(">", file=fp)
        ...         print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
        ...         print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)
        ...         print(">", file=fp)
        ...         print("7.0 8.0 9.0 TEXT8 TEXT90", file=fp)
        ...         print("10.0 11.0 12.0 TEXT123 TEXT456789", file=fp)
        ...
        ...     # file output
        ...     with Session() as lib:
        ...         with GMTTempFile(suffix=".txt") as outtmp:
        ...             with lib.virtualfile_out(
        ...                 kind="dataset", fname=outtmp.name
        ...             ) as vouttbl:
        ...                 lib.call_module("read", [tmpfile.name, vouttbl, "-Td"])
        ...                 result = lib.virtualfile_to_dataset(
        ...                     vfname=vouttbl, output_type="file"
        ...                 )
        ...                 assert result is None
        ...                 assert Path(outtmp.name).stat().st_size > 0
        ...
        ...     # strings, numpy and pandas outputs
        ...     with Session() as lib:
        ...         with lib.virtualfile_out(kind="dataset") as vouttbl:
        ...             lib.call_module("read", [tmpfile.name, vouttbl, "-Td"])
        ...
        ...             # strings output
        ...             outstr = lib.virtualfile_to_dataset(
        ...                 vfname=vouttbl, output_type="strings"
        ...             )
        ...             assert isinstance(outstr, np.ndarray)
        ...             assert outstr.dtype.kind in ("S", "U")
        ...
        ...             # numpy output
        ...             outnp = lib.virtualfile_to_dataset(
        ...                 vfname=vouttbl, output_type="numpy"
        ...             )
        ...             assert isinstance(outnp, np.ndarray)
        ...
        ...             # pandas output
        ...             outpd = lib.virtualfile_to_dataset(
        ...                 vfname=vouttbl, output_type="pandas"
        ...             )
        ...             assert isinstance(outpd, pd.DataFrame)
        ...
        ...             # pandas output with specified column names
        ...             outpd2 = lib.virtualfile_to_dataset(
        ...                 vfname=vouttbl,
        ...                 output_type="pandas",
        ...                 column_names=["col1", "col2", "col3", "coltext"],
        ...             )
        ...             assert isinstance(outpd2, pd.DataFrame)
        >>> outstr
        array(['TEXT1 TEXT23', 'TEXT4 TEXT567', 'TEXT8 TEXT90',
           'TEXT123 TEXT456789'], dtype='<U18')
        >>> outnp
        array([[1.0, 2.0, 3.0, 'TEXT1 TEXT23'],
               [4.0, 5.0, 6.0, 'TEXT4 TEXT567'],
               [7.0, 8.0, 9.0, 'TEXT8 TEXT90'],
               [10.0, 11.0, 12.0, 'TEXT123 TEXT456789']], dtype=object)
        >>> outpd
              0     1     2                   3
        0   1.0   2.0   3.0        TEXT1 TEXT23
        1   4.0   5.0   6.0       TEXT4 TEXT567
        2   7.0   8.0   9.0        TEXT8 TEXT90
        3  10.0  11.0  12.0  TEXT123 TEXT456789
        >>> outpd2
           col1  col2  col3             coltext
        0   1.0   2.0   3.0        TEXT1 TEXT23
        1   4.0   5.0   6.0       TEXT4 TEXT567
        2   7.0   8.0   9.0        TEXT8 TEXT90
        3  10.0  11.0  12.0  TEXT123 TEXT456789
        """
        if output_type == "file":  # Already written to file, so return None
            return None

        # Read the virtual file as a _GMT_DATASET object
        result = self.read_virtualfile(vfname, kind="dataset").contents

        if output_type == "strings":  # strings output
            return result.to_strings()

        result = result.to_pandas(
            header=header, column_names=column_names, dtype=dtype, index_col=index_col
        )
        if output_type == "numpy":  # numpy.ndarray output
            return result.to_numpy()
        return result  # pandas.DataFrame output

    def virtualfile_to_raster(
        self,
        vfname: str,
        kind: Literal["grid", "image", "cube", None] = "grid",
        outgrid: str | None = None,
    ) -> xr.DataArray | None:
        """
        Output raster data stored in a virtual file to an :class:`xarray.DataArray`
        object.

        The raster data can be a grid, an image or a cube.

        Parameters
        ----------
        vfname
            The virtual file name that stores the result grid/image/cube.
        kind
            Type of the raster data. Valid values are ``"grid"``, ``"image"``,
            ``"cube"`` or ``None``. If ``None``, will inquire the data type from the
            virtual file name.
        outgrid
            Name of the output grid/image/cube. If specified, it means the raster data
            was already saved into an actual file and will return ``None``.

        Returns
        -------
        result
            The result grid/image/cube. If ``outgrid`` is specified, return ``None``.

        Examples
        --------
        >>> from pathlib import Path
        >>> from pygmt.clib import Session
        >>> from pygmt.helpers import GMTTempFile
        >>> with Session() as lib:
        ...     # file output
        ...     with GMTTempFile(suffix=".nc") as tmpfile:
        ...         outgrid = tmpfile.name
        ...         with lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd:
        ...             lib.call_module("read", ["@earth_relief_01d_g", voutgrd, "-Tg"])
        ...             result = lib.virtualfile_to_raster(
        ...                 vfname=voutgrd, outgrid=outgrid
        ...             )
        ...             assert result == None
        ...             assert Path(outgrid).stat().st_size > 0
        ...
        ...     # xarray.DataArray output
        ...     outgrid = None
        ...     with lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd:
        ...         lib.call_module("read", ["@earth_relief_01d_g", voutgrd, "-Tg"])
        ...         result = lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
        ...         assert isinstance(result, xr.DataArray)
        """
        if outgrid is not None:  # Already written to file, so return None
            return None
        if kind is None:  # Inquire the data family from the virtualfile
            family = self.inquire_virtualfile(vfname)
            kind = {  # type: ignore[assignment]
                self["GMT_IS_GRID"]: "grid",
                self["GMT_IS_IMAGE"]: "image",
                self["GMT_IS_CUBE"]: "cube",
            }[family]
        return self.read_virtualfile(vfname, kind=kind).contents.to_xarray()

    def extract_region(self) -> np.ndarray:
        """
        Extract the region of the currently active figure.

        Retrieves the information from the PostScript file, so it works for country
        codes as well.

        Returns
        -------
        region
            A numpy 1-D array with the west, east, south, and north dimensions of the
            current figure.

        Examples
        --------
        >>> import pygmt
        >>> fig = pygmt.Figure()
        >>> fig.coast(
        ...     region=[0, 10, -20, -10], projection="M12c", frame=True, land="black"
        ... )
        >>> with Session() as lib:
        ...     region = lib.extract_region()
        >>> print(", ".join([f"{x:.2f}" for x in region]))
        0.00, 10.00, -20.00, -10.00

        Using ISO country codes for the regions (for example ``"US.HI"`` for Hawaiʻi):

        >>> fig = pygmt.Figure()
        >>> fig.coast(region="US.HI", projection="M12c", frame=True, land="black")
        >>> with Session() as lib:
        ...     region = lib.extract_region()
        >>> print(", ".join([f"{x:.2f}" for x in region]))
        -164.71, -154.81, 18.91, 23.58

        The country codes can have an extra argument that rounds the region to multiples
        of the argument (for example, ``"US.HI+r5"`` will round the region to multiples
        of 5):

        >>> fig = pygmt.Figure()
        >>> fig.coast(region="US.HI+r5", projection="M12c", frame=True, land="black")
        >>> with Session() as lib:
        ...     region = lib.extract_region()
        >>> print(", ".join([f"{x:.2f}" for x in region]))
        -165.00, -150.00, 15.00, 25.00
        """  # noqa: RUF002
        c_extract_region = self.get_libgmt_func(
            "GMT_Extract_Region",
            argtypes=[ctp.c_void_p, ctp.c_char_p, ctp.POINTER(ctp.c_double)],
            restype=ctp.c_int,
        )

        region = np.empty(4, dtype=np.float64)
        status = c_extract_region(
            self.session_pointer,
            None,  # File pointer to a PostScript file. Must be None in modern mode.
            region.ctypes.data_as(ctp.POINTER(ctp.c_double)),
        )
        if status != 0:
            msg = "Failed to extract region from current figure."
            raise GMTCLibError(msg)
        return region
