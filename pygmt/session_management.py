"""
Modern mode session management modules.
"""
from pygmt.clib import Session


def begin():
    """
    Initiate a new GMT modern mode session.

    Used in combination with :func:`pygmt.end`.

    Only meant to be used once for creating the global session.
    """
    prefix = "pygmt-session"
    with Session() as lib:
        lib.call_module("begin", prefix)
        # pygmt relies on GMT modern mode with GMT_COMPATIBILITY at version 6
        lib.call_module("set", "GMT_COMPATIBILITY 6")


def end():
    """
    Terminate GMT modern mode session and optionally produce the figure files.

    Called after :func:`pygmt.begin` and all commands that you want included in
    a session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``pygmt.begin``), and bring the figures to the working directory.
    """
    with Session() as lib:
        lib.call_module("end", "")
