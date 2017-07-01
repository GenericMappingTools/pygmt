"""
Define some constants that are used throughout the project.

Some are copied from the GMT source code because they aren't accessible through
the C API.
"""


GMT_SESSION_NAME = b'gmt-python'
# Default grid padding (taken from gmt_constants.h) used by create_session
GMT_PAD_DEFAULT = 2
# Session type (external API) used as 'mode' argument by create_session
GMT_SESSION_EXTERNAL = 2
