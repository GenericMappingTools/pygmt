"""
GMT supplementary X2SYS module for crossover analysis.
"""
import contextlib
import os
import re

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


@contextlib.contextmanager
def tempfile_from_dftrack(track, suffix):
    """
    Saves a pandas.DataFrame track table to a temporary tab-separated ASCII
    text file with a suffix (e.g. 'xyz').
    """
    with GMTTempFile(suffix=suffix) as tmpfile:
        track.to_csv(
            path_or_buf=tmpfile.name,
            sep="\t",
            index=False,
            date_format="%Y-%m-%dT%H:%M:%S.%fZ",
        )

        yield tmpfile.name


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
@use_alias(
    A="combitable",
    C="runtimes",
    D="override",
    I="interpolation",
    R="region",
    S="speed",
    T="tag",
    Q="coe",
    V="verbose",
    W="numpoints",
    Z="trackvalues",
)
@kwargs_to_strings(R="sequence")
def x2sys_cross(tracks=None, outfile=None, **kwargs):
    """
    Calculate crossovers between track data files.

    x2sys_cross is used to determine all intersections between ("external
    cross-overs") or within ("internal cross-overs") tracks (Cartesian or
    geographic), and report the time, position, distance along track, heading
    and speed along each track segment, and the crossover error (COE) and mean
    values for all observables. By default, x2sys_cross will look for both
    external and internal COEs. As an option, you may choose to project all
    data using one of the map-projections prior to calculating the COE.

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

    combitable : str
        Only process the pair-combinations found in the file *combitable*
        [Default process all possible combinations among the specified files].
        The file *combitable* is created by *x2sys_get*'s -L option

    runtimes : bool or str
        Compute and append the processing run-time for each pair to the
        progress message (use ``runtimes=True``). Pass in a filename (e.g.
        ``runtimes="file.txt"``) to save these run-times to file. The idea here
        is to use the knowledge of run-times to split the main process in a
        number of sub-processes that can each be launched in a different
        processor of your multi-core machine. See the MATLAB function
        split_file4coes.m that lives in the x2sys supplement source code.

    override : bool or str
        ``S|N``.
        Control how geographic coordinates are handled (Cartesian data are
        unaffected). By default, we determine if the data are closer to one
        pole than the other, and then we use a cylindrical polar conversion to
        avoid problems with longitude jumps. You can turn this off entirely
        with *override* and then the calculations uses the original data (we
        have protections against longitude jumps). However, you can force the
        selection of the pole for the projection by appending **S** or **N**
        for the south or north pole, respectively. The conversion is used
        because the algorithm used to find crossovers is inherently a
        Cartesian algorithm that can run into trouble with data that has large
        longitudinal range at higher latitudes.

    interpolation : str
        ``l|a|c``.
        Sets the interpolation mode for estimating values at the crossover.
        Choose among:

        - **l** - Linear interpolation [Default].
        - **a** - Akima spline interpolation.
        - **c** - Cubic spline interpolation.

    coe : str
        Use **e** for external COEs only, and **i** for internal COEs only
        [Default is all COEs].

    {R}

    speed : str or list
        ``l|u|hspeed``.
        Defines window of track speeds. If speeds are outside this window we do
        not calculate a COE. Specify:

        - **l** sets lower speed [Default is 0].
        - **u** sets upper speed [Default is Infinity].
        - **h** does not limit the speed but sets a lower speed below which \
        headings will not be computed (i.e., set to NaN) [Default calculates \
        headings regardless of speed].

        For example, you can use ``speed=["l0", "u10", "h5"] to set a lower
        speed of 0, upper speed of 10, and disable heading calculations for
        speeds below 5.

    {V}

    numpoints : int
        Give the maximum number of data points on either side of the crossover
        to use in the spline interpolation [Default is 3].

    trackvalues : bool
        Report the values of each track at the crossover [Default reports the
        crossover value and the mean value].

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
                # find suffix (-E) of trackfiles used (e.g. xyz, csv, etc) from
                # $X2SYS_HOME/TAGNAME/TAGNAME.tag file using regex search
                try:
                    with open(
                        os.path.join(
                            os.environ["X2SYS_HOME"], kwargs["T"], f"{kwargs['T']}.tag"
                        ),
                        "r",
                    ) as tagfile:
                        suffix = re.search(
                            pattern=r"-E(\S*)",  # match file extension after -E
                            string=tagfile.readlines()[-1],  # e.g. "-Dxyz -Exyz -I1/1"
                        ).group(1)
                except AttributeError:  # 'NoneType' object has no attribute 'group'
                    suffix = kwargs["T"]  # tempfile suffix will be same as TAG name

                # Save pandas.DataFrame track data to temporary file
                file_contexts.append(tempfile_from_dftrack(track=track, suffix=suffix))
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
                # Read the tab-separated ASCII table into pandas.DataFrame
                result = pd.read_csv(
                    tmpfile.name,
                    sep="\t",
                    header=2,  # Column names are on 2nd row
                    comment=">",  # Skip the 3rd row with a ">"
                    parse_dates=[2, 3],  # Datetimes on 3rd and 4th column
                )
                # Remove the "# " from "# x" in the first column
                result = result.rename(
                    columns={result.columns[0]: result.columns[0][2:]}
                )
            elif outfile != tmpfile.name:  # if outfile is set, output in outfile only
                result = None

    return result
