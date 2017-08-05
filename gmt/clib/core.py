"""
ctypes wrappers for core functions from the C API
"""
import sys
import ctypes

from ..exceptions import GMTOSError, GMTCLibNotFoundError, GMTCLibError


def load_libgmt():
    """
    Find and load ``libgmt`` as a ctypes.CDLL.

    Currently only works for Linux (looks for ``libgmt.so``).

    Library path must be discoverable, either by being in standard places or by
    setting the environment variable ``LD_LIBRARY_PATH``.

    Returns
    -------
    ctypes.CDLL object
        The loaded shared library.

    """
    # Set the shared library extension in a platform independent way
    if sys.platform.startswith('linux'):
        lib_ext = 'so'
    elif sys.platform == 'darwin':
        # Darwin is OSX
        lib_ext = 'dylib'
    else:
        raise GMTOSError('Unknown operating system: {}'.format(sys.platform))

    lib_name = '.'.join(['libgmt', lib_ext])

    try:
        libgmt = ctypes.CDLL(lib_name)
    except OSError as err:
        msg = ' '.join([
            "Couldn't find the GMT shared library '{}'.".format(lib_name),
            "Have you tried setting the LD_LIBRARY_PATH environment variable?",
        ])
        raise GMTCLibNotFoundError(msg) from err

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
    return libgmt


def get_constant(name):
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
    ValueError
        If the constant doesn't exist.

    """
    libgmt = load_libgmt()
    c_get_enum = libgmt.GMT_Get_Enum
    c_get_enum.argtypes = [ctypes.c_char_p]
    c_get_enum.restype = ctypes.c_int

    value = c_get_enum(name.encode())

    assert value is not None, 'GMT_Get_Enum failed returning None.'
    if value == -99999:
        raise GMTCLibError(
            "Constant '{}' doesn't exits in libgmt.".format(name))

    return value


def call_module(session, module, args):
    """
    Call a GMT module with the given arguments.

    Makes a call to ``GMT_Call_Module`` from the C API using mode
    ``GMT_MODULE_CMD`` (arguments passed as a single string).

    Most interactions with the C API are done through this function.

    Parameters
    ----------
    session : ctypes.c_void_p
        A ctypes void pointer to a GMT session created by
        :func:`gmt.clib.APISession`.
    module : str
        Module name (``'pscoast'``, ``'psbasemap'``, etc).
    args : str
        String with the command line arguments that will be passed to the
        module (for example, ``'-R0/5/0/10 -JM'``).

    """
    libgmt = load_libgmt()
    c_call_module = libgmt.GMT_Call_Module
    c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_void_p]
    c_call_module.restype = ctypes.c_int

    mode = get_constant('GMT_MODULE_CMD')
    status = c_call_module(session, module.encode(), mode, args.encode())

    if status is None or status != 0:
        raise GMTCLibError(
            'Failed GMT_Call_Module with status code {}.'.format(status))


def create_session(name='gmt-python-session'):
    """
    Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

    .. warning::

        Best not used directly. Use :class:`gmt.clib.APISession` instead.

    It is a C void pointer containing the current session information and
    cannot be accessed directly.

    Remember to terminate the current session using
    :func:`gmt.clib.destroy_session` before creating a new one.

    Returns
    -------
    api_pointer : C void pointer (returned by ctypes as an integer)
        Used by GMT C API functions.

    """
    libgmt = load_libgmt()
    c_create_session = libgmt.GMT_Create_Session
    c_create_session.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint,
                                 ctypes.c_void_p]
    c_create_session.restype = ctypes.c_void_p
    # None is passed in place of the print function pointer. It becomes the
    # NULL pointer when passed to C, prompting the C API to use the default
    # print function.
    session = c_create_session(name.encode(),
                               get_constant('GMT_PAD_DEFAULT'),
                               get_constant('GMT_SESSION_EXTERNAL'),
                               None)

    if session is None:
        raise GMTCLibError("Failed to create a GMT API void pointer.")

    return session


def destroy_session(session):
    """
    Terminate and free the memory of a registered ``GMTAPI_CTRL`` session.

    .. warning::

        Best not used directly. Use :class:`gmt.clib.APISession` instead.

    The session is created and consumed by the C API modules and needs to be
    freed before creating a new. Otherwise, some of the configuration files
    might be left behind and can influence subsequent API calls.

    Parameters
    ----------
    session : C void pointer (returned by ctypes as an integer)
        The active session object produced by :func:`gmt.clib.create_session`.

    """
    libgmt = load_libgmt()
    c_destroy_session = libgmt.GMT_Destroy_Session
    c_destroy_session.argtypes = [ctypes.c_void_p]
    c_destroy_session.restype = ctypes.c_int
    status = c_destroy_session(session)
    if status is None or status != 0:
        raise GMTCLibError(
            'Failed GMT_Destroy_Session with status code {}.'.format(status))


class APISession():  # pylint: disable=too-few-public-methods
    """
    Context manager to create a GMT C API session and destroy it.

    Needs to be used when wrapping a GMT module into a function.

    If creating GMT data structures to communicate data, put that code inside
    this context manager and reuse the same session.

    Examples
    --------

    >>> with APISession() as session:
    ...     call_module(session, 'figure', 'my-figure')

    """

    def __init__(self):
        self.session_id = None

    def __enter__(self):
        """
        Start the GMT session and keep the session argument.
        """
        self.session_id = create_session()
        return self.session_id

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the session when exiting the context.
        """
        destroy_session(self.session_id)
        self.session_id = None
