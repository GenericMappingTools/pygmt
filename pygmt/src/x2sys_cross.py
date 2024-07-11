"""
x2sys_cross - Calculate crossovers between track data files.
"""

import contextlib
import os
from pathlib import Path
from typing import Any

import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    unique_name,
    use_alias,
)


@contextlib.contextmanager
def tempfile_from_dftrack(track, suffix):
    """
    Saves pandas.DataFrame track table to a temporary tab-separated ASCII text file with
    a unique name (to prevent clashes when running x2sys_cross), adding a suffix
    extension to the end.

    Parameters
    ----------
    track : pandas.DataFrame
        A table holding track data with coordinate (x, y) or (lon, lat) values,
        and (optionally) time (t).
    suffix : str
        File extension, e.g. xyz, tsv, etc.

    Yields
    ------
    tmpfilename : str
        A temporary tab-separated value file with a unique name holding the
        track data. E.g. 'track-1a2b3c4.tsv'.
    """
    try:
        tmpfilename = f"track-{unique_name()[:7]}.{suffix}"
        track.to_csv(
            path_or_buf=tmpfilename,
            sep="\t",
            index=False,
            na_rep="NaN",  # write a NaN value explicitly instead of a blank string
            date_format="%Y-%m-%dT%H:%M:%S.%fZ",  # ISO8601 format
        )
        yield tmpfilename
    finally:
        Path(tmpfilename).unlink()


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
def x2sys_cross(
    tracks=None, outfile: str | None = None, **kwargs
) -> pd.DataFrame | None:
    r"""
    Calculate crossovers between track data files.

    Determines all intersections between ("external cross-overs") or within
    ("internal cross-overs") tracks (Cartesian or geographic), and report the
    time, position, distance along track, heading and speed along each track
    segment, and the crossover error (COE) and mean values for all observables.
    By default, :func:`pygmt.x2sys_cross` will look for both external and
    internal COEs. As an option, you may choose to project all data using one
    of the map projections prior to calculating the COE.

    Full option list at :gmt-docs:`supplements/x2sys/x2sys_cross.html`

    {aliases}

    Parameters
    ----------
    tracks : pandas.DataFrame or str or list
        A table or a list of tables with (x, y) or (lon, lat) values in the
        first two columns. Track(s) can be provided as pandas DataFrame tables
        or file names. Supported file formats are ASCII, native binary, or
        COARDS netCDF 1-D data. More columns may also be present.

        If the file names are missing their file extension, we will append the
        suffix specified for this TAG. Track files will be searched for first
        in the current directory and second in all directories listed in
        $X2SYS_HOME/TAG/TAG_paths.txt (if it exists). [If $X2SYS_HOME is not
        set it will default to $GMT_SHAREDIR/x2sys]. (**Note**: MGD77 files
        will also be looked for via $MGD77_HOME/mgd77_paths.txt and .gmt
        files will be searched for via $GMT_SHAREDIR/mgg/gmtfile_paths).

    outfile
        The file name for the output ASCII txt file to store the table in.
    tag : str
        Specify the x2sys TAG which identifies the attributes of this data
        type.

    combitable : str
        Only process the pair-combinations found in the file *combitable*
        [Default process all possible combinations among the specified files].
        The file *combitable* is created by :gmt-docs:`x2sys_get's -L option
        <supplements/x2sys/x2sys_get.html#l>`.

    runtimes : bool or str
        Compute and append the processing run-time for each pair to the
        progress message (use ``runtimes=True``). Pass in a file name (e.g.
        ``runtimes="file.txt"``) to save these run-times to file. The idea here
        is to use the knowledge of run-times to split the main process in a
        number of sub-processes that can each be launched in a different
        processor of your multi-core machine. See the MATLAB function
        `split_file4coes.m
        <https://github.com/GenericMappingTools/gmt/blob/master/src/x2sys/>`_.

    override : bool or str
        **S**\|\ **N**.
        Control how geographic coordinates are handled (Cartesian data are
        unaffected). By default, we determine if the data are closer to one
        pole than the other, and then we use a cylindrical polar conversion to
        avoid problems with longitude jumps. You can turn this off entirely
        with ``override`` and then the calculations uses the original data (we
        have protections against longitude jumps). However, you can force the
        selection of the pole for the projection by appending **S** or **N**
        for the south or north pole, respectively. The conversion is used
        because the algorithm used to find crossovers is inherently a
        Cartesian algorithm that can run into trouble with data that has large
        longitudinal range at higher latitudes.

    interpolation : str
        **l**\|\ **a**\|\ **c**.
        Sets the interpolation mode for estimating values at the crossover.
        Choose among:

        - **l** - Linear interpolation [Default].
        - **a** - Akima spline interpolation.
        - **c** - Cubic spline interpolation.

    coe : str
        Use **e** for external COEs only, and **i** for internal COEs only
        [Default is all COEs].

    {region}

    speed : str or list
        **l**\|\ **u**\|\ **h**\ *speed*.
        Defines window of track speeds. If speeds are outside this window we do
        not calculate a COE. Specify:

        - **l** sets lower speed [Default is 0].
        - **u** sets upper speed [Default is infinity].
        - **h** does not limit the speed but sets a lower speed below which
          headings will not be computed (i.e., set to NaN) [Default
          calculates headings regardless of speed].

        For example, you can use ``speed=["l0", "u10", "h5"]`` to set a lower
        speed of 0, upper speed of 10, and disable heading calculations for
        speeds below 5.

    {verbose}

    numpoints : int
        Give the maximum number of data points on either side of the crossover
        to use in the spline interpolation [Default is 3].

    trackvalues : bool
        Report the values of each track at the crossover [Default reports the
        crossover value and the mean value].

    Returns
    -------
    crossover_errors
        Table containing crossover error information. A :class:`pandas.DataFrame` object
        is returned if ``outfile`` is not set, otherwise ``None`` is returned and output
        will be stored in file set by ``outfile``.
    """
    # Determine output type based on 'outfile' parameter
    output_type = "pandas" if outfile is None else "file"

    file_contexts: list[contextlib.AbstractContextManager[Any]] = []
    for track in tracks:
        match data_kind(track):
            case "file":
                file_contexts.append(contextlib.nullcontext(track))
            case "matrix":
                # find suffix (-E) of trackfiles used (e.g. xyz, csv, etc) from
                # $X2SYS_HOME/TAGNAME/TAGNAME.tag file
                tagfile = Path(
                    os.environ["X2SYS_HOME"], kwargs["T"], f"{kwargs['T']}.tag"
                )
                # Last line is like "-Dxyz -Etsv -I1/1"
                lastline = tagfile.read_text(encoding="utf8").splitlines()[-1]
                for item in sorted(lastline.split()):  # sort list alphabetically
                    if item.startswith(("-E", "-D")):  # prefer -Etsv over -Dxyz
                        suffix = item[2:]  # e.g. tsv (1st choice) or xyz (2nd choice)

                # Save pandas.DataFrame track data to temporary file
                file_contexts.append(tempfile_from_dftrack(track=track, suffix=suffix))
            case _:
                raise GMTInvalidInput(f"Unrecognized data type: {type(track)}")

    with Session() as lib:
        with lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl:
            with contextlib.ExitStack() as stack:
                fnames = [stack.enter_context(c) for c in file_contexts]
                lib.call_module(
                    module="x2sys_cross",
                    args=build_arg_list(kwargs, infile=fnames, outfile=vouttbl),
                )
                result = lib.virtualfile_to_dataset(
                    vfname=vouttbl, output_type=output_type, header=2
                )

            if output_type == "file":
                return result

            # Convert 3rd and 4th columns to datetime/timedelta for pandas output.
            # These two columns have names "t_1"/"t_2" or "i_1"/"i_2".
            # "t_" means absolute datetimes and "i_" means dummy times.
            # Internally, they are all represented as double-precision numbers in GMT,
            # relative to TIME_EPOCH with the unit defined by TIME_UNIT.
            # In GMT, TIME_UNIT can be 'y' (year), 'o' (month), 'w' (week), 'd' (day),
            # 'h' (hour), 'm' (minute), 's' (second). Years are 365.2425 days and months
            # are of equal length.
            # pd.to_timedelta() supports unit of 'W'/'D'/'h'/'m'/'s'/'ms'/'us'/'ns'.
            match time_unit := lib.get_default("TIME_UNIT"):
                case "y":
                    unit = "s"
                    scale = 365.2425 * 86400.0
                case "o":
                    unit = "s"
                    scale = 365.2425 / 12.0 * 86400.0
                case "w" | "d" | "h" | "m" | "s":
                    unit = time_unit.upper() if time_unit in "wd" else time_unit
                    scale = 1.0

            columns = result.columns[2:4]
            result[columns] *= scale
            result[columns] = result[columns].apply(pd.to_timedelta, unit=unit)
            if columns[0][0] == "t":  # "t" or "i":
                result[columns] += pd.Timestamp(lib.get_default("TIME_EPOCH"))
            return result
