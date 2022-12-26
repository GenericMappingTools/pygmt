"""
select - Select data table subsets based on multiple spatial criteria.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["select"]


@fmt_docstring
@use_alias(
    A="area_thresh",
    D="resolution",
    G="gridmask",
    I="reverse",
    J="projection",
    N="mask",
    R="region",
    V="verbose",
    Z="z_subregion",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    o="outcols",
    s="skiprows",
    w="wrap",
)
@kwargs_to_strings(M="sequence", R="sequence", i="sequence_comma", o="sequence_comma")
def select(data=None, outfile=None, **kwargs):
    r"""
    Select data table subsets based on multiple spatial criteria.

    This is a filter that reads (x, y) or (longitude, latitude) positions from
    the first 2 columns of *data* and uses a combination of 1-7 criteria to
    pass or reject the records. Records can be selected based on whether or not
    they are:

    1. inside a rectangular region (``region`` [and ``projection``])
    2. within *dist* km of any point in *pointfile*
    3. within *dist* km of any line in *linefile*
    4. inside one of the polygons in the *polygonfile*
    5. inside geographical features (based on coastlines)
    6. has z-values within a given range, or
    7. inside bins of a grid mask whose nodes are non-zero

    The sense of the tests can be reversed for each of these 7 criteria by
    using the ``reverse`` parameter.

    Full option list at :gmt-docs:`gmtselect.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in either a file name to an ASCII data table, a 2-D
        {table-classes}.
    outfile : str
        The file name for the output ASCII file.
    {area_thresh}
    resolution : str
        *resolution*\ [**+f**].
        Ignored unless ``mask`` is set. Selects the resolution of the coastline
        data set to use ((**f**)ull, (**h**)igh, (**i**)ntermediate, (**l**)ow,
        or (**c**)rude). The resolution drops off by ~80% between data sets.
        [Default is **l**]. Append (**+f**) to automatically select a lower
        resolution should the one requested not be available [Default is abort
        if not found]. Note that because the coastlines differ in details
        it is not guaranteed that a point will remain inside [or outside] when
        a different resolution is selected.
    gridmask : str
        Pass all locations that are inside the valid data area of the grid
        *gridmask*. Nodes that are outside are either NaN or zero.
    reverse : str
        [**cflrsz**].
        Reverses the sense of the test for each of the criteria specified:

        - **c** select records NOT inside any point's circle of influence.
        - **f** select records NOT inside any of the polygons.
        - **g** will pass records inside the cells with z equal zero of the
          grid mask in ``gridmask``.
        - **l** select records NOT within the specified distance of any line.
        - **r** select records NOT inside the specified rectangular region.
        - **s** select records NOT considered inside as specified by ``mask``
          (and ``area_thresh``, ``resolution``).
        - **z** select records NOT within the range specified by
          ``z_subregion``.
    {projection}
    mask : str or list
        Pass all records whose location is inside specified geographical
        features. Specify if records should be skipped (s) or kept (k) using
        1 of 2 formats:

        - *wet/dry*.
        - *ocean/land/lake/island/pond*.

        [Default is s/k/s/k/s (i.e., s/k), which passes all points on dry
        land].
    {region}
    {verbose}
    z_subregion : str or list
        *min*\ [/*max*]\ [**+a**]\ [**+c**\ *col*]\ [**+i**].
        Pass all records whose 3rd column (*z*; *col* = 2) lies within the
        given range or is NaN (use ``skiprows`` to skip NaN records). If *max*
        is omitted then we test if *z* equals *min* instead. This means
        equality within 5 ULPs (unit of least precision;
        http://en.wikipedia.org/wiki/Unit_in_the_last_place). Input file must
        have at least three columns. To indicate no limit on *min* or *max*,
        specify a hyphen (-). If your 3rd column is absolute time then remember
        to supply ``coltypes="2T"``. To specify another column, append
        **+c**\ *col*, and to specify several tests pass a list of arguments
        as you have columns to test.
        **Note**: When more than one ``z_subregion`` argument is given then the
        ``reverse="z"`` cannot be used. In the case of multiple tests
        you may use these modifiers as well: **+a** passes any record that
        passes at least one of your *z* tests [Default is all tests must pass],
        and **+i** reverses the tests to pass record with *z* value NOT in the
        given range. Finally, if **+c** is not used then it is automatically
        incremented for each new ``z_subregion`` argument, starting with 2.
    {binary}
    {nodata}
    {find}
    {coltypes}
    {gap}
    {header}
    {incols}
    {outcols}
    {skiprows}
    {wrap}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table if ``outfile`` is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).

    Example
    -------
    >>> import pygmt
    >>> # Load a table of ship observations of bathymetry off Baja California
    >>> ship_data = pygmt.datasets.load_sample_data(name="bathymetry")
    >>> # Only return the data points that lie within the region between
    >>> # longitudes 246 and 247 and latitudes 20 and 21
    >>> out = pygmt.select(data=ship_data, region=[246, 247, 20, 21])
    """

    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with table_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                lib.call_module(
                    module="select",
                    args=build_arg_string(kwargs, infile=infile, outfile=outfile),
                )

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            try:
                column_names = data.columns.to_list()
                result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)
            except AttributeError:  # 'str' object has no attribute 'columns'
                result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

    return result
