"""
x2sys_init - Initialize a new x2sys track database.
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


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
    r"""
    Initialize a new x2sys track database.

    Serves as the starting point for x2sys and initializes a set of data bases
    that are particular to one kind of track data. These data, their associated
    data bases, and key parameters are given a short-hand notation called an
    x2sys TAG. The TAG keeps track of settings such as file format, whether the
    data are geographic or not, and the binning resolution for track indices.

    Before you can run :meth:`pygmt.x2sys_init` you must set the environmental
    parameter X2SYS_HOME to a directory where you have write permission, which
    is where x2sys can keep track of your settings.

    Full option list at :gmt-docs:`supplements/x2sys/x2sys_init.html`

    {aliases}

    Parameters
    ----------
    tag : str
        The unique name of this data type x2sys TAG.

    fmtfile : str
        Format definition file prefix for this data set (see
        :gmt-docs:`GMT's Format Definition Files
        <supplements/x2sys/x2sys_init.html#format-definition-files>`
        for more information). Specify full path if the file is not in the
        current directory.

        Some file formats already have definition files premade. These include:

        - **mgd77** (for plain ASCII MGD77 data files)
        - **mgd77+** (for enhanced MGD77+ netCDF files)
        - **gmt** (for old mgg supplement binary files)
        - **xy** (for plain ASCII x, y tables)
        - **xyz** (same, with one z-column)
        - **geo** (for plain ASCII longitude, latitude files)
        - **geoz** (same, with one z-column).

    suffix : str
        Specifies the file extension (suffix) for these data files. If not
        given we use the format definition file prefix as the suffix (see
        ``fmtfile``).

    discontinuity : str
        **d**\|\ **g**.
        Selects geographical coordinates. Append **d** for discontinuity at the
        Dateline (makes longitude go from -180 to +180) or **g** for
        discontinuity at Greenwich (makes longitude go from 0 to 360
        [Default]). If not given we assume the data are Cartesian.

    spacing : str or list
         *dx*\[/*dy*].
         *dx* and optionally *dy* is the grid spacing. Append **m** to
         indicate minutes or **s** to indicate seconds for geographic data.
         These spacings refer to the binning used in the track bin-index data
         base.

    units : str or list
        **d**\|\ **s**\ *unit*.
        Sets the units used for distance and speed when requested by other
        programs. Append **d** for distance or **s** for speed, then give the
        desired *unit* as:

        - **c** - Cartesian userdist or userdist/usertime
        - **e** - meters or m/s
        - **f** - feet or feet/s
        - **k** - km or km/hr
        - **m** - miles or miles/hr
        - **n** - nautical miles or knots
        - **u** - survey feet or survey feet/s

        [Default is ``units=["dk", "se"]`` (km and m/s) if ``discontinuity`` is
        set, and ``units=["dc", "sc"]`` otherwise (e.g., for Cartesian units)].

    {R}
    {V}

    gap : str or list
        **t**\|\ **d**\ *gap*.
        Give **t** or **d** and append the corresponding maximum time gap (in
        user units; this is typically seconds [Default is infinity]), or
        distance (for units, see ``units``) gap [Default is infinity]) allowed
        between the two data points immediately on either side of a crossover.
        If these limits are exceeded then a data gap is assumed and no COE will
        be determined.

    {j}
    """
    with Session() as lib:
        arg_str = " ".join([tag, build_arg_string(kwargs)])
        lib.call_module(module="x2sys_init", args=arg_str)
