"""
subplot - Manage figure subplot configuration and selection.
"""

import contextlib
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position


def _alias_option_A(  # noqa: N802
    tag: str | bool = False,
    tag_position: AnchorCode | Position | None = None,
    tag_box: Box | None = None,
    tag_number_style: Literal["arabic", "roman", "Roman"] | None = None,
    tag_orientation: Literal["horizontal", "vertical"] | None = None,
    autolabel: str | bool = False,
):
    """
    Helper function to create the alias list for the -A option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(A=_alias_option_A(**kwargs)).get("A")
    >>> parse(tag="a)")
    'a)'
    >>> parse(tag_position="TL")
    '+jTL'
    >>> parse(tag_position=Position("TL", cstype="inside", offset=("2c", "2c")))
    '+jTL+o2c/2c'
    >>> parse(tag_position=Position("TL", cstype="outside", offset=("2c", "2c")))
    '+JTL+o2c/2c'
    >>> parse(tag_box=Box(pen="1p,red", clearance="2c"))
    '+c2c+p1p,red'
    >>> parse(tag_number_style="roman")
    '+r'
    >>> parse(tag_orientation="vertical")
    '+v'
    >>> parse(
    ...     tag="(1)",
    ...     tag_position="TL",
    ...     tag_box=Box(pen="1p,red"),
    ...     tag_number_style="Roman",
    ...     tag_orientation="horizontal",
    ... )
    '(1)+jTL+p1p,red+R'
    """
    # Check conflicts with deprecated 'autolabel' parameter.
    if autolabel:
        if any(
            v is not None and v is not False
            for v in [tag, tag_position, tag_box, tag_number_style, tag_orientation]
        ):
            raise GMTParameterError(
                conflicts_with=(
                    "autolabel",
                    [
                        "tag",
                        "tag_position",
                        "tag_box",
                        "tag_number_style",
                        "tag_orientation",
                    ],
                ),
                reason="'autolabel' is specified using a unrecommend GMT command string syntax.",
            )
        return Alias(autolabel, name="autolabel")

    # Validate tag_box if provided.
    if tag_box:
        if any(
            v is not None and v is not False
            for v in {tag_box.inner_pen, tag_box.inner_gap, tag_box.radius}
        ):
            raise GMTValueError(
                tag_box,
                description="Box properties for 'tag_box' in 'Figure.subplot'",
                reason="The 'inner_pen', 'inner_gap', and 'radius' properties are not supported.",
            )
        if isinstance(tag_box.clearance, Sequence) and len(tag_box.clearance) > 2:
            raise GMTValueError(
                tag_box,
                description="Box 'clearance' property for 'tag_box' in 'Figure.subplot'",
                reason="Only one or two values are accepted.",
            )
    # Validate the tag_position if provided.
    if getattr(tag_position, "cstype", None) in {
        "mapcoords",
        "plotcoords",
        "boxcoords",
    }:
        raise GMTValueError(
            tag_position,
            description="tag position for 'Figure.subplot'.",
            reason="Only 'inside' or 'outside' cstype is allowed.",
        )

    return [
        Alias(tag, name="tag"),
        # tag_position's prefix is "+", not "+j" or "+J".
        Alias(_parse_position(tag_position), name="tag_position", prefix="+"),
        Alias(tag_box, name="tag_box"),
        Alias(
            tag_number_style,
            name="tag_number_style",
            mapping={"arabic": "", "roman": "+r", "Roman": "+R"},
        ),
        Alias(
            tag_orientation,
            name="tag_orientation",
            mapping={"horizontal": "", "vertical": "+v"},
        ),
    ]


