"""
grdtrack - Sample grids at specified (x,y) locations.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="resample",
    C="crossprofile",
    D="dfile",
    E="profile",
    F="critical",
    R="region",
    N="no_skip",
    S="stack",
    T="radius",
    V="verbose",
    Z="z_only",
    f="coltypes",
    i="incols",
    j="distcalc",
    n="interpolation",
)
@kwargs_to_strings(R="sequence", S="sequence")
def grdtrack(points, grid, newcolname=None, outfile=None, **kwargs):
    r"""
    Sample grids at specified (x,y) locations.

    Reads one or more grid files and a table (from file or an array input; but
    see ``profile`` for exception) with (x,y) [or (lon,lat)] positions in the
    first two columns (more columns may be present). It interpolates the
    grid(s) at the positions in the table and writes out the table with the
    interpolated values added as (one or more) new columns. Alternatively
    (``crossprofile``), the input is considered to be line-segments and we
    create orthogonal cross-profiles at each data point or with an equidistant
    separation and sample the grid(s) along these profiles. A bicubic
    [Default], bilinear, B-spline or nearest-neighbor interpolation is used,
    requiring boundary conditions at the limits of the region (see
    ``interpolation``; Default uses "natural" conditions (second partial
    derivative normal to edge is zero) unless the grid is automatically
    recognized as periodic.)

    Full option list at :gmt-docs:`grdtrack.html`

    {aliases}

    Parameters
    ----------
    points : str or {table-like}
        Pass in either a file name to an ASCII data table, a 2D
        {table-classes}.

    grid : xarray.DataArray or str
        Gridded array from which to sample values from, or a filename (netcdf
        format).

    newcolname : str
        Required if ``points`` is a :class:`pandas.DataFrame`. The name for the
        new column in the track :class:`pandas.DataFrame` table where the
        sampled values will be placed.

    outfile : str
        The file name for the output ASCII file.

    resample : str
        **f**\|\ **p**\|\ **m**\|\ **r**\|\ **R**\ [**+l**]
        For track resampling (if ``crossprofile`` or ``profile`` are set) we
        can select how this is to be performed. Append **f** to keep original
        points, but add intermediate points if needed [Default], **m** as
        **f**, but first follow meridian (along y) then parallel (along x),
        **p** as **f**, but first follow parallel (along y) then meridian
        (along x), **r** to resample at equidistant locations; input points are
        not necessarily included in the output, and **R** as **r**, but adjust
        given spacing to fit the track length exactly. Finally, append
        **+l** if geographic distances should be measured along rhumb lines
        (loxodromes) instead of great circles. Ignored unless ``crossprofile``
        is used.
    crossprofile : str
        *length*/\ *ds*\ [*/spacing*][**+a**\|\ **+v**][**l**\|\ **r**].
        Use input line segments to create an equidistant and (optionally)
        equally-spaced set of crossing profiles along which we sample the
        grid(s) [Default simply samples the grid(s) at the input locations].
        Specify two length scales that control how the sampling is done:
        *length* sets the full length of each cross-profile, while *ds* is
        the sampling spacing along each cross-profile. Optionally, append
        **/**\ *spacing* for an equidistant spacing between cross-profiles
        [Default erects cross-profiles at the input coordinates]; see
        ``resample`` for how resampling the input track is controlled. By
        default, all cross-profiles have the same direction (left to right
        as we look in the direction of the input line segment). Append **+a**
        to alternate the direction of cross-profiles, or **v** to enforce
        either a "west-to-east" or "south-to-north" view. By default the entire
        profiles are output. Choose to only output the left or right halves
        of the profiles by appending **+l** or **+r**, respectively.  Append
        suitable units to *length*; it sets the unit used for *ds* [and
        *spacing*] (See :gmt-docs:`Units <grdtrack.html#units>`). The default
        unit for geographic grids is meter while Cartesian grids implies the
        user unit.  The output columns will be *lon*, *lat*, *dist*, *azimuth*,
        *z1*, *z2*, ..., *zn* (The *zi* are the sampled values for each of the
        *n* grids).
    dfile : str
        In concert with ``crossprofile`` we can save the (possibly resampled)
        original lines to *dfile* [Default only saves the cross-profiles]. The
        columns will be *lon*, *lat*, *dist*, *azimuth*, *z1*, *z2*, ...
        (sampled value for each grid).
    profile : str
        *line*\ [,\ *line*,...][**+a**\ *az*][**+c**][**+d**][**+g**]\
        [**+i**\ *inc*][**+l**\ *length*][**+n**\ *np*][**+o**\ *az*]\
        [**+r**\ *radius*].
        Instead of reading input track coordinates, specify profiles via
        coordinates and modifiers. The format of each *line* is
        *start*/*stop*, where *start* or *stop* are either *lon*/*lat* (*x*/*y*
        for Cartesian data) or a 2-character XY key that uses the
        :gmt-docs:`text <text.html>`-style justification format to specify
        a point on the map as [LCR][BMT]. Each line will be a separate segment
        unless **+c** is used which will connect segments with shared joints
        into a single segment. In addition to line coordinates, you can use Z-,
        Z+ to mean the global minimum and maximum locations in the grid (only
        available if a single grid is given via **outfile**). You may append
        **+i**\ *inc* to set the sampling interval; if not given then we
        default to half the minimum grid interval. For a *line* along parallels
        or meridians you can add **+g** to report degrees of longitude or
        latitude instead of great circle distances starting at zero. Instead of
        two coordinates you can specify an origin and one of **+a**, **+o**, or
        **+r**. The **+a** sets the azimuth of a profile of given length
        starting at the given origin, while **+o** centers the profile on the
        origin; both require **+l**. For circular sampling specify **+r** to
        define a circle of given radius centered on the origin; this option
        requires either **+n** or **+i**.  The **+n**\ *np* modifier sets the
        desired number of points, while **+l**\ *length* gives the total length
        of the profile. Append **+d** to output the along-track distances after
        the coordinates. **Note**: No track file will be read. Also note that
        only one distance unit can be chosen. Giving different units will
        result in an error. If no units are specified we default to great
        circle distances in km (if geographic). If working with geographic data
        you can use ``distcalc`` to control distance calculation mode [Default
        is Great Circle]. **Note**: If ``crossprofile`` is set and *spacing* is
        given then that sampling scheme overrules any modifier set in
        ``profile``.
    critical : str
        [**+b**][**+n**][**+r**][**+z**\ *z0*].
        Find critical points along each cross-profile as a function of
        along-track distance. Requires ``crossprofile`` and a single input grid
        (*z*). We examine each cross-profile generated and report (*dist*,
        *lonc*, *latc*, *distc*, *azimuthc*, *zc*) at the center peak of
        maximum *z* value, (*lonl*, *latl*, *distl*) and (*lonr*, *latr*,
        *distr*) at the first and last non-NaN point whose *z*-value exceeds
        *z0*, respectively, and the *width* based on the two extreme points
        found. Here, *dist* is the distance along the original input
        ``points`` and the other 12 output columns are a function of that
        distance.  When searching for the center peak and the extreme first and
        last values that exceed the threshold we assume the profile is positive
        up. If we instead are looking for a trough then you must use **+n** to
        temporarily flip the profile to positive. The threshold *z0* value is
        always given as >= 0; use **+z** to change it [Default is 0].
        Alternatively, use **+b** to determine the balance point and standard
        deviation of the profile; this is the weighted mean and weighted
        standard deviation of the distances, with *z* acting as the weight.
        Finally, use **+r** to obtain the weighted rms about the cross-track
        center (*distc* == 0). **Note**: We round the exact results to the
        nearest distance nodes along the cross-profiles. We write 13 output
        columns per track: *dist, lonc, latc, distc, azimuthc, zc, lonl, latl,
        distl, lonr, latr, distr, width*.
    {R}
    no_skip : bool
        Do *not* skip points that fall outside the domain of the grid(s)
        [Default only output points within grid domain].
    stack : str or list
        *method*/*modifiers*.
        In conjunction with ``crossprofile``, compute a single stacked profile
        from all profiles across each segment. Choose how stacking should be
        computed [Default method is **a**]:

        - **a** = mean (average)
        - **m** = median
        - **p** = mode (maximum likelihood)
        - **l** = lower
        - **L** = lower but only consider positive values
        - **u** = upper
        - **U** = upper but only consider negative values.

        The *modifiers* control the output; choose one or more among these
        choices:

        - **+a** : Append stacked values to all cross-profiles.
        - **+d** : Append stack deviations to all cross-profiles.
        - **+r** : Append data residuals (data - stack) to all cross-profiles.
        - **+s**\ [*file*] : Save stacked profile to *file* [Default filename
          is grdtrack_stacked_profile.txt].
        - **+c**\ *fact* : Compute envelope on stacked profile as
          ±\ *fact* \*\ *deviation* [Default fact value is 2].

        Notes:

        1. Deviations depend on *method* and are st.dev (**a**), L1 scale,
           i.e., 1.4826 \* median absolute deviation (MAD) (for **m** and
           **p**), or half-range (upper-lower)/2.
        2. The stacked profile file contains a leading column plus groups of
           4-6 columns, with one group for each sampled grid. The leading
           column holds cross distance, while the first four columns in a group
           hold stacked value, deviation, min value, and max value,
           respectively. If *method* is one of **a**\|\ **m**\|\ **p** then we
           also write the lower and upper confidence bounds (see **+c**). When
           one or more of **+a**, **+d**, and **+r** are used then we also
           append the stacking results to the end of each row, for all
           cross-profiles. The order is always stacked value (**+a**), followed
           by deviations (**+d**) and finally residuals (**+r**). When more
           than one grid is sampled this sequence of 1-3 columns is repeated
           for each grid.
    radius : bool or int or float or str
        [*radius*][**+e**\|\ **p**].
        To be used with normal grid sampling, and limited to a single, non-IMG
        grid. If the nearest node to the input point is NaN, search outwards
        until we find the nearest non-NaN node and report that value instead.
        Optionally specify a search radius which limits the consideration to
        points within this distance from the input point. To report the
        location of the nearest node and its distance from the input point,
        append **+e**. The default unit for geographic grid distances is
        spherical degrees. Use *radius* to change the unit and give *radius* =
        0 if you do not want to limit the radius search. To instead replace the
        input point with the coordinates of the nearest node, append **+p**.
    {V}
    z_only : bool
        Only write out the sampled z-values [Default writes all columns].
    {f}
    {i}
    {j}
    {n}

    Returns
    -------
    track: pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, ..., newcolname) if
          ``outfile`` is not set
        - None if ``outfile`` is set (track output will be stored in file set
          by ``outfile``)
    """
    if hasattr(points, "columns") and newcolname is None:
        raise GMTInvalidInput("Please pass in a str to 'newcolname'")

    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(check_kind="vector", data=points)
            # Store the xarray.DataArray grid in virtualfile
            grid_context = lib.virtualfile_from_data(check_kind="raster", data=grid)

            # Run grdtrack on the temporary (csv) points table
            # and (netcdf) grid virtualfile
            with table_context as csvfile:
                with grid_context as grdfile:
                    kwargs.update({"G": grdfile})
                    if outfile is None:  # Output to tmpfile if outfile is not set
                        outfile = tmpfile.name
                    arg_str = " ".join(
                        [csvfile, build_arg_string(kwargs), "->" + outfile]
                    )
                    lib.call_module(module="grdtrack", args=arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            try:
                column_names = points.columns.to_list() + [newcolname]
                result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)
            except AttributeError:  # 'str' object has no attribute 'columns'
                result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

    return result
