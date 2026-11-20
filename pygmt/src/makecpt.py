"""
makecpt - Make GMT color palette tables.
"""

from collections.abc import Sequence
from contextlib import nullcontext
from typing import Literal

import numpy as np
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTParameterError
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    is_nonstr_iter,
    sequence_join,
    use_alias,
)


def _explicit_series(series) -> np.ndarray:
    """
    Convert explicit color slice boundaries to a single column of doubles.
    """
    values = np.asanyarray(series)
    if values.ndim != 1:
        msg = "Parameter 'series' must be one-dimensional."
        raise GMTInvalidInput(msg)
    if isinstance(values, np.ma.MaskedArray):
        values = values.compressed()
    if values.size < 2:
        msg = "Parameter 'series' must provide at least two unmasked boundaries."
        raise GMTInvalidInput(msg)

    msg = "Explicit color slice boundaries must be finite real numbers."
    # NumPy can coerce complex and time scalars in object arrays to doubles.
    if values.dtype.kind not in "biufOSU" or (
        values.dtype.kind == "O"
        and any(
            isinstance(
                value, complex | np.complexfloating | np.datetime64 | np.timedelta64
            )
            for value in values
        )
    ):
        raise GMTInvalidInput(msg)
    try:
        boundaries = values.astype(np.float64, copy=False)
    except (TypeError, ValueError, OverflowError) as error:
        raise GMTInvalidInput(msg) from error
    if not np.isfinite(boundaries).all():
        raise GMTInvalidInput(msg)
    return boundaries


