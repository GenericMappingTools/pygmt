"""
grdgradient - Compute directional gradients from a grid.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias

__doctest_skip__ = ["grdgradient"]


def _alias_option_N(  # noqa: N802
    normalize=False,
    norm_amp=None,
    norm_ambient=None,
    norm_sigma=None,
    norm_offset=None,
):
    """
    Helper function to create the alias list for the -N option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(N=_alias_option_N(**kwargs)).get("N")
    >>> parse(normalize=True)
    ''
    >>> parse(normalize="laplace")
    'e'
    >>> parse(normalize="cauchy")
    't'
    >>> parse(
    ...     normalize="laplace",
    ...     norm_amp=2,
    ...     norm_offset=10,
    ...     norm_sigma=0.5,
    ...     norm_ambient=0.1,
    ... )
    'e2+a0.1+s0.5+o10'
    >>> # Check for backward compatibility with old syntax
    >>> parse(normalize="e2+a0.2+s0.5+o10")
    'e2+a0.2+s0.5+o10'
    """
    _normalize_mapping = {"laplace": "e", "cauchy": "t"}
    # Check for old syntax for normalize
    if isinstance(normalize, str) and normalize not in _normalize_mapping:
        if any(
            v is not None and v is not False
            for v in [norm_amp, norm_ambient, norm_sigma, norm_offset]
        ):
            raise GMTParameterError(
                conflicts_with=(
                    "normalize",
                    ["norm_amp", "norm_ambient", "norm_sigma", "norm_offset"],
                ),
                reason="'normalize' is specified using the unrecommended GMT command string syntax.",
            )
        _normalize_mapping = None

    return [
        Alias(normalize, name="normalize", mapping=_normalize_mapping),
        Alias(norm_amp, name="norm_amp"),
        Alias(norm_ambient, name="norm_ambient", prefix="+a"),
        Alias(norm_sigma, name="norm_sigma", prefix="+s"),
        Alias(norm_offset, name="norm_offset", prefix="+o"),
    ]


@fmt_docstring
@use_alias(D="direction", Q="tiles", S="slope_file", f="coltypes", n="interpolation")
def grdgradient(  # noqa: PLR0913
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    azimuth: float | Sequence[float] | None = None,
    radiance: Sequence[float] | str | None = None,
    normalize: Literal["laplace", "cauchy"] | bool = False,
    norm_amp: float | None = None,
    norm_ambient: float | None = None,
    norm_sigma: float | None = None,
    norm_offset: float | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Compute directional gradients from a grid.

    Can accept ``azimuth``, ``direction``, and ``radiance`` input to create
    the resulting gradient.

    Full GMT docs at :gmt-docs:`grdgradient.html`.

    $aliases
       - A = azimuth
       - E = radiance
       - G = outgrid
       - R = region
       - V = verbose

    .. hlist::
       :columns: 1

       - N = normalize, norm_amp, **+a**: norm_ambient, **+s**: norm_sigma,
         **+o**: norm_offset

    Parameters
    ----------
    $grid
    $outgrid
    azimuth
        *azim* or (*azim*, *azim2*).
        Azimuthal direction for a directional derivative; *azim* is the angle in the x-y
        plane measured in degrees positive clockwise from north (the +y direction)
        toward east (the +x direction). The negative of the directional derivative,
        :math:`-(\frac{dz}{dx}\sin(\mbox{azim}) + \frac{dz}{dy}\cos(\mbox{azim}))`, is
        found; negation yields positive values when the slope of :math:`z(x,y)` is
        downhill in the *azim* direction, the correct sense for shading the illumination
        of an image by (see :meth:`pygmt.Figure.grdimage` and
        :meth:`pygmt.Figure.grdview`) a light source above the x-y plane shining from
        the *azim* direction. Optionally, supply two azimuths, (*azim*, *azim2*), in
        which case the gradients in each of these directions are calculated and the one
        larger in magnitude is retained; this is useful for illuminating data with two
        directions of lineated structures, e.g., ``(0, 270)`` illuminates from the north
        (top) and west (left). Finally, if *azim* is a file it must be a grid of the
        same domain, spacing and registration as *grid* that will update the azimuth at
        each output node when computing the directional derivatives.
    direction : str
        [**a**][**c**][**o**][**n**].
        Find the direction of the positive (up-slope) gradient of the data.
        The following options are supported:

        - **a**: Find the aspect (i.e., the down-slope direction)
        - **c**: Use the conventional Cartesian angles measured
          counterclockwise from the positive x (east) direction.
        - **o**: Report orientations (0-180) rather than directions (0-360).
        - **n**: Add 90 degrees to all angles (e.g., to give local strikes of
          the surface).
    radiance
        (*azim*, *elev*) or [**m**\|\ **s**\|\ **p**]\ *azim/elev*\ [**+a**\ *ambient*]
        [**+d**\ *diffuse*][**+p**\ *specular*][**+s**\ *shine*].
        Compute Lambertian radiance appropriate to use with
        :meth:`pygmt.Figure.grdimage` and :meth:`pygmt.Figure.grdview`. The
        Lambertian Reflection assumes an ideal surface that reflects all the
        light that strikes it and the surface appears
        equally bright from all viewing directions. Here, *azim* and *elev* are
        the azimuth and elevation of the light vector. Optionally, supply
        *ambient* [0.55], *diffuse* [0.6], *specular* [0.4], or *shine* [10],
        which are parameters that control the reflectance properties of the
        surface. Default values are given in the brackets. Use **s** for a
        simpler Lambertian algorithm. Note that with this form you only have
        to provide azimuth and elevation. Alternatively, use **p** for
        the Peucker piecewise linear approximation (simpler but faster
        algorithm; in this case *azim* and *elev* are hardwired to 315
        and 45 degrees. This means that even if you provide other values
        they will be ignored.).
    normalize
        Normalize the output gradients. Valid values are:

        - ``False``: No normalization is done [Default].
        - ``True``: Normalize using max absolute value.
        - ``"laplace"``: Normalize using cumulative Laplace distribution.
        - ``"cauchy"``: Normalize using cumulative Cauchy distribution.

        The normalization process is controlled via the additional parameters
        ``norm_amp``, ``norm_ambient``, ``norm_sigma``, and ``norm_offset``.

        Let :math:`g` denote the actual gradients, :math:`g_n` the normalized gradients,
        :math:`a` the maximum output magnitude (``norm_amp``), :math:`o` the offset
        value (``norm_offset``), and :math:`\sigma` the sigma value (``norm_sigma``).
        The normalization is computed as follows:

        - ``True``: :math:`g_n = a (\frac{g - o}{\max(|g - o|)})`
        - ``"laplace"``: :math:`g_n = a(1 - \exp(\sqrt{2}\frac{g - o}{\sigma}))`
        - ``"cauchy"``: :math:`g_n = \frac{2a}{\pi}\arctan(\frac{g - o}{\sigma})`
    norm_amp
        Set the maximum output magnitude [Default is 1].
    norm_ambient
        The ambient value to add to all nodes after gradient calculations are completed
        [Default is 0].
    norm_offset
        The offset value used in the normalization. If not given, it is set to the
        average of :math:`g`.
    norm_sigma
        The *sigma* value used in the Laplace or Cauchy normalization. If not given,
        it is estimated from the L1 norm of :math:`g-o` for Laplace or the L2 norm of
        :math:`g-o` for Cauchy.
    tiles : str
        **c**\|\ **r**\|\ **R**.
        Control how normalization via ``normalize`` is carried out. When
        multiple grids should be normalized the same way (i.e., with the same
        *offset* and/or *sigma*),
        we must pass these values via ``normalize``. However, this is
        inconvenient if we compute these values from a grid. Use **c** to
        save the results of *offset* and *sigma* to a statistics file; if
        grid output is not needed for this run then do not specify
        ``outgrid``. For subsequent runs, just use **r** to read these
        values. Using **R** will read then delete the statistics file.
    slope_file : str
        Name of output grid file with scalar magnitudes of gradient vectors.
        Requires ``direction`` but makes ``outgrid`` optional.
    $region
    $verbose
    $coltypes
    $interpolation

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a new grid from an input grid, set the azimuth to 10 degrees,
    >>> new_grid = pygmt.grdgradient(grid=grid, azimuth=10)
    """
    if kwargs.get("Q") is not None and kwargs.get("N") is None:
        raise GMTParameterError(
            required="normalize", reason="Required when 'tiles' is set."
        )
    if (
        kwargs.get("A", azimuth) is None
        and kwargs.get("D") is None
        and kwargs.get("E", radiance) is None
    ):
        raise GMTParameterError(at_least_one=["azimuth", "direction", "radiance"])

    aliasdict = AliasSystem(
        A=Alias(azimuth, name="azimuth", sep="/", size=2),
        E=Alias(radiance, name="radiance", sep="/", size=2),
        N=_alias_option_N(
            normalize=normalize,
            norm_amp=norm_amp,
            norm_ambient=norm_ambient,
            norm_sigma=norm_sigma,
            norm_offset=norm_offset,
        ),
    ).add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdgradient", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
