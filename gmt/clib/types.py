# pylint: disable=too-few-public-methods
"""
Wrappers for GMT data structures.

Useful if you need to access the internal values of a GMT data structure or
pass it along as something other than a void pointer.
"""
import ctypes


class LUT(ctypes.Structure):
    """
    Wrapper for GMT_LUT (look up table).
    Required for Palette.
    """

    __fields_ = [
        ('z_low', ctypes.c_double),
        ('z_high', ctypes.c_double),
        ('i_dz', ctypes.c_double),
        ('rgb_low', ctypes.c_double*4),
        ('rgb_high', ctypes.c_double*4),
        ('rgb_diff', ctypes.c_double*4),
        ('hsv_low', ctypes.c_double*4),
        ('hsv_high', ctypes.c_double*4),
        ('hsv_diff', ctypes.c_double*4),
        ('annot', ctypes.c_uint),  # 1 for Lower, 2 for Upper, 3 for Both
        ('skip', ctypes.c_uint),  # true means skip this slice
        # Used as void pointer so we don't have to wrap GMT_FILL as well
        ('fill', ctypes.c_void_p),  # For patterns instead of color
        ('label', ctypes.c_char_p),  # For non-number labels
    ]


class BFN(ctypes.Structure):
    """
    Wrapper for GMT_BFN (back-, fore-, and nan-colors).
    Required for Palette.
    """

    _fields_ = [
        ('rgb', ctypes.c_double*4),  # Red, green, blue, and alpha
        ('hsv', ctypes.c_double*4),  # Hue, saturation, value, alpha
        ('skip', ctypes.c_uint),  # true means skip this slice
        # Used as void pointer so we don't have to wrap GMT_FILL as well
        ('fill', ctypes.c_void_p),  # For patterns instead of color
    ]


class Palette(ctypes.Structure):
    """
    Wrapper for GMT_PALETTE (stores a color palette table, or CPT).
    Holds all pen, color, and fill-related parameters.
    """

    _fields_ = [
        # CPT lookup table read by gmtlib_read_cpt
        ('data', ctypes.POINTER(LUT)),
        # Structures with back/fore/nan colors
        ('bfn', BFN*3),
        # Number of CPT header records (0 if no header)
        ('n_headers', ctypes.c_uint),
        # Number of colors in CPT lookup table
        ('n_colors', ctypes.c_uint),
        # Flags controlling use of BFN colors
        ('mode', ctypes.c_uint),
        # RGB, HSV, CMYK
        ('model', ctypes.c_uint),
        # If 1 then we must wrap around to find color - can never be F or B
        ('is_wrapping', ctypes.c_uint),
        # true if only grayshades are needed
        ('is_gray', ctypes.c_uint),
        # true if only black and white are needed
        ('is_bw', ctypes.c_uint),
        # true if continuous color tables have been given
        ('is_continuous', ctypes.c_uint),
        # true if CPT contains any patterns
        ('has_pattern', ctypes.c_uint),
        # true if CPT is hinged at hinge (below)
        ('has_hinge', ctypes.c_uint),
        # true if CPT has a natural range (minmax below)
        ('has_range', ctypes.c_uint),
        # true if CPT applies to categorical data
        ('categorical', ctypes.c_uint),
        # Min/max z-value for a default range, if given
        ('minmax', ctypes.c_double*2),
        # z-value for hinged CPTs
        ('hinge', ctypes.c_double),
        # z-length of active CPT
        ('wrap_length', ctypes.c_double),
        # Array with all CPT header records, if any)
        ('header', ctypes.POINTER(ctypes.c_char_p)),
        # Book-keeping variables "hidden" from the API
        ('hidden', ctypes.c_void_p),
    ]
