import ctypes as ctp


class GMT_DATASEGMENT(ctp.Structure):
    """
    For holding segment lines in memory.
    """

    _fields_ = [
        ("n_rows", ctp.c_uint64),  # Number of points in this segment
        ("n_columns", ctp.c_uint64),  # Number of fields in each record (>= 2)
        ("min", ctp.POINTER(ctp.c_double)),  # Minimum coordinate for each column
        ("max", ctp.POINTER(ctp.c_double)),  # Maximum coordinate for each column
        # Data x, y, and possibly other columns
        ("data", ctp.POINTER(ctp.POINTER(ctp.c_double))),
        ("label", ctp.c_char_p),  # Label string (if applicable)
        ("header", ctp.c_char_p),  # Segment header (if applicable)
        ("text", ctp.POINTER(ctp.c_char_p)),  # text beyond the data
        ("hidden", ctp.c_void_p),  # Book-keeping variables "hidden" from the API
    ]


class GMT_DATATABLE(ctp.Structure):
    """
    To hold an array of line segment structures and header information in one
    container.
    """

    _fields_ = [
        ("n_headers", ctp.c_uint),  # Number of file header records (0 if no header)
        ("n_columns", ctp.c_uint64),  # Number of columns (fields) in each record
        ("n_segments", ctp.c_uint64),  # Number of segments in the array
        ("n_records", ctp.c_uint64),  # Total number of data records across all segments
        ("min", ctp.POINTER(ctp.c_double)),  # Minimum coordinate for each column
        ("max", ctp.POINTER(ctp.c_double)),  # Maximum coordinate for each column
        (
            "header",
            ctp.POINTER(ctp.c_char_p),
        ),  # Array with all file header records, if any
        (
            "segment",
            ctp.POINTER(ctp.POINTER(GMT_DATASEGMENT)),
        ),  # Pointer to array of segments
        ("hidden", ctp.c_void_p),  # Book-keeping variables "hidden" from the API
    ]


class GMT_DATASET(ctp.Structure):
    """
    Single container for an array of GMT tables (files)
    """

    _fields_ = [
        ("n_tables", ctp.c_uint64),  # The total number of tables (files) contained
        ("n_columns", ctp.c_uint64),  # The number of data columns
        ("n_segments", ctp.c_uint64),  #  The total number of segments across all tables
        # The total number of data records across all tables
        ("n_records", ctp.c_uint64),
        ("min", ctp.POINTER(ctp.c_double)),  # Minimum coordinate for each column
        ("max", ctp.POINTER(ctp.c_double)),  # Maximum coordinate for each column
        # Pointer to array of tables
        ("table", ctp.POINTER(ctp.POINTER(GMT_DATATABLE))),
        # The datatype (numerical, text, or mixed) of this dataset
        ("type", ctp.c_int32),
        ("geometry", ctp.c_int32),  # The geometry of this dataset
        # To store a referencing system string in PROJ.4 format
        ("ProjRefPROJ4", ctp.c_char_p),
        # To store a referencing system string in WKT format
        (
            "ProjRefWKT",
            ctp.c_char_p,
        ),
        ("ProjRefEPSG", ctp.c_int),  # To store a referencing system EPSG code
        ("hidden", ctp.c_void_p),  # Book-keeping variables "hidden" from the API
    ]
