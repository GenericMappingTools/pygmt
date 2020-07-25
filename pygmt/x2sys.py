"""
GMT supplementary X2SYS module for crossover analysis.
"""
import contextlib

import pandas as pd

from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    D="fmtfile",
    E="suffix",
    F="force",
    G="discontinuity",
    I="spacing",
    N="units",
    R="region",
    V="verbose",
    W="gap",
    j="distcalc",
)
@kwargs_to_strings(I="sequence", R="sequence")
def x2sys_init(tag, **kwargs):
    """
    Initialize a new x2sys track database.

    x2sys_init is the starting point for anyone wishing to use x2sys; it
    initializes a set of data bases that are particular to one kind of track
    data. These data, their associated data bases, and key parameters are given
    a short-hand notation called an x2sys TAG. The TAG keeps track of settings
    such as file format, whether the data are geographic or not, and the
    binning resolution for track indices.

    Before you can run x2sys_init you must set the environmental parameter
    X2SYS_HOME to a directory where you have write permission, which is where
    x2sys can keep track of your settings.

    Full option list at :gmt-docs:`supplements/x2sys/x2sys_init.html`

    {aliases}

    Parameters
    ----------
    tag : str
        The unique name of this data type x2sys TAG.

    fmtfile : str
        Format definition file prefix for this data set [See Format Definition
        Files for more information]. Specify full path if the file is not in
        the current directory.

        Some file formats already have definition files premade. These include:

        - mgd77 (for plain ASCII MGD77 data files)
        - mgd77+ (for enhanced MGD77+ netCDF files)
        - gmt (for old mgg supplement binary files)
        - xy (for plain ASCII x, y tables)
        - xyz (same, with one z-column)
        - geo (for plain ASCII longitude, latitude files)
        - geoz (same, with one z-column).

    suffix : str
        Specifies the file extension (suffix) for these data files. If not
        given we use the format definition file prefix as the suffix (see
        *fmtfile*).

    discontinuity : str
        ``d|g``
        Selects geographical coordinates. Append **d** for discontinuity at the
        Dateline (makes longitude go from -180 to + 180) or **g** for
        discontinuity at Greenwich (makes longitude go from 0 to 360
        [Default]). If not given we assume the data are Cartesian.

    spacing : str or list
         ``dx[/dy]``
         x_inc [and optionally y_inc] is the grid spacing. Append **m** to
         indicate minutes or **s** to indicate seconds for geographic data.
         These spacings refer to the binning used in the track bin-index data
         base.

    units : str or list
        ``d|sunit``.
        Sets the units used for distance and speed when requested by other
        programs. Append **d** for distance or **s** for speed, then give the
        desired unit as:

        - **c** - Cartesian userdist or userdist/usertime
        - **e** - meters or m/s
        - **f** - feet or feet/s
        - **k** - km or kms/hr
        - **m** - miles or miles/hr
        - **n** - nautical miles or knots
        - **u** - survey feet or survey feet/s

        Default is ``units=["dk", "se"]`` (km and m/s) if *discontinuity* is
        set, and ``units=["dc", "sc"]`` otherwise (Cartesian units).

    {R}
    {V}

    gap : str or list
        ``t|dgap``.
        Give **t** or **d** and append the corresponding maximum time gap (in
        user units; this is typically seconds [Infinity]), or distance (for
        units, see *units*) gap [Infinity]) allowed between the two data points
        immediately on either side of a crossover. If these limits are exceeded
        then a data gap is assumed and no COE will be determined.

    {j}
    """
    with Session() as lib:
        arg_str = " ".join([tag, build_arg_string(kwargs)])
        lib.call_module(module="x2sys_init", args=arg_str)


@fmt_docstring
@use_alias(T="tag", Q="coe", V="verbose")
def x2sys_cross(tracks=None, outfile=None, **kwargs):
    """
    Calculate crossovers between track data files.

    x2sys_cross is used to determine all intersections between ("external
    cross-overs") or within ("internal cross-overs") tracks (Cartesian or
    geographic), and report the time, position, distance along track, heading
    and speed along each track segment, and the crossover error (COE) and mean
    values for all observables. The names of the tracks are passed on the
    command line. By default, x2sys_cross will look for both external and
    internal COEs. As an option, you may choose to project all data using one
    of the map-projections prior to calculating the COE.

    Full option list at :gmt-docs:`supplements/x2sys/x2sys_cross.html`

    {aliases}

    Parameters
    ----------
    tracks : str or list
        A table or a list of tables with (x, y) or (lon, lat) values in the
        first two columns. Supported formats are ASCII, native binary, or
        COARDS netCDF 1-D data. More columns may also be present.

        If the filenames are missing their file extension, we will append the
        suffix specified for this TAG. Track files will be searched for first
        in the current directory and second in all directories listed in
        $X2SYS_HOME/TAG/TAG_paths.txt (if it exists). [If $X2SYS_HOME is not
        set it will default to $GMT_SHAREDIR/x2sys]. (Note: MGD77 files will
        also be looked for via $MGD77_HOME/mgd77_paths.txt and *.gmt files will
        be searched for via $GMT_SHAREDIR/mgg/gmtfile_paths).

    outfile : str
        Optional. The file name for the output ASCII txt file to store the
        table in.

    tag : str
        Specify the x2sys TAG which identifies the attributes of this data
        type.

    coe : str
        Use **e** for external COEs only, and **i** for internal COEs only
        [Default is all COEs].

    {V}

    Returns
    -------
    crossover_errors : pandas.DataFrame or None
        Table containing crossover error information.
        Return type depends on whether the outfile parameter is set:

        - pandas.DataFrame table with (x, y, ..., etc) if outfile is not set
        - None if outfile is set (track output will be stored in outfile)
    """
    with Session() as lib:
        file_contexts = []
        for track in tracks:
            kind = data_kind(track)
            if kind == "file":
                file_contexts.append(dummy_context(track))
            elif kind == "matrix":
                raise NotImplementedError(f"{type(track)} inputs are not supported yet")
                # file_contexts.append(lib.virtualfile_from_matrix(track.values))
            else:
                raise GMTInvalidInput(f"Unrecognized data type: {type(track)}")

        with GMTTempFile(suffix=".txt") as tmpfile:
            with contextlib.ExitStack() as stack:
                fnames = [stack.enter_context(c) for c in file_contexts]
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([*fnames, build_arg_string(kwargs), "->" + outfile])
                lib.call_module(module="x2sys_cross", args=arg_str)

            # Read temporary csv output to a pandas table
            if outfile == tmpfile.name:  # if outfile isn't set, return pd.DataFrame
                # Read the tab-separated ASCII table
                # Header is on 2nd row, and we skip the 3rd row with a ">"
                df = pd.read_csv(tmpfile.name, sep="\t", header=2, comment=">")
                # Remove the "# " from "# x" in the first column
                result = df.rename(columns={df.columns[0]: df.columns[0][2:]})
            elif outfile != tmpfile.name:  # if outfile is set, output in outfile only
                result = None

    return result
