"""
config - set GMT defaults globally or locally.
"""

from typing import Any, ClassVar, Literal, TypedDict

from pygmt.clib import Session


class Parameters(TypedDict):
    """
    A TypedDict that defines the valid keyword arguments for pygmt.config.
    """

    COLOR_BACKGROUND: Any
    COLOR_FOREGROUND: Any
    COLOR_CPT: Any
    COLOR_NAN: Any
    COLOR_MODEL: Literal["none", "rgb", "hsv", "cmyk"]
    COLOR_HSV_MIN_S: Any
    COLOR_HSV_MAX_S: Any
    COLOR_HSV_MIN_V: Any
    COLOR_HSV_MAX_V: Any
    COLOR_SET: Any
    DIR_CACHE: Any
    DIR_DATA: Any
    DIR_DCW: Any
    DIR_GSHHG: Any
    FONT_ANNOT_PRIMARY: Any
    FONT_ANNOT_SECONDARY: Any
    FONT_HEADING: Any
    FONT_LABEL: Any
    FONT_LOGO: Any
    FONT_SUBTITLE: Any
    FONT_TAG: Any
    FONT_TITLE: Any
    FORMAT_CLOCK_IN: Any
    FORMAT_CLOCK_OUT: Any
    FORMAT_CLOCK_MAP: Any
    FORMAT_DATE_IN: Any
    FORMAT_DATE_OUT: Any
    FORMAT_DATE_MAP: Any
    FORMAT_GEO_OUT: Any
    FORMAT_GEO_MAP: Any
    FORMAT_FLOAT_OUT: Any
    FORMAT_FLOAT_MAP: Any
    FORMAT_TIME_PRIMARY_MAP: Any
    FORMAT_TIME_SECONDARY_MAP: Any
    FORMAT_TIME_STAMP: Any
    GMT_DATA_SERVER: Any
    GMT_DATA_SERVER_LIMIT: Any
    GMT_DATA_UPDATE_INTERVAL: Any
    GMT_COMPATIBILITY: Any
    GMT_CUSTOM_LIBS: Any
    GMT_EXPORT_TYPE: Any
    GMT_EXTRAPOLATE_VAL: Any
    GMT_FFT: Any
    GMT_GRAPHICS_DPU: Any
    GMT_GRAPHICS_FORMAT: Any
    GMT_HISTORY: Any
    GMT_INTERPOLANT: Any
    GMT_LANGUAGE: Any
    GMT_MAX_CORES: Any
    GMT_THEME: Any
    GMT_TRIANGULATE: Any
    GMT_VERBOSE: Any
    IO_COL_SEPARATOR: Any
    IO_FIRST_HEADER: Any
    IO_GRIDFILE_FORMAT: Any
    IO_GRIDFILE_SHORTHAND: Any
    IO_HEADER: Any
    IO_HEADER_MARKER: Any
    IO_N_HEADER_RECS: Any
    IO_NAN_RECORDS: Any
    IO_NC4_CHUNK_SIZE: Any
    IO_NC4_DEFLATION_LEVEL: Any
    IO_LONLAT_TOGGLE: Any
    IO_SEGMENT_BINARY: Any
    IO_SEGMENT_MARKER: Any
    MAP_ANNOT_MIN_ANGLE: Any
    MAP_ANNOT_MIN_SPACING: Any
    MAP_ANNOT_OBLIQUE: Any
    MAP_ANNOT_OFFSET_PRIMARY: Any
    MAP_ANNOT_OFFSET_SECONDARY: Any
    MAP_ANNOT_ORTHO: Any
    MAP_DEFAULT_PEN: Any
    MAP_DEGREE_SYMBOL: Any
    MAP_EMBELLISHMENT_MODE: Any
    MAP_FRAME_AXES: Any
    MAP_FRAME_PEN: Any
    MAP_FRAME_PERCENT: Any
    MAP_FRAME_TYPE: Any
    MAP_FRAME_WIDTH: Any
    MAP_GRID_CROSS_SIZE_PRIMARY: Any
    MAP_GRID_CROSS_SIZE_SECONDARY: Any
    MAP_GRID_PEN_PRIMARY: Any
    MAP_GRID_PEN_SECONDARY: Any
    MAP_HEADING_OFFSET: Any
    MAP_LABEL_MODE: Any
    MAP_LABEL_OFFSET: Any
    MAP_LINE_STEP: Any
    MAP_LOGO: Any
    MAP_LOGO_POS: Any
    MAP_ORIGIN_X: Any
    MAP_ORIGIN_Y: Any
    MAP_POLAR_CAP: Any
    MAP_SCALE_HEIGHT: Any
    MAP_TICK_LENGTH_PRIMARY: Any
    MAP_TICK_LENGTH_SECONDARY: Any
    MAP_TICK_PEN_PRIMARY: Any
    MAP_TICK_PEN_SECONDARY: Any
    MAP_TITLE_OFFSET: Any
    MAP_VECTOR_SHAPE: Any
    PROJ_AUX_LATITUDE: Any
    PROJ_DATUM: Any
    PROJ_ELLIPSOID: Any
    PROJ_GEODESIC: Any
    PROJ_LENGTH_UNIT: Any
    PROJ_MEAN_RADIUS: Any
    PROJ_SCALE_FACTOR: Any
    PS_CHAR_ENCODING: Any
    PS_COLOR_MODEL: Any
    PS_COMMENTS: Any
    PS_CONVERT: Any
    PS_IMAGE_COMPRESS: Any
    PS_LINE_CAP: Any
    PS_LINE_JOIN: Any
    PS_MITER_LIMIT: Any
    PS_MEDIA: Any
    PS_PAGE_COLOR: Any
    PS_PAGE_ORIENTATION: Any
    PS_SCALE_X: Any
    PS_SCALE_Y: Any
    PS_TRANSPARENCY: Any
    TIME_EPOCH: Any
    TIME_IS_INTERVAL: Any
    TIME_INTERVAL_FRACTION: Any
    TIME_LEAP_SECONDS: Any
    TIME_REPORT: Any
    TIME_UNIT: Any
    TIME_WEEK_START: Any
    TIME_Y2K_OFFSET_YEAR: Any
    # special keywords
    FONT: Any
    FONT_ANNOT: Any
    FORMAT_TIME_MAP: Any
    MAP_ANNOT_OFFSET: Any
    MAP_GRID_CROSS_SIZE: Any
    MAP_GRID_PEN: Any
    MAP_TICK_LENGTH: Any
    MAP_TICK_PEN: Any


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

    """
    __signature__ = Signature(
        parameters=[
            Parameter(
                key,
                kind=Parameter.KEYWORD_ONLY,
                default=getattr(Parameters, key),
            )
            for key in Parameters.__annotations__
        ]
    )
    """

    def __init__(self, **kwargs: Parameters):
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
