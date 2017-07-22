"""
ctypes wrappers for core functions from the C API
"""
import sys
import ctypes

from . import constants


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
        raise RuntimeError('Unknown operating system: {}'.format(sys.platform))
    libgmt = ctypes.CDLL('.'.join(['libgmt', lib_ext]))
    assert hasattr(libgmt, 'GMT_Create_Session'), \
        "Error loading libgmt. Can't access GMT_Create_Session."
    return libgmt


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
        :func:`gmt.clib.GMTSession`.
    module : str
        Module name (``'pscoast'``, ``'psbasemap'``, etc).
    args : str
        String with the command line arguments that will be passed to the
        module (for example, ``'-R0/5/0/10 -JM'``).

    """
    mode = constants.GMT_MODULE_CMD
    libgmt = load_libgmt()
    c_call_module = libgmt.GMT_Call_Module
    c_call_module.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int,
                              ctypes.c_void_p]
    c_call_module.restype = ctypes.c_int
    status = c_call_module(session, module.encode(), mode, args.encode())
    assert status is not None, 'Failed returning None.'
    assert status == 0, 'Failed with status code {}.'.format(status)


def create_session():
    """
    Create the ``GMTAPI_CTRL`` struct required by the GMT C API functions.

    .. warning::

        Best not used directly. Use :class:`gmt.clib.GMTSession` instead.

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
    session = c_create_session(constants.GMT_SESSION_NAME,
                               constants.GMT_PAD_DEFAULT,
                               constants.GMT_SESSION_EXTERNAL,
                               None)
    assert session is not None, \
        "Failed creating GMT API pointer using create_session."
    return session


def destroy_session(session):
    """
    Terminate and free the memory of a registered ``GMTAPI_CTRL`` session.

    .. warning::

        Best not used directly. Use :class:`gmt.clib.GMTSession` instead.

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
    assert status is not None, 'Failed returning None.'
    assert status == 0, 'Failed with status code {}.'.format(status)


class GMTSession():  # pylint: disable=too-few-public-methods
    """
    Context manager to create a GMT C API session and destroy it.

    Needs to be used when wrapping a GMT module into a function.

    If creating GMT data structures to communicate data, put that code inside
    this context manager and reuse the same session.

    Examples
    --------

    >>> with GMTSession() as session:
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
