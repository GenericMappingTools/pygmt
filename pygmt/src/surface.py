"""
surface - Grid table data using adjustable tension continuous curvature splines.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["surface"]


@fmt_docstring
@use_alias(
    C="convergence",
    I="spacing",
    Ll="lower",
    Lu="upper",
    M="maxradius",
    R="region",
    T="tension",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence")
def surface(
    data=None, x=None, y=None, z=None, outgrid: str | None = None, **kwargs
) -> xr.DataArray | None:
    r"""
    Grid table data using adjustable tension continuous curvature splines.

    Surface reads randomly-spaced (x, y, z) triplets and produces gridded
    values z(x,y) by solving:

    .. math::    (1 - t)\nabla^2(z)+t\nabla(z) = 0

    where :math:`t` is a tension factor between 0 and 1, and :math:`\nabla`
    indicates the Laplacian operator. Here, :math:`t = 0` gives the
    "minimum curvature" solution. Minimum curvature can cause undesired
    oscillations and false local maxima or minima (see Smith and Wessel,
    1990), and you may wish to use :math:`t > 0` to suppress these effects.
    Experience suggests :math:`t \sim 0.25` usually looks good for potential
    field data and t should be larger (:math:`t \sim 0.35`) for steep
    topography data. :math:`t = 1` gives a harmonic surface (no maxima or
    minima are possible except at control data points). It is recommended that
    the user preprocess the data with :func:`pygmt.blockmean`,
    :func:`pygmt.blockmedian`, or :func:`pygmt.blockmode` to avoid spatial
    aliasing and eliminate redundant data. You may impose lower and/or upper
    bounds on the solution. These may be entered in the form of a fixed value,
    a grid with values, or simply be the minimum/maximum input data values.
    Natural boundary conditions are applied at the edges, except for
    geographic data with 360-degree range where we apply periodic boundary
    conditions in the longitude direction.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`surface.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    {region}
    {outgrid}
    convergence : float
        Optional. Convergence limit. Iteration is assumed to have converged
        when the maximum absolute change in any grid value is less than
        ``convergence``. (Units same as data z units). Alternatively,
        give limit in percentage of root-mean-square (rms) deviation by
        appending %. [Default is scaled to :math:`10^{{-4}}` of the rms
        deviation of the data from a best-fit (least-squares) plane.]
        This is the final convergence limit at the desired grid spacing;
        for intermediate (coarser) grids the effective convergence limit is
        divided by the grid spacing multiplier.
    maxradius : float or str
        Optional. After solving for the surface, apply a mask so that nodes
        farther than ``maxradius`` away from a data constraint are set to NaN
        [Default is no masking]. Append a distance unit (see
        :gmt-docs:`Units <surface.html#units>`) if needed. One can also
        select the nodes to mask by using the *n_cells*\ **c** form. Here
        *n_cells* means the number of cells around the node is controlled
        by a data point. As an example ``"0c"`` means that only the cell
        where the point lies is filled, ``"1c"`` keeps one cell beyond
        that (i.e. makes a 3x3 square neighborhood), and so on.
    lower : float or str
        Optional. Impose limits on the output solution. Parameter ``lower``
        sets the lower bound. ``lower`` can be the name of a grid file with
        lower bound values, a fixed value, **d** to set to minimum input
        value, or **u** for unconstrained [Default]. Grid files used to set
        the limits may contain NaNs. In the presence of NaNs, the limit of
        a node masked with NaN is unconstrained.
    upper : float or str
        Optional. Impose limits on the output solution. Parameter ``upper``
        sets the upper bound and can be the name of a grid file with upper
        bound values, a fixed value, **d** to set to maximum input value,
        or **u** for unconstrained [Default]. Grid files used to set the
        limits may contain NaNs. In the presence of NaNs, the limit of a
        node masked with NaN is unconstrained.
    tension : float or str
        [**b**\|\ **i**].
        Optional. Tension factor[s]. These must be between 0 and 1. Tension
        may be used in the interior solution (above equation, where it
        suppresses spurious oscillations) and in the boundary conditions
        (where it tends to flatten the solution approaching the edges). Add
        **i**\ *tension* to set interior tension, and **b**\ *tension* to
        set boundary tension. If you do not prepend **i** or **b**, both
        will be set to the same value. [Default is 0 for both and gives
        minimum curvature solution.]
    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {registration}
    {wrap}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a sample table of topography
    >>> topography = pygmt.datasets.load_sample_data(name="notre_dame_topography")
    >>> # Perform gridding of topography data
    >>> grid = pygmt.surface(data=topography, spacing=1, region=[0, 4, 0, 8])
    """
    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
            ) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="surface", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
