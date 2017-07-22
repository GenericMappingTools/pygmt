"""
Session management modules: begin, end, figure, etc
"""
import os
from tempfile import NamedTemporaryFile

from .clib import call_module, GMTSession


def begin():
    """
    Initiate a new GMT modern mode session.

    Used in combination with :func:`gmt.end`.

    Only meant to be used once for creating the global session.

    """
    prefix = 'gmt-python-session'
    with GMTSession() as session:
        call_module(session, 'begin', prefix)


def end():
    """
    Terminate GMT modern mode session and optionally produce the figure files.

    Called after :func:`gmt.begin` and all commands that you want included in a
    session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``gmt.begin``), and bring the figures to the working directory.

    """
    with GMTSession() as session:
        call_module(session, 'end', '')


def figure():
    """
    Start a new figure.

    All plotting commands run afterward will append to this figure.

    Unlike the command-line version (``gmt figure``), this function does not
    trigger the generation of a figure file. An explicit call to
    :func:`gmt.savefig` or :func:`gmt.psconvert` must be made in order to get a
    file.

    """
    # Need a unique name prefix for each figure, otherwise GMT will plot
    # everything on the same figure.
    tmpfile = NamedTemporaryFile(prefix='gmt-python-', dir=os.path.curdir,
                                 delete=True)
    prefix = tmpfile.name
    tmpfile.close()
    # Passing format '-' tells gmt.end to not produce any files.
    fmt = '-'
    with GMTSession() as session:
        call_module(session, 'figure', '{} {}'.format(prefix, fmt))
