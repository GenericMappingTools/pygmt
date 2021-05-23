"""
subplot - Manage modern mode figure subplot configuration and selection.
"""
import contextlib

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@contextlib.contextmanager
@use_alias(
    Ff="figsize",
    Fs="subsize",
    A="autolabel",
    B="frame",
    C="clearance",
    J="projection",
    M="margins",
    R="region",
    SC="sharex",
    SR="sharey",
    T="title",
    V="verbose",
    X="xshift",
    Y="yshift",
)
@kwargs_to_strings(Ff="sequence", Fs="sequence", M="sequence", R="sequence")
def subplot(self, nrows=1, ncols=1, **kwargs):
    r"""
    Create multi-panel subplot figures.

    This function is used to split the current figure into a rectangular layout
    of subplots that each may contain a single self-contained figure. Begin by
    defining the layout of the entire multi-panel illustration. Several
    parameters are available to specify the systematic layout, labeling,
    dimensions, and more for the subplots.

    Full option list at :gmt-docs:`subplot.html#synopsis-begin-mode`

    {aliases}

    Parameters
    ----------
    nrows : int
        Number of vertical rows of the subplot grid.
    ncols : int
        Number of horizontal columns of the subplot grid.
    figsize : tuple
        Specify the final figure dimensions as (*width*, *height*).
    subsize : tuple
        Specify the dimensions of each subplot directly as (*width*, *height*).
        Note that only one of ``figsize`` or ``subsize`` can be provided at
        once.

    autolabel : bool or str
        [*autolabel*][**+c**\ *dx*\ [/*dy*]][**+g**\ *fill*][**+j**\|\ **J**\
        *refpoint*][**+o**\ *dx*\ [/*dy*]][**+p**\ *pen*][**+r**\|\ **R**]
        [**+v**].
        Specify automatic tagging of each subplot. Append either a number or
        letter [a]. This sets the tag of the first, top-left subplot and others
        follow sequentially. Surround the number or letter by parentheses on
        any side if these should be typeset as part of the tag. Use
        **+j**\|\ **J**\ *refpoint* to specify where the tag should be placed
        in the subplot [TL]. Note: **+j** sets the justification of the tag to
        *refpoint* (suitable for interior tags) while **+J** instead selects
        the mirror opposite (suitable for exterior tags). Append
        **+c**\ *dx*\[/*dy*] to set the clearance between the tag and a
        surrounding text box requested via **+g** or **+p** [3p/3p, i.e., 15%
        of the :gmt-term:`FONT_TAG` size dimension]. Append **+g**\ *fill* to
        paint the tag's text box with *fill* [no painting]. Append
        **+o**\ *dx*\ [/*dy*] to offset the tag's reference point in the
        direction implied by the justification [4p/4p, i.e., 20% of the
        :gmt-term:`FONT_TAG` size]. Append **+p**\ *pen* to draw the outline of
        the tag's text box using selected *pen* [no outline]. Append **+r** to
        typeset your tag numbers using lowercase Roman numerals; use **+R** for
        uppercase Roman numerals [Arabic numerals]. Append **+v** to increase
        tag numbers vertically down columns [horizontally across rows].
    {B}
    clearance : str or list
        [*side*]\ *clearance*.
        Reserve a space of dimension *clearance* between the margin and the
        subplot on the specified side, using *side* values from **w**, **e**,
        **s**, or **n**; or **x** for both **w** and **e**; or **y** for both
        **s** and **n**. No *side* means all sides (i.e. ``clearance='1c'``
        would set a clearance of 1 cm on all sides). The option is repeatable
        to set aside space on more than one side (e.g. ``clearance=['w1c',
        's2c']`` would set a clearance of 1 cm on west side and 2 cm on south
        side). Such space will be left untouched by the main map plotting but
        can be accessed by modules that plot scales, bars, text, etc.
    {J}
    margins : str or list
        This is margin space that is added between neighboring subplots (i.e.,
        the interior margins) in addition to the automatic space added for tick
        marks, annotations, and labels. The margins can be specified as either:

        - a single value (for same margin on all sides). E.g. '5c'.
        - a pair of values (for setting separate horizontal and vertical
          margins). E.g. ['5c', '3c'].
        - a set of four values (for setting separate left, right, bottom, and
          top margins). E.g. ['1c', '2c', '3c', '4c'].

        The actual gap created is always a sum of the margins for the two
        opposing sides (e.g., east plus west or south plus north margins)
        [Default is half the primary annotation font size, giving the full
        annotation font size as the default gap].
    {R}
    sharex : bool or str
        Set subplot layout for shared x-axes. Use when all subplots in a column
        share a common *x*-range. If ``sharex=True``, the first (i.e.,
        **t**\ op) and the last (i.e., **b**\ ottom) rows will have
        *x*-annotations; use ``sharex='t'`` or ``sharex='b'`` to select only
        one of those two rows [both]. Append **+l** if annotated *x*-axes
        should have a label [none]; optionally append the label if it is the
        same for the entire subplot. Append **+t** to make space for subplot
        titles for each row; use **+tc** for top row titles only [no subplot
        titles].
    sharey : bool or str
        Set subplot layout for shared y-axes. Use when all subplots in a row
        share a common *y*-range. If ``sharey=True``, the first (i.e.,
        **l**\ eft) and the last (i.e., **r**\ ight) columns will have
        *y*-annotations; use ``sharey='l'`` or ``sharey='r'`` to select only
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
    title : str
        While individual subplots can have titles (see ``sharex``/``sharey`` or
        ``frame``), the entire figure may also have an overarching *heading*
        [no heading]. Font is determined by setting :gmt-term:`FONT_HEADING`.
    {V}
    {XY}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    # allow for spaces in string without needing double quotes
    if isinstance(kwargs.get("A"), str):
        kwargs["A"] = f'"{kwargs.get("A")}"'
    kwargs["T"] = f'"{kwargs.get("T")}"' if kwargs.get("T") else None

    if nrows < 1 or ncols < 1:
        raise GMTInvalidInput("Please ensure that both 'nrows'>=1 and 'ncols'>=1.")
    if kwargs.get("Ff") and kwargs.get("Fs"):
        raise GMTInvalidInput(
            "Please provide either one of 'figsize' or 'subsize' only."
        )

    with Session() as lib:
        try:
            arg_str = " ".join(["begin", f"{nrows}x{ncols}", build_arg_string(kwargs)])
            lib.call_module("subplot", arg_str)
            yield
        finally:
            v_arg = build_arg_string({"V": kwargs.get("V")})
            lib.call_module("subplot", f"end {v_arg}")


@fmt_docstring
@contextlib.contextmanager
@use_alias(A="fixedlabel", C="clearance", V="verbose")
def set_panel(self, panel=None, **kwargs):
    r"""
    Set the current subplot panel to plot on.

    Before you start plotting you must first select the active subplot. Note:
    If any *projection* option is passed with the question mark **?** as scale
    or width when plotting subplots, then the dimensions of the map are
    automatically determined by the subplot size and your region. For Cartesian
    plots: If you want the scale to apply equally to both dimensions then you
    must specify ``projection="x"`` [The default ``projection="X"`` will fill
    the subplot by using unequal scales].

    {aliases}

    Parameters
    ----------
    panel : str or list
        *row,col*\|\ *index*.
        Sets the current subplot until further notice. **Note**: First *row*
        or *col* is 0, not 1. If not given we go to the next subplot by order
        specified via ``autolabel`` in :meth:`pygmt.Figure.subplot`. As an
        alternative, you may bypass using :meth:`pygmt.Figure.set_panel` and
        instead supply the common option **panel**\ =[*row,col*] to the first
        plot command you issue in that subplot. GMT maintains information about
        the current figure and subplot. Also, you may give the one-dimensional
        *index* instead which starts at 0 and follows the row or column order
        set via ``autolabel`` in :meth:`pygmt.Figure.subplot`.

    fixedlabel : str
        Overrides the automatic labeling with the given string. No modifiers
        are allowed. Placement, justification, etc. are all inherited from how
        ``autolabel`` was specified by the initial :meth:`pygmt.Figure.subplot`
        command.

    clearance : str or list
        [*side*]\ *clearance*.
        Reserve a space of dimension *clearance* between the margin and the
        subplot on the specified side, using *side* values from **w**, **e**,
        **s**, or **n**. The option is repeatable to set aside space on more
        than one side (e.g. ``clearance=['w1c', 's2c']`` would set a clearance
        of 1 cm on west side and 2 cm on south side). Such space will be left
        untouched by the main map plotting but can be accessed by modules that
        plot scales, bars, text, etc. This setting overrides the common
        clearances set by ``clearance`` in the initial
        :meth:`pygmt.Figure.subplot` call.

    {V}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    # allow for spaces in string with needing double quotes
    kwargs["A"] = f'"{kwargs.get("A")}"' if kwargs.get("A") is not None else None
    # convert tuple or list to comma-separated str
    panel = ",".join(map(str, panel)) if is_nonstr_iter(panel) else panel

    with Session() as lib:
        arg_str = " ".join(["set", f"{panel}", build_arg_string(kwargs)])
        lib.call_module(module="subplot", args=arg_str)
        yield
