"""
Wrappers for GMT data types.
"""
import ctypes as ctp

import numpy as np


# Python representation of the GMT data types.
# See the comments in the `GMT_DATASET.to_pydata` method for more details.
class PyGMT_DATASET:
    def __init__(self, table):
        self.table = table


class PyGMT_DATATABLE:
    def __init__(self, segment):
        self.segment = segment


class PyGMT_DATASEGMENT:
    def __init__(self, data):
        self.data = data


class GMT_DATASET(ctp.Structure):
    """
    GMT dataset structure for holding multiple tables (files).

    This class is only meant for internal use by PyGMT. It is not exposed to
    users.

    See the GMT source code gmt_resources.h for the original C struct
    definitions.

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
    ...     # read the data file
    ...     with Session() as lib:
    ...         with lib.virtualfile_to_data(kind="dataset") as vouttbl:
    ...             lib.call_module("read", f"{tmpfile.name} {vouttbl} -Td")
    ...             # the dataset
    ...             ds = lib.read_virtualfile(vouttbl, kind="dataset").contents
    ...             print(ds.n_tables, ds.n_columns, ds.n_segments)
    ...             print(ds.min[: ds.n_columns], ds.max[: ds.n_columns])
    ...             # the table
    ...             tbl = ds.table[0].contents
    ...             print(tbl.n_columns, tbl.n_segments, tbl.n_records)
    ...             print(tbl.min[: tbl.n_columns], ds.max[: tbl.n_columns])
    ...             for i in range(tbl.n_segments):
    ...                 seg = tbl.segment[i].contents
    ...                 for j in range(seg.n_columns):
    ...                     print(seg.data[j][: seg.n_rows])
    ...                 print(seg.text[: seg.n_rows])
    ...
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

    class GMT_DATATABLE(ctp.Structure):
        """
        GMT datatable structure for holding a single table with multiple
        segments.
        """

        class GMT_DATASEGMENT(ctp.Structure):
            """
            GMT datasegment structure for holding a single segment with
            multiple columns.
            """

            _fields_ = [
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

        _fields_ = [
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
            ("segment", ctp.POINTER(ctp.POINTER(GMT_DATASEGMENT))),
            # Book-keeping variables "hidden" from the API
            ("hidden", ctp.c_void_p),
        ]

    _fields_ = [
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
        ("table", ctp.POINTER(ctp.POINTER(GMT_DATATABLE))),
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

    def to_vectors(self):
        """
        Convert a GMT_DATASET object to a list of vectors.

        Currently, the number of columns in all segments of all tables are
        assumed to be the same. The same column in all segments of all tables
        are concatenated. The trailing text column is also concatenated as a
        string vector.

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
        ...         with lib.virtualfile_to_data(kind="dataset") as vouttbl:
        ...             lib.call_module(
        ...                 "read", f"{tmpfile.name} {vouttbl} -Td"
        ...             )
        ...             ds = lib.read_virtualfile(vouttbl, kind="dataset")
        ...             vectors = ds.contents.to_vectors()
        ...
        >>> len(vectors)  # 4 columns
        4
        >>> vectors[0]
        array([ 1.,  4.,  7., 10.])
        >>> vectors[1]
        array([ 2.,  5.,  8., 11.])
        >>> vectors[2]
        array([ 3.,  6.,  9., 12.])
        >>> vectors[3]
        array(['TEXT1 TEXT23', 'TEXT4 TEXT567', 'TEXT8 TEXT90',
                'TEXT123 TEXT456789'], dtype='<U18')

        Returns
        -------
        vectors : list of 1-D arrays
            List of vectors containing the data from the GMT_DATASET object.
        """
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

        # deal with trailing text column
        textvector = []
        for itbl in range(self.n_tables):
            dtbl = self.table[itbl].contents
            for iseg in range(dtbl.n_segments):
                dseg = dtbl.segment[iseg].contents
                if dseg.text:
                    textvector.extend(dseg.text[: dseg.n_rows])
        if textvector:
            vectors.append(np.char.decode(textvector))

        return vectors

    def to_pydata(self):
        """
        Convert the ctypes GMT_DATASET object to the Python PyGMT_DATASET
        object.

        The ctypes GMT_DATASET/GMT_DATATABLE/GMT_DATASEGMENT objects are
        difficult to use, because most of attributes are pointers to other
        objects or ctypes arrays. For example, let's say ``dataset`` is a
        GMT_DATASET object, and you want to access the data of the first
        segment of the first table, you have to use the following code
        (note the ``contents`` attribute)::

            data = dataset.table[0].contents.segment[0].contents.data

        Now ``data`` is a ``POINTER(POINTER(c_double))`` object. The first
        column is ``data[0]``, but you can't use ``print(data[0])`` to print
        the data, because it will print the memory address of the data.
        You have to use::

            print(np.ctypeslib.as_array(data[0], shape=(n_rows,)))

        to print the data. It's difficult to use for us developers (see the
        ``to_vectors`` above for example). It will be even more difficult to
        understand for users. So, exposing the ctypes objects to users is a
        bad idea.

        This method converts the ctypes object to a Python object, which is
        easier to use. For example, the following code converts the ``dataset``
        to a Python object::

            pydata = dataset.to_pydata()

        Now ``pydata`` is a PyGMT_DATASET object.

        To get the number of tables, you can use the following code::

            len(pydata.table)

        To get the first column of the first  segment of the first table::

            pydata.table[0].segment[0].data[0]

        The PyGMT_DATASET object is more Pythonic and can be exposed to users.
        The most big benefit is that now it's possible to support
        multiple-segment files with headers (e.g., a segment with header
        ``> -Z1.0``).

        However, the arrays in the Python object are still pointers to the
        original memory allocated by GMT, so the data will be destroyed when
        the Session ends. We may need to copy the data to a new memory location
        if we want to use the data after the Session ends.

        Notes
        -----
        In GMT.jl, the GMT_DATASET is defined in
        https://github.com/GenericMappingTools/GMT.jl/blob/master/src/libgmt_h.jl#L119.
        It also provides the more friendly data type GMTdataset.
        See https://www.generic-mapping-tools.org/GMT.jl/dev/types/#Dataset-type.

        A `get_dataset` function is provided to convert GMT's GMT_DATASET
        to GMT.jl's GMTdataset.
        """
        table = []
        for itbl in range(self.n_tables):
            segment = []
            for iseg in range(self.table[itbl].contents.n_segments):
                seg = self.table[itbl].contents.segment[iseg].contents
                n_columns, n_rows = seg.n_columns, seg.n_rows
                data = [
                    np.ctypeslib.as_array(seg.data[icol], shape=(n_rows,))
                    for icol in range(n_columns)
                ]
                segment.append(PyGMT_DATASEGMENT(data=data))
            table.append(PyGMT_DATATABLE(segment=segment))
        pydata = PyGMT_DATASET(table=table)
        pydata.n_columns = self.n_columns
        return pydata