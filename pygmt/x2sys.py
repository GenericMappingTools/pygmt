"""
GMT supplementary X2SYS module for crossover analysis.
"""
import pandas as pd
import xarray as xr

from .clib import Session
from .helpers import (
    build_arg_string,
    fmt_docstring,
    GMTTempFile,
    use_alias,
    data_kind,
    dummy_context,
)
from .exceptions import GMTInvalidInput


@fmt_docstring
@use_alias(D="fmtfile", F="force")
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

    """
    with Session() as lib:
        arg_str = " ".join([tag, build_arg_string(kwargs)])
        lib.call_module(module="x2sys_init", args=arg_str)


@fmt_docstring
@use_alias(T="tag", Q="coe")
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
    tracks : pandas.DataFrame or str
        Either a table with (x, y) or (lon, lat) values in the first two
        columns, or a filename (e.g. csv, txt format). More columns may be
        present.

    outfile : str
        Optional. The file name for the output ASCII txt file to store the
        table in.

    tag : str
        Specify the x2sys TAG which identifies the attributes of this data
        type.

    coe : str
        Use **e** for external COEs only, and **i** for internal COEs only
        [Default is all COEs].

    Returns
    -------
    crossover_errors : pandas.DataFrame or None
        Table containing crossover error information.
        Return type depends on whether the outfile parameter is set:

        - pandas.DataFrame table with (x, y, ..., etc) if outfile is not set
        - None if outfile is set (track output will be stored in outfile)

    """
    # kinds = [data_kind(data=track) for track in tracks]
    track = tracks[0]
    kind = data_kind(track)

    with Session() as lib:
        # for kind, track in zip(kinds, tracks):
        if kind == "file":
            file_context = dummy_context(track)
        elif kind == "matrix":
            file_context = lib.virtualfile_from_matrix(track.values)

        with GMTTempFile(suffix=".txt") as tmpfile:
            with file_context as fname:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([fname, build_arg_string(kwargs), "->" + outfile])
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
