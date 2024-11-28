"""
config - set GMT defaults globally or locally.
"""

from inspect import Parameter, Signature
from typing import ClassVar

from pygmt.clib import Session


class config:  # noqa: N801
    """
    Set GMT defaults globally or locally.

    Change GMT defaults globally::

        pygmt.config(PARAMETER=value)

    Change GMT defaults locally by using it as a context manager::

        with pygmt.config(PARAMETER=value):
            ...

    Full GMT defaults list at :gmt-docs:`gmt.conf.html`
    """

    # Manually set the __signature__ attribute to enable tab autocompletion
    _keywords: ClassVar = [
        "COLOR_BACKGROUND",
        "COLOR_FOREGROUND",
        "COLOR_CPT",
        "COLOR_NAN",
        "COLOR_MODEL",
        "COLOR_HSV_MIN_S",
        "COLOR_HSV_MAX_S",
        "COLOR_HSV_MIN_V",
        "COLOR_HSV_MAX_V",
        "COLOR_SET",
        "DIR_CACHE",
        "DIR_DATA",
        "DIR_DCW",
        "DIR_GSHHG",
        "FONT_ANNOT_PRIMARY",
        "FONT_ANNOT_SECONDARY",
        "FONT_HEADING",
        "FONT_LABEL",
        "FONT_LOGO",
        "FONT_SUBTITLE",
        "FONT_TAG",
        "FONT_TITLE",
        "FORMAT_CLOCK_IN",
        "FORMAT_CLOCK_OUT",
        "FORMAT_CLOCK_MAP",
        "FORMAT_DATE_IN",
        "FORMAT_DATE_OUT",
        "FORMAT_DATE_MAP",
        "FORMAT_GEO_OUT",
        "FORMAT_GEO_MAP",
        "FORMAT_FLOAT_OUT",
        "FORMAT_FLOAT_MAP",
        "FORMAT_TIME_PRIMARY_MAP",
        "FORMAT_TIME_SECONDARY_MAP",
        "FORMAT_TIME_STAMP",
        "GMT_DATA_SERVER",
        "GMT_DATA_SERVER_LIMIT",
        "GMT_DATA_UPDATE_INTERVAL",
        "GMT_COMPATIBILITY",
        "GMT_CUSTOM_LIBS",
        "GMT_EXPORT_TYPE",
        "GMT_EXTRAPOLATE_VAL",
        "GMT_FFT",
        "GMT_GRAPHICS_DPU",
        "GMT_GRAPHICS_FORMAT",
        "GMT_HISTORY",
        "GMT_INTERPOLANT",
        "GMT_LANGUAGE",
        "GMT_MAX_CORES",
        "GMT_THEME",
        "GMT_TRIANGULATE",
        "GMT_VERBOSE",
        "IO_COL_SEPARATOR",
        "IO_FIRST_HEADER",
        "IO_GRIDFILE_FORMAT",
        "IO_GRIDFILE_SHORTHAND",
        "IO_HEADER",
        "IO_HEADER_MARKER",
        "IO_N_HEADER_RECS",
        "IO_NAN_RECORDS",
        "IO_NC4_CHUNK_SIZE",
        "IO_NC4_DEFLATION_LEVEL",
        "IO_LONLAT_TOGGLE",
        "IO_SEGMENT_BINARY",
        "IO_SEGMENT_MARKER",
        "MAP_ANNOT_MIN_ANGLE",
        "MAP_ANNOT_MIN_SPACING",
        "MAP_ANNOT_OBLIQUE",
        "MAP_ANNOT_OFFSET_PRIMARY",
        "MAP_ANNOT_OFFSET_SECONDARY",
        "MAP_ANNOT_ORTHO",
        "MAP_DEFAULT_PEN",
        "MAP_DEGREE_SYMBOL",
        "MAP_EMBELLISHMENT_MODE",
        "MAP_FRAME_AXES",
        "MAP_FRAME_PEN",
        "MAP_FRAME_PERCENT",
        "MAP_FRAME_TYPE",
        "MAP_FRAME_WIDTH",
        "MAP_GRID_CROSS_SIZE_PRIMARY",
        "MAP_GRID_CROSS_SIZE_SECONDARY",
        "MAP_GRID_PEN_PRIMARY",
        "MAP_GRID_PEN_SECONDARY",
        "MAP_HEADING_OFFSET",
        "MAP_LABEL_MODE",
        "MAP_LABEL_OFFSET",
        "MAP_LINE_STEP",
        "MAP_LOGO",
        "MAP_LOGO_POS",
        "MAP_ORIGIN_X",
        "MAP_ORIGIN_Y",
        "MAP_POLAR_CAP",
        "MAP_SCALE_HEIGHT",
        "MAP_TICK_LENGTH_PRIMARY",
        "MAP_TICK_LENGTH_SECONDARY",
        "MAP_TICK_PEN_PRIMARY",
        "MAP_TICK_PEN_SECONDARY",
        "MAP_TITLE_OFFSET",
        "MAP_VECTOR_SHAPE",
        "PROJ_AUX_LATITUDE",
        "PROJ_DATUM",
        "PROJ_ELLIPSOID",
        "PROJ_GEODESIC",
        "PROJ_LENGTH_UNIT",
        "PROJ_MEAN_RADIUS",
        "PROJ_SCALE_FACTOR",
        "PS_CHAR_ENCODING",
        "PS_COLOR_MODEL",
        "PS_COMMENTS",
        "PS_CONVERT",
        "PS_IMAGE_COMPRESS",
        "PS_LINE_CAP",
        "PS_LINE_JOIN",
        "PS_MITER_LIMIT",
        "PS_MEDIA",
        "PS_PAGE_COLOR",
        "PS_PAGE_ORIENTATION",
        "PS_SCALE_X",
        "PS_SCALE_Y",
        "PS_TRANSPARENCY",
        "TIME_EPOCH",
        "TIME_IS_INTERVAL",
        "TIME_INTERVAL_FRACTION",
        "TIME_LEAP_SECONDS",
        "TIME_REPORT",
        "TIME_UNIT",
        "TIME_WEEK_START",
        "TIME_Y2K_OFFSET_YEAR",
    ]

    _special_keywords: ClassVar = {
        "FONT": [
            "FONT_ANNOT_PRIMARY",
            "FONT_ANNOT_SECONDARY",
            "FONT_HEADING",
            "FONT_LABEL",
            "FONT_TAG",
            "FONT_TITLE",
        ],
        "FONT_ANNOT": ["FONT_ANNOT_PRIMARY", "FONT_ANNOT_SECONDARY"],
        "FORMAT_TIME_MAP": ["FORMAT_TIME_PRIMARY_MAP", "FORMAT_TIME_SECONDARY_MAP"],
        "MAP_ANNOT_OFFSET": [
            "MAP_ANNOT_OFFSET_PRIMARY",
            "MAP_ANNOT_OFFSET_SECONDARY",
        ],
        "MAP_GRID_CROSS_SIZE": [
            "MAP_GRID_CROSS_SIZE_PRIMARY",
            "MAP_GRID_CROSS_SIZE_SECONDARY",
        ],
        "MAP_GRID_PEN": ["MAP_GRID_PEN_PRIMARY", "MAP_GRID_PEN_SECONDARY"],
        "MAP_TICK_LENGTH": ["MAP_TICK_LENGTH_PRIMARY", "MAP_TICK_LENGTH_SECONDARY"],
        "MAP_TICK_PEN": ["MAP_TICK_PEN_PRIMARY", "MAP_TICK_PEN_SECONDARY"],
    }

    __signature__ = Signature(
        parameters=[
            Parameter(key, kind=Parameter.KEYWORD_ONLY, default=None)
            for key in _keywords + list(_special_keywords.keys())
        ]
    )

    def __init__(self, **kwargs):
        # Save values so that we can revert to their initial values
        self.old_defaults = {}
        with Session() as lib:
            for key in kwargs:
                if key in self._special_keywords:
                    for k in self._special_keywords[key]:
                        self.old_defaults[k] = lib.get_default(k)
                else:
                    self.old_defaults[key] = lib.get_default(key)

        # call gmt set to change GMT defaults
        with Session() as lib:
            lib.call_module(
                module="set", args=[f"{key}={value}" for key, value in kwargs.items()]
            )

    def __enter__(self):
        """
        Do nothing but return the object.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Revert GMT configurations to initial values.
        """
        with Session() as lib:
            lib.call_module(
                module="set",
                args=[f"{key}={value}" for key, value in self.old_defaults.items()],
            )
