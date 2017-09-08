"""
Defines the LibGMT context manager that is the main interface with libgmt.
"""
from .core import load_libgmt, create_session, destroy_session, call_module, \
    get_constant


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

    def __init__(self):
        self._libgmt = load_libgmt()
        self._session_id = None
        self._session_name = 'gmt-python-session'

    def __enter__(self):
        """
        Start the GMT session and keep the session argument.
        """
        self._session_id = create_session(self._session_name, self._libgmt)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Destroy the session when exiting the context.
        """
        destroy_session(self._session_id, self._libgmt)
        self._session_id = None

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
        value = get_constant(name, self._libgmt)
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
        call_module(self._session_id, module, args, self._libgmt)