@fmt_docstring
@contextlib.contextmanager
@use_alias(Ff="figsize", Fs="subsize", C="clearance", SC="sharex", SR="sharey")
@kwargs_to_strings(Ff="sequence", Fs="sequence")
def subplot(  # noqa: PLR0913
    self,
    nrows: int = 1,
    ncols: int = 1,
    tag: str | bool = False,
    tag_position: AnchorCode | Position | None = None,
    tag_box: Box | None = None,
    tag_orientation: Literal["horizontal", "vertical"] | None = None,
    tag_number_style: Literal["arabic", "roman", "Roman"] | None = None,
    tag_font: str | None = None,
    autolabel: str | bool = False,
    margins: float | str | Sequence[float | str] | None = None,
    title: str | None = None,
    projection: str | None = None,
    frame: str | Sequence[str] | Literal["none"] | bool = False,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Manage figure subplot configuration and selection.

    This method is used to split the current figure into a rectangular layout
    of subplots that each may contain a single self-contained figure. Begin by
    defining the layout of the entire multi-panel illustration. Several
    parameters are available to specify the systematic layout, labeling,
    dimensions, and more for the subplots.

    Full GMT docs at :gmt-docs:`subplot.html#synopsis-begin-mode`.

    $aliases
       - B = frame
       - J = projection
       - M = margins
       - R = region
       - T = title
       - V = verbose

    Parameters
    ----------
    nrows
        Number of vertical rows of the subplot grid.
    ncols
        Number of horizontal columns of the subplot grid.
    figsize : list
        Specify the final figure dimensions as [*width*, *height*].
    subsize : list
        Specify the dimensions of each subplot directly as [*width*, *height*].
        Note that only one of ``figsize`` or ``subsize`` can be provided at
        once.
    tag
        Specify automatic tagging of each subplot. It can accept a number, or a letter.
        The number or letter can be surrounded by parentheses on any side if these
        should be typeset as part of the tag. This sets the tag of the first, top-left
        subplot and others follow sequentially. If set to ``True``, default to ``"a)"``.

        Examples are:

        - ``tag="a"``: tags are ``a``, ``b``, ``c``, ...
        - ``tag="1"``: tags are ``1``, ``2``, ``3``, ...
        - ``tag="a)"``: tags are ``a)``, ``b)``, ``c)``, ...
        - ``tag="(c)"``: tags are ``(c)``, ``(d)``, ``(e)``, ...
        - ``tag=True``: same as ``tag="a)"``.
    tag_position
        Position of the subplot tag on the plot. It can be specified in two ways:

        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.
        - A :class:`pygmt.params.Position` object to fully control the position and
          offset. **Note**: the ``refpoint`` property of the Position object must be
          an two-character justification code, and ``cstype`` must be set to either
          ``"inside"`` or ``"outside"``,

        If not specified, defaults to Top Left corner inside the plot with the offset
        default to ``("4p", "4p")``, i.e., 20% of the :gmt-term:`FONT_TAG` size.
    tag_box
        Draw a box around the subplot tag. See :class:`pygmt.params.Box` for details on
        how to specify the box.

        **Notes on the use of the ``Box`` class:**

        - The property ``clearance`` only accept one or two values.
        - The properties ``inner_pen``, ``inner_gap``, ``radius`` are not supported.
    tag_number_style
        Style of the subplot tag numbers. It can be:

        - ``"arabic"``: Arabic numerals: 1, 2, 3, ... [Default].
        - ``"roman"``: Lowercase Roman numerals: i, ii, iii, ...
        - ``"Roman"``: Uppercase Roman numerals: I, II, III, ...
    tag_orientation
        Orientation of the subplot tag. It can be:

        - ``"horizontal"``: Increase tag numbers horizontally across rows [Default].
        - ``"vertical"``: Increase tag numbers vertically down columns.
    tag_font
        Font for the subplot tag [Default to ``"20p,Helvetica,black"``].
    autolabel
        Specify automatic tag of each subplot.

        .. deprecated:: v0.19.0

           Use the parameters ``tag``, ``tag_position``, ``tag_box``,
           ``tag_number_style``, ``tag_orientation``, and ``tag_font`` instead.
    clearance : str or list
        [*side*]\ *clearance*.
        Reserve a space of dimension *clearance* between the margin and the
        subplot on the specified side, using *side* values from **w**, **e**,
        **s**, or **n**; or **x** for both **w** and **e**; or **y** for both
        **s** and **n**. No *side* means all sides (i.e. ``clearance="1c"``
        would set a clearance of 1 cm on all sides). The option is repeatable
        to set aside space on more than one side (e.g.
        ``clearance=["w1c", "s2c"]`` would set a clearance of 1 cm on west
        side and 2 cm on south side). Such space will be left untouched by
        the main map plotting but can be accessed by methods that plot
        scales, bars, text, etc.
    margins
        Margin space that is added between neighboring subplots (i.e., the interior
        margins) in addition to the automatic space added for tick marks, annotations,
        and labels. The margins can be specified as either:

        - a single value (for same margin on all sides). E.g. ``"5c"``.
        - a pair of values (for separate horizontal and vertical margins). E.g.,
          ``("5c", "3c")``.
        - a set of four values (for separate left, right, bottom, and top margins).
          E.g., ``("1c", "2c", "3c", "4c")``.

        The actual gap created is always a sum of the margins for the two opposing sides
        (e.g., east plus west or south plus north margins) [Default is half the primary
        annotation font size, giving the full annotation font size as the default gap].
    sharex : bool or str
        Set subplot layout for shared x-axes. Use when all subplots in a column
        share a common *x*-range. If ``sharex=True``, the first (i.e.,
        **t**\ op) and the last (i.e., **b**\ ottom) rows will have
        *x*-annotations; use ``sharex="t"`` or ``sharex="b"`` to select only
        one of those two rows [both]. Append **+l** if annotated *x*-axes
        should have a label [none]; optionally append the label if it is the
        same for the entire subplot. Append **+t** to make space for subplot
        titles for each row; use **+tc** for top row titles only [no subplot
        titles].
    sharey : bool or str
        Set subplot layout for shared y-axes. Use when all subplots in a row
        share a common *y*-range. If ``sharey=True``, the first (i.e.,
        **l**\ eft) and the last (i.e., **r**\ ight) columns will have
        *y*-annotations; use ``sharey="l"`` or ``sharey="r"`` to select only
        one of those two columns [both]. Append **+l** if annotated *y*-axes
        will have a label [none]; optionally, append the label if it is the
        same for the entire subplot. Append **+p** to make all annotations
        axis-parallel [horizontal]; if not used you may have to set
        ``clearance`` to secure extra space for long horizontal annotations.

        Notes for ``sharex``/``sharey``:

        - Labels and titles that depends on which row or column are specified
          as usual via a subplot's own ``frame`` setting.
        - Append **+w** to the ``figsize`` or ``subsize`` parameter to draw
          horizontal and vertical lines between interior panels using selected
          pen [no lines].
    title
        Set the overarching heading of the entire figure [Default is no heading]. Font
        is determined by :gmt-term:`FONT_HEADING`. Individual subplot can have titles
        set by ``sharex``/``sharey`` or ``frame``.
    $projection
    $region
    $frame
    $verbose
    """
    self._activate_figure()

    if nrows < 1 or ncols < 1:
        _value = f"{nrows=}, {ncols=}"
        raise GMTValueError(
            _value,
            description="number of rows/columns",
            reason="Expect positive integers.",
        )

    if kwargs.get("Ff") and kwargs.get("Fs"):
        raise GMTParameterError(at_most_one=["figsize", "subsize"])

    aliasdict = AliasSystem(
        A=_alias_option_A(
            tag=tag,
            tag_position=tag_position,
            tag_box=tag_box,
            tag_number_style=tag_number_style,
            tag_orientation=tag_orientation,
            autolabel=autolabel,
        ),
        M=Alias(margins, name="margins", sep="/", size=(2, 4)),
        T=Alias(title, name="title"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    # Configure FONT_TAG if tag_font is set
    confdict = {"FONT_TAG": tag_font} if tag_font is not None else {}

    # Need to use separate sessions for "subplot begin" and "subplot end".
    # Otherwise, "subplot end" will use the last session, which may cause
    # strange positioning issues for later plotting calls.
    # See https://github.com/GenericMappingTools/pygmt/issues/2426.
    try:
        with Session() as lib:
            lib.call_module(
                module="subplot",
                args=[
                    "begin",
                    f"{nrows}x{ncols}",
                    *build_arg_list(aliasdict, confdict=confdict),
                ],
            )
            yield
    finally:
        with Session() as lib:
            lib.call_module(
                module="subplot",
                args=["end", *build_arg_list({"V": aliasdict.get("V")})],
            )


@fmt_docstring
@contextlib.contextmanager
# TODO(PyGMT>=0.23.0): Remove the deprecated 'fixedlabel' parameter.
@deprecate_parameter("fixedlabel", "tag", "v0.19.0", remove_version="v0.23.0")
@use_alias(C="clearance")
def set_panel(
    self,
    panel: int | Sequence[int] | None = None,
    tag: str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Set the current subplot panel to plot on.

    Before you start plotting you must first select the active subplot.
    **Note**: If any *projection* option is passed with the question mark
    **?** as scale or width when plotting subplots, then the dimensions of
    the map are automatically determined by the subplot size and your
    region. For Cartesian plots: If you want the scale to apply equally to
    both dimensions then you must specify ``projection="x"`` [The default
    ``projection="X"`` will fill the subplot by using unequal scales].

    $aliases
       - A = tag
       - V = verbose

    Parameters
    ----------
    panel
        *index* or (*row*, *col*).
        Sets the current subplot until further notice. **Note**: First *row* or *col* is
        0, not 1. If not given we go to the next subplot by order specified via
        ``autolabel`` in :meth:`pygmt.Figure.subplot`. As an alternative, you may bypass
        using :meth:`pygmt.Figure.set_panel` and instead supply the common option
        **panel**\ =(*row*, *col*) to the first plot command you issue in that subplot.
        GMT maintains information about the current figure and subplot. Also, you may
        give the one-dimensional *index* instead which starts at 0 and follows the row
        or column order set via ``autolabel`` in :meth:`pygmt.Figure.subplot`.
    tag
        Tag for the current subplot. It overrides the automatic tag set by the
        :meth:`pygmt.Figure.subplot` method. Use ``tag="-"`` to skip the tag for this
        panel.
    clearance : str or list
        [*side*]\ *clearance*.
        Reserve a space of dimension *clearance* between the margin and the
        subplot on the specified side, using *side* values from **w**, **e**,
        **s**, or **n**. The option is repeatable to set aside space on more
        than one side (e.g. ``clearance=["w1c", "s2c"]`` would set a clearance
        of 1 cm on west side and 2 cm on south side). Such space will be left
        untouched by the main map plotting but can be accessed by methods that
        plot scales, bars, text, etc. This setting overrides the common
        clearances set by ``clearance`` in the initial
        :meth:`pygmt.Figure.subplot` call.

    $verbose
    """
    self._activate_figure()

    aliasdict = AliasSystem(A=Alias(tag, name="tag")).add_common(V=verbose)
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(
            module="subplot",
            args=[
                "set",
                Alias(panel, name="panel", sep=",", size=2)._value,
                *build_arg_list(aliasdict),
            ],
        )
        yield