@fmt_docstring
@use_alias(
    A="transparency",
    D="background",
    F="color_model",
    H="output",
    I="reverse",
    T="series",
    W="categorical",
    Ww="cyclic",
)
def makecpt(
    cmap: str | bool = False,
    truncate: Sequence[float] | None = None,
    overrule_bg: bool = False,
    no_bg: bool = False,
    log: bool = False,
    continuous: bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Make GMT color palette tables.

    This function will help you to make static color palette tables (CPTs).
    By default, the CPT will be saved as the current CPT of the session,
    figure, subplot, panel, or inset depending on which level
    :func:`pygmt.makecpt` is called (for details on how GMT modern mode
    maintains different levels of colormaps please see
    :gmt-docs:`reference/features.html#gmt-modern-mode-hierarchical-levels`).
    You can use ``output`` to save the CPT to a file.
    You define an equidistant
    set of contour intervals or pass your own z-table or list, and create a new
    CPT based on an existing master (dynamic) CPT. The resulting CPT can be
    reversed relative to the master cpt, and can be made continuous or
    discrete. For color tables beyond the standard GMT offerings, visit
    `cpt-city <https://phillips.shef.ac.uk/pub/cpt-city/>`_ and
    `Scientific Colour-Maps <https://www.fabiocrameri.ch/colourmaps.php>`_.

    The CPT includes three additional colors beyond the range of z-values.
    These are the background color (B) assigned to values lower than the lowest
    *z*-value, the foreground color (F) assigned to values higher than the
    highest *z*-value, and the NaN color (N) painted wherever values are
    undefined.

    If the master CPT includes B, F, and N entries, these will be copied into
    the new master file. If not, the parameters :gmt-term:`COLOR_BACKGROUND`,
    :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` from the
    :gmt-docs:`gmt.conf <gmt.conf>` file will be used. This
    default behavior can be overruled using the parameters ``background``,
    ``overrule_bg`` or ``no_bg``.

    The color model (RGB, HSV or CMYK) of the palette created by
    :func:`pygmt.makecpt` will be the same as specified in the header of the
    master CPT. When there is no :gmt-term:`COLOR_MODEL` entry in the
    master CPT, the :gmt-term:`COLOR_MODEL` specified in the
    :gmt-docs:`gmt.conf <gmt.conf>` file will be used.

    Full GMT docs at :gmt-docs:`makecpt.html`.

    $aliases
       - C = cmap
       - G = truncate
       - M = overrule_bg
       - N = no_bg
       - Q = log
       - V = verbose
       - Z = continuous

    Parameters
    ----------
    transparency : float or str
        Set a constant level of transparency (0-100) for all color slices. Append **+a**
        to also affect the foreground, background, and NaN colors [Default is no
        transparency, i.e., ``0`` (opaque)].
    cmap : str
        Select the master color palette table (CPT) to use in the
        interpolation. Full list of built-in color palette tables can be found
        at :gmt-docs:`reference/cpts.html#built-in-color-palette-tables-cpt`.
    background : bool or str
        Select the back- and foreground colors to match the colors for lowest
        and highest *z*-values in the output CPT [Default (``background=True``
        or ``background="o"``) uses the colors specified in the master file, or
        those defined by the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN`]. Use
        ``background="i"`` to match the colors for the lowest and highest
        values in the input (instead of the output) CPT.
    color_model : str
        [**R**\|\ **r**\|\ **h**\|\ **c**]\
        [**+c**\ [*label*\|\ *start*\ [**-**]]].
        Force output CPT to be written with r/g/b codes, gray-scale values or
        color name (**R**, default) or r/g/b codes only (**r**), or h-s-v codes
        (**h**), or c/m/y/k codes (**c**).  Optionally or alternatively, append
        **+c** to write discrete palettes in categorical format. If *label* is
        appended then we create labels for each category to be used when the
        CPT is plotted. The *label* may be a comma-separated list of category
        names (you can skip a category by not giving a name), or give
        *start*, where we automatically build monotonically increasing
        labels from *start* (a single letter or an integer). Additionally
        append **-** to build ranges *start*-*start+1* as labels instead.
    series : str or array-like
        [*min/max/inc*\ [**+b**\|\ **l**\|\ **n**]\|\ *file*\|\ *list*].
        A two-value sequence specifies *min* and *max*. A three-value sequence
        adds *inc*. A one-dimensional sequence of four or more finite real
        numbers specifies the boundaries directly. For example,
        ``series=[0, 0.25, 0.9, 2]`` creates three color slices. Masked entries
        are skipped when reading explicit boundaries. A string can contain a
        file name, GMT's range syntax, or a comma-separated list of boundaries.
        Use GMT's string syntax to specify two or three explicit boundaries or
        a list of absolute times.
        If ``series`` is omitted, use the range of the master CPT. The **+n**
        modifier sets the number of boundaries, which is one more than the
        number of color slices. For details on array creation, see
        :gmt-docs:`makecpt.html#generate-1d-array`.
    truncate
        (*zlow*, *zhigh*).
        Truncate the incoming CPT so that the lowest and highest z-levels are to *zlow*
        and *zhigh*. If one of these equals NaN, then we leave that end of the CPT
        alone. The truncation takes place before any resampling. See also
        :gmt-docs:`reference/features.html#manipulating-cpts`.
    output : str
        Optional. The file name with extension .cpt to store the generated CPT
        file. If not given or ``False`` [Default], saves the CPT as the current
        CPT of the session, figure, subplot, panel, or inset depending on which
        level :func:`pygmt.makecpt` is called.
    reverse : str
        Set this to ``True`` or **c** [Default] to reverse the sense of color
        progression in the master CPT. Also the foreground and background colors
        are exchanged, including those specified by :gmt-term:`COLOR_BACKGROUND` and
        :gmt-term:`COLOR_FOREGROUND`. Set this to **z** to reverse the sign of z-values
        in the color table. Note that this change of the z-direction happens before
        the ``truncate`` and ``series`` values are used, so the latter must be
        compatible with the changed z-range. See also
        :gmt-docs:`reference/features.html#manipulating-cpts`.
    overrule_bg
        Overrule background, foreground, and NaN colors specified in the master CPT with
        the values of the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` specified in the
        :gmt-docs:`gmt.conf <gmt.conf>` file or by :func:`pygmt.config`. When combined
        with ``background``, only :gmt-term:`COLOR_NAN` is considered.
    no_bg
        Do not write out the background, foreground, and NaN-color fields [Default will
        write them, i.e. ``no_bg=False``].
    log
        For logarithmic interpolation scheme with input given as logarithms. Expects
        input z-values provided via ``series`` to be log10(*z*), assigns colors, and
        writes out *z*.
    continuous
        Force a continuous CPT when building from a list of colors and a list of
        z-values [Default is False, i.e. discrete CPT].
    categorical : bool
        Do not interpolate the input color table but pick the output colors
        starting at the beginning of the color table, until colors for all
        intervals are assigned. This is particularly useful in combination with
        a categorical color table, like ``cmap="gmt/categorical"``.
    cyclic : bool
        Produce a wrapped (cyclic) color table that endlessly repeats its
        range. Note that ``cyclic=True`` cannot be set together with
        ``categorical=True``.
    $verbose
    """
    if kwargs.get("W") is not None and kwargs.get("Ww") is not None:
        raise GMTParameterError(at_most_one=["categorical", "cyclic"])

    if (output := kwargs.pop("H", None)) is not None:
        kwargs["H"] = True

    aliasdict = AliasSystem(
        C=Alias(cmap, name="cmap"),
        G=Alias(truncate, name="truncate", sep="/", size=2),
        M=Alias(overrule_bg, name="overrule_bg"),
        N=Alias(no_bg, name="no_bg"),
        Q=Alias(log, name="log"),
        Z=Alias(continuous, name="continuous"),
    ).add_common(
        V=verbose,
    )
    series = kwargs.pop("T", None)
    aliasdict.merge(kwargs)

    if is_nonstr_iter(series):
        if not hasattr(series, "__len__"):
            series = tuple(series)
        if (size := len(series)) <= 3:
            series = sequence_join(tuple(series), sep="/", ndim=1) if size else ""
        else:
            series = _explicit_series(series)

    with Session() as lib:
        series_context = (
            # The LIST table header tells GMT to use comma-list color assignment.
            lib._virtualfile_from_column(series, header="LIST")
            if is_nonstr_iter(series)
            else nullcontext(series)
        )
        with series_context as vseries:
            aliasdict["T"] = vseries
            lib.call_module(
                module="makecpt", args=build_arg_list(aliasdict, outfile=output)
            )
