"""
Modern mode session management modules.
"""

import os
import sys

from pygmt.clib import Session
from pygmt.helpers import unique_name


def begin():
    """
    Initiate a new GMT modern mode session.

    Used in combination with :func:`pygmt.end`.

    Only meant to be used once for creating the global session.
    """
    # On Windows, need to set GMT_SESSION_NAME to a unique value
    if sys.platform == "win32":
        os.environ["GMT_SESSION_NAME"] = unique_name()

    prefix = "pygmt-session"
    with Session() as lib:
        lib.call_module(module="begin", args=[prefix])
        # pygmt relies on GMT modern mode with GMT_COMPATIBILITY at version 6
        lib.call_module(module="set", args=["GMT_COMPATIBILITY=6"])


def end():
    """
    Terminate GMT modern mode session and optionally produce the figure files.

    Called after :func:`pygmt.begin` and all commands that you want included in
    a session. Will finalize any PostScript plots that were made in the
    background, convert them to the desired format (specified in
    ``pygmt.begin``), and bring the figures to the working directory.
    """
    with Session() as lib:
        lib.call_module(module="end", args=[])
