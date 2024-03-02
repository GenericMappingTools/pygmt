"""
Wrapper for the GMT_DATASET data type.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import pandas as pd


class _GMT_DATASET(ctp.Structure):  # noqa: N801
    """
    GMT dataset structure for holding multiple tables (files).

    This class is only meant for internal use by PyGMT and is not exposed to users.
    See the GMT source code gmt_resources.h for the original C struct definitions.

    Examples
    --------
    >>> from pygmt.helpers import GMTTempFile
    >>> from pygmt.clib import Session
    >>>
    >>> with GMTTempFile(suffix=".txt") as tmpfile:
    ...     # Prepare the sample data file
    ...     with open(tmpfile.name, mode="w") as fp:
    ...         print(">", file=fp)
    ...         print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
    ...         print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)
    ...         print(">", file=fp)
    ...         print("7.0 8.0 9.0 TEXT8 TEXT90", file=fp)
    ...         print("10.0 11.0 12.0 TEXT123 TEXT456789", file=fp)
    ...     # Read the data file
    ...     with Session() as lib:
    ...         with lib.virtualfile_out(kind="dataset") as vouttbl:
    ...             lib.call_module("read", f"{tmpfile.name} {vouttbl} -Td")
    ...             # The dataset
    ...             ds = lib.read_virtualfile(vouttbl, kind="dataset").contents
    ...             print(ds.n_tables, ds.n_columns, ds.n_segments)
    ...             print(ds.min[: ds.n_columns], ds.max[: ds.n_columns])
    ...             # The table
    ...             tbl = ds.table[0].contents
    ...             print(tbl.n_columns, tbl.n_segments, tbl.n_records)
    ...             print(tbl.min[: tbl.n_columns], ds.max[: tbl.n_columns])
    ...             for i in range(tbl.n_segments):
    ...                 seg = tbl.segment[i].contents
    ...                 for j in range(seg.n_columns):
    ...                     print(seg.data[j][: seg.n_rows])
    ...                 print(seg.text[: seg.n_rows])
    1 3 2
    [1.0, 2.0, 3.0] [10.0, 11.0, 12.0]
    3 2 4
    [1.0, 2.0, 3.0] [10.0, 11.0, 12.0]
    [1.0, 4.0]
    [2.0, 5.0]
    [3.0, 6.0]
    [b'TEXT1 TEXT23', b'TEXT4 TEXT567']
    [7.0, 10.0]
    [8.0, 11.0]
    [9.0, 12.0]
    [b'TEXT8 TEXT90', b'TEXT123 TEXT456789']
    """

    class _GMT_DATATABLE(ctp.Structure):  # noqa: N801
        """
        GMT datatable structure for holding a table with multiple segments.
        """

        class _GMT_DATASEGMENT(ctp.Structure):  # noqa: N801
            """
            GMT datasegment structure for holding a segment with multiple columns.
            """

            _fields_: ClassVar = [
                # Number of rows/records in this segment
                ("n_rows", ctp.c_uint64),
                # Number of fields in each record
                ("n_columns", ctp.c_uint64),
                # Minimum coordinate for each column
                ("min", ctp.POINTER(ctp.c_double)),
                # Maximum coordinate for each column
                ("max", ctp.POINTER(ctp.c_double)),
                # Data x, y, and possibly other columns
                ("data", ctp.POINTER(ctp.POINTER(ctp.c_double))),
                # Label string (if applicable)
                ("label", ctp.c_char_p),
                # Segment header (if applicable)
                ("header", ctp.c_char_p),
                # text beyond the data
                ("text", ctp.POINTER(ctp.c_char_p)),
                # Book-keeping variables "hidden" from the API
                ("hidden", ctp.c_void_p),
            ]

        _fields_: ClassVar = [
            # Number of file header records (0 if no header)
            ("n_headers", ctp.c_uint),
            # Number of columns (fields) in each record
            ("n_columns", ctp.c_uint64),
            # Number of segments in the array
            ("n_segments", ctp.c_uint64),
            # Total number of data records across all segments
            ("n_records", ctp.c_uint64),
            # Minimum coordinate for each column
            ("min", ctp.POINTER(ctp.c_double)),
            # Maximum coordinate for each column
            ("max", ctp.POINTER(ctp.c_double)),
            # Array with all file header records, if any
            ("header", ctp.POINTER(ctp.c_char_p)),
            # Pointer to array of segments
            ("segment", ctp.POINTER(ctp.POINTER(_GMT_DATASEGMENT))),
            # Book-keeping variables "hidden" from the API
            ("hidden", ctp.c_void_p),
        ]

    _fields_: ClassVar = [
        # The total number of tables (files) contained
        ("n_tables", ctp.c_uint64),
        # The number of data columns
        ("n_columns", ctp.c_uint64),
        #  The total number of segments across all tables
        ("n_segments", ctp.c_uint64),
        # The total number of data records across all tables
        ("n_records", ctp.c_uint64),
        # Minimum coordinate for each column
        ("min", ctp.POINTER(ctp.c_double)),
        # Maximum coordinate for each column
        ("max", ctp.POINTER(ctp.c_double)),
        # Pointer to array of tables
        ("table", ctp.POINTER(ctp.POINTER(_GMT_DATATABLE))),
        # The datatype (numerical, text, or mixed) of this dataset
        ("type", ctp.c_int32),
        # The geometry of this dataset
        ("geometry", ctp.c_int32),
        # To store a referencing system string in PROJ.4 format
        ("ProjRefPROJ4", ctp.c_char_p),
        # To store a referencing system string in WKT format
        ("ProjRefWKT", ctp.c_char_p),
        # To store a referencing system EPSG code
        ("ProjRefEPSG", ctp.c_int),
        # Book-keeping variables "hidden" from the API
        ("hidden", ctp.c_void_p),
    ]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert a _GMT_DATASET object to a :class:`pandas.DataFrame` object.

        Currently, the number of columns in all segments of all tables are assumed to be
        the same. The same column in all segments of all tables are concatenated. The
        trailing text column is also concatenated as a single string column.

        Returns
        -------
        df
            A :class:`pandas.DataFrame` object.

        Examples
        --------
        >>> from pygmt.helpers import GMTTempFile
        >>> from pygmt.clib import Session
        >>>
        >>> with GMTTempFile(suffix=".txt") as tmpfile:
        ...     # prepare the sample data file
        ...     with open(tmpfile.name, mode="w") as fp:
        ...         print(">", file=fp)
        ...         print("1.0 2.0 3.0 TEXT1 TEXT23", file=fp)
        ...         print("4.0 5.0 6.0 TEXT4 TEXT567", file=fp)
        ...         print(">", file=fp)
        ...         print("7.0 8.0 9.0 TEXT8 TEXT90", file=fp)
        ...         print("10.0 11.0 12.0 TEXT123 TEXT456789", file=fp)
        ...     with Session() as lib:
        ...         with lib.virtualfile_out(kind="dataset") as vouttbl:
        ...             lib.call_module("read", f"{tmpfile.name} {vouttbl} -Td")
        ...             ds = lib.read_virtualfile(vouttbl, kind="dataset")
        ...             df = ds.contents.to_dataframe()
        >>> df
              0     1     2                   3
        0   1.0   2.0   3.0        TEXT1 TEXT23
        1   4.0   5.0   6.0       TEXT4 TEXT567
        2   7.0   8.0   9.0        TEXT8 TEXT90
        3  10.0  11.0  12.0  TEXT123 TEXT456789
        """
        # Deal with numeric columns
        vectors = []
        for icol in range(self.n_columns):
            colvector = []
            for itbl in range(self.n_tables):
                dtbl = self.table[itbl].contents
                for iseg in range(dtbl.n_segments):
                    dseg = dtbl.segment[iseg].contents
                    colvector.append(
                        np.ctypeslib.as_array(dseg.data[icol], shape=(dseg.n_rows,))
                    )
            vectors.append(np.concatenate(colvector))

        # Deal with trailing text column
        textvector = []
        for itbl in range(self.n_tables):
            dtbl = self.table[itbl].contents
            for iseg in range(dtbl.n_segments):
                dseg = dtbl.segment[iseg].contents
                if dseg.text:
                    textvector.extend(dseg.text[: dseg.n_rows])
        if textvector:
            vectors.append(np.char.decode(textvector))

        df = pd.concat([pd.Series(v) for v in vectors], axis=1)

        # convert text data from object dtype to string dtype
        if textvector:
            df = df.convert_dtypes(
                convert_string=True,
                convert_integer=False,
                convert_floating=False,
                convert_boolean=False,
            )
        return df
