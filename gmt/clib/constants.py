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

# Modes for GMT_Call_Module
# As GMT_MODULE_PURPOSE, but only lists the modules.
GMT_MODULE_LIST = -4
# Return GMT_NOERROR (0) if module exists, GMT_NOT_A_VALID_MODULE otherwise.
GMT_MODULE_EXIST = -3
# As GMT_MODULE_EXIST, but also print the module purpose.
GMT_MODULE_PURPOSE = -2
# Args is a linked list of option structures.
GMT_MODULE_OPT = -1
# Args is a single text string with multiple options
GMT_MODULE_CMD = 0
