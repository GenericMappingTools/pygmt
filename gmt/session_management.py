"""
Modern mode session management modules.
"""
from .clib import call_module, APISession


def begin():
    """
    Initiate a new GMT modern mode session.

    Used in combination with :func:`gmt.end`.

    Only meant to be used once for creating the global session.

    """
    prefix = 'gmt-python-session'
    with APISession() as session:
        call_module(session, 'begin', prefix)


def end():
    """
    Terminate GMT modern mode session and optionally produce the figure files.

    Called after :func:`gmt.begin` and all commands that you want included in a
    session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``gmt.begin``), and bring the figures to the working directory.

    """
    with APISession() as session:
        call_module(session, 'end', '')
