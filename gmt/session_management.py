"""
Session management modules: begin, end, figure, clean
"""
from . import clib


def begin():
    """
    Initiate a new GMT modern mode session.

    Used in combination with :func:`gmt.end`.

    Only meant to be used once for creating the global session.

    """
    prefix = 'gmt-python-session'
    clib.call_module('begin', prefix)


def end():
    """
    Terminate GMT modern mode session and optionally produce the figure files.

    Called after :func:`gmt.begin` and all commands that you want included in a
    session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``gmt.begin``), and bring the figures to the working directory.

    """
    clib.call_module('end', '')


def figure():
    """
    Start a new figure.

    All plotting commands run afterward will append to this figure.

    Unlike the command-line version (``gmt figure``), this function does not
    trigger the generation of a figure file. An explicit call to
    :func:`gmt.savefig` or :func:`gmt.psconvert` must be made in order to get a
    file.

    """
    prefix = 'gmt-python-figure'
    # Passing format '-' tells gmt.end to not produce any files.
    fmt = '-'
    clib.call_module('figure', '{} {}'.format(prefix, fmt))


class GMTSession():
    """
    Placeholder for an active modern mode session.

    Calls ``begin`` and ``figure`` when created. Calls ``end`` when destroyed
    so that the temporary files are cleaned.

    The call to ``figure`` is necessary because the default behavior in Python
    is to not generate figure files unless explicitly commanded by
    ``psconvert`` or ``savefig``. The call starts a new figure with the format
    ``-`` which indicates that ``end`` should skip processing that figure.

    """

    def __init__(self):
        self.is_active = False
        self.begin()

    def begin(self):
        """
        Starts a modern mode session by calling ``begin`` and ``figure``.

        Sets the attribute ``_is_active`` to ``True`` to indicate that there
        is an active session.
        """
        assert not self.is_active, \
            "Session is already active. Can't start two simultaneous sessions"
        begin()
        figure()
        self.is_active = True

    def end(self):
        """
        End the current session.
        """
        assert self.is_active, "Can't end an inactive session."
        end()
        self.is_active = False

    def restart(self):
        """
        End the current session (if it's active) and start a new one.
        """
        if self.is_active:
            self.end()
        self.begin()

    def __del__(self):
        """
        When the session is being garbage collected, call ``end`` to clean up
        the session.
        """
        self.end()
