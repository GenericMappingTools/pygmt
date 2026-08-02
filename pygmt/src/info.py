"""
info - Get information about data tables.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import GMTTempFile, build_arg_list, fmt_docstring, use_alias


@fmt_docstring
@use_alias(T="nearest_multiple", a="aspatial", f="coltypes")
def info(
    data: PathLike | TableLike,
    spacing: Sequence[float] | str | None = None,
    per_column: bool = False,
    incols: int | str | Sequence[int | str] | None = None,
    registration: Literal["gridline", "pixel"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> np.ndarray | str:
    r"""
    Get information about data tables.

    Reads from files and finds the extreme values in each of the columns
    reported as min/max pairs. It recognizes NaNs and will print warnings if
    the number of columns vary from record to record. As an option, it will
    find the extent of the first two columns rounded up and down to the nearest
    multiple of the supplied increments given by ``spacing``. Such output will
    be in a :class:`numpy.ndarray` form [*w*, *e*, *s*, *n*], which can be used
    directly as the ``region`` parameter for other modules (hence only *dx*
    and *dy* are needed). If the ``per_column`` parameter is combined with
    ``spacing``, then the :class:`numpy.ndarray` output will be rounded up/down for as
    many columns as there are increments provided in ``spacing``. A similar
    parameter ``nearest_multiple`` will provide a :class:`numpy.ndarray` in the form
    of [*zmin*, *zmax*, *dz*] for makecpt.

    Full GMT docs at :gmt-docs:`gmtinfo.html`.

    $aliases
       - C = per_column
       - I = spacing
       - V = verbose
       - i = incols
       - r = registration

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a 1-D/2-D
        $table_classes.
    per_column
        Report the min/max values per column in separate columns [Default is the format
        <min/max>].
    spacing
        [**b**\|\ **p**\|\ **f**\|\ **s**]\ *dx*\[/*dy*\[/*dz*...]].
        Compute the min/max values of the first n columns to the nearest
        multiple of the provided increments [default is 2 columns]. By default,
        output results in the form ``[w, e, s, n]``, unless ``per_column`` is
        set in which case we output each min and max value in separate output
        columns.
    nearest_multiple : str
        **dz**\[\ **+c**\ *col*].
        Report the min/max of the first (0'th) column to the nearest multiple
        of dz and output this in the form ``[zmin, zmax, dz]``.
    $verbose
    $aspatial
    $coltypes
    $incols
    $registration

    Returns
    -------
    output : :class:`numpy.ndarray` or str
        Return type depends on whether any of the ``per_column``,
        ``spacing``, or ``nearest_multiple`` parameters are set.

        - :class:`numpy.ndarray` if either of the above parameters are used.
        - str if none of the above parameters are used.
    """
    aliasdict = AliasSystem(
        C=Alias(per_column, name="per_column"),
        I=Alias(spacing, name="spacing", sep="/"),
    ).add_common(
        V=verbose,
        i=incols,
        r=registration,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with GMTTempFile() as tmpfile:
            with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
                lib.call_module(
                    module="info",
                    args=build_arg_list(aliasdict, infile=vintbl, outfile=tmpfile.name),
                )
            result = tmpfile.read()

        if (
            kwargs.get("C", per_column) is not False
            or kwargs.get("I", spacing) is not None
            or kwargs.get("T") is not None
        ):
            # Converts certain output types into a numpy array
            # instead of a raw string that is less useful.
            if result.startswith(("-R", "-T")):  # e.g. -R0/1/2/3 or -T0/9/1
                result = result[2:].replace("/", " ")
            try:
                result = np.loadtxt(result.splitlines())
            except ValueError:
                # Load non-numerical outputs in str type, e.g. for datetime
                result = np.loadtxt(result.splitlines(), dtype=np.str_)

        return result
