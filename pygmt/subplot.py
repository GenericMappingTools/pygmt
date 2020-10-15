"""High level functions for making subplots."""
import numpy as np

from .clib import Session
from .figure import Figure
from .helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


class SubPlot(Figure):
    """
    Manage modern mode figure subplot configuration and selection.

    The subplot module is used to split the current figure into a
    rectangular layout of subplots that each may contain a single
    self-contained figure. A subplot setup is started with the begin
    directive that defines the layout of the subplots, while positioning to
    a particular subplot for plotting is done via the set directive. The
    subplot process is completed via the end directive.

    Full option list at :gmt-docs:`subplot.html`
    """

    def __init__(self, nrows, ncols, figsize, **kwargs):
        super().__init__()
        # Activate main Figure, and initiate subplot
        self._activate_figure()
        self.begin_subplot(row=nrows, col=ncols, figsize=figsize, **kwargs)

    @staticmethod
    @fmt_docstring
    @use_alias(
        Ff="figsize",
        A="autolabel",
        B="frame",
        C="clearance",
        M="margins",
        S="layout",
        T="title",
    )
    @kwargs_to_strings(Ff="sequence", M="sequence")
    def begin_subplot(row=None, col=None, **kwargs):
        """
        The begin directive of subplot defines the layout of the entire multi-
        panel illustration. Several options are available to specify the
        systematic layout, labeling, dimensions, and more for the subplots.

        {aliases}
        """
        arg_str = " ".join(["begin", f"{row}x{col}", build_arg_string(kwargs)])
        with Session() as lib:
            lib.call_module(module="subplot", args=arg_str)

    @staticmethod
    @fmt_docstring
    @use_alias(F="dimensions")
    def sca(ax=None, **kwargs):
        """
        Set the current Axes instance to *ax*.

        Before you start plotting you must first select the active subplot.
        Note: If any projection (J) option is passed with ? as scale or
        width when plotting subplots, then the dimensions of the map are
        automatically determined by the subplot size and your region. For
        Cartesian plots: If you want the scale to apply equally to both
        dimensions then you must specify ``projection="x"`` [The default
        ``projection="X"`` will fill the subplot by using unequal scales].

        {aliases}
        """
        arg_str = " ".join(["set", f"{ax}", build_arg_string(kwargs)])
        with Session() as lib:
            lib.call_module(module="subplot", args=arg_str)

    @staticmethod
    @fmt_docstring
    @use_alias(V="verbose")
    def end_subplot(**kwargs):
        """
        This command finalizes the current subplot, including any placement of
        tags, and updates the gmt.history to reflect the dimensions and linear
        projection required to draw the entire figure outline. This allows
        subsequent commands, such as colorbar, to use ``position="J"`` to place
        bars with reference to the complete figure dimensions. We also reset
        the current plot location to where it was prior to the subplot.

        {aliases}
        """
        arg_str = " ".join(["end", build_arg_string(kwargs)])
        with Session() as lib:
            lib.call_module(module="subplot", args=arg_str)


def subplots(
    nrows=1,
    ncols=1,
    figsize=(6.4, 4.8),
    autolabel=None,
    clearance=None,
    margins=None,
    layout=None,
    title=None,
    **kwargs,
):
    """
    Create a figure with a set of subplots.

    Full option list at :gmt-docs:`subplot.html#synopsis-begin-mode`

    Parameters
    ----------
    nrows : int
        Number of rows of the subplot grid.

    ncols : int
        Number of columns of the subplot grid.

    figsize : tuple
        Overall figure dimensions as ``(width, height)``. Default is (6.4, 4.8)

    autolabel : bool or str
        ``[autolabel][+cdx[/dy]][+gfill][+j|Jrefpoint][+odx[/dy]][+ppen][+r|R]
        [+v]``.
        Specify automatic tagging of each subplot. Append either a number or
        letter [a]. This sets the tag of the first, top-left subplot and others
        follow sequentially. Surround the number or letter by parentheses on
        any side if these should be typeset as part of the tag. Use
        **+j|J**\\ *refpoint* to specify where the tag should be placed in the
        subplot [TL]. Note: **+j** sets the justification of the tag to
        *refpoint* (suitable for interior tags) while **+J** instead selects
        the mirror opposite (suitable for exterior tags). Append
        **+c**\\ *dx*[/*dy*] to set the clearance between the tag and a
        surrounding text box requested via **+g** or **+p** [3p/3p, i.e., 15%
        of the FONT_TAG size dimension]. Append **+g**\\ *fill* to paint the
        tag's text box with *fill* [no painting]. Append
        **+o**\\ *dx*\\ [/*dy*] to offset the tag's reference point in the
        direction implied by the justification [4p/4p, i.e., 20% of the
        FONT_TAG size]. Append **+p**\\ *pen* to draw the outline of the tag's
        text box using selected *pen* [no outline]. Append **+r** to typeset
        your tag numbers using lowercase Roman numerals; use **+R** for
        uppercase Roman numerals [Arabic numerals]. Append **+v** to increase
        tag numbers vertically down columns [horizontally across rows].

    clearance : str
        ``[side]clearance``.
        Reserve a space of dimension *clearance* between the margin and the
        subplot on the specified side, using *side* values from **w**, **e**,
        **s**, or **n**, or **x** for both **w** and **e** or **y** for both
        **s** and **n**.  No *side* means all sides. The option is repeatable
        to set aside space on more than one side. Such space will be left
        untouched by the main map plotting but can be accessed by modules that
        plot scales, bars, text, etc.  Settings specified under **begin**
        directive apply to all subplots, while settings under **set** only
        apply to the selected (active) subplot. **Note**: Common options
        **x_offset** and **y_offset* are not available during subplots; use
        **clearance** instead.

    margins : tuple
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

    layout : str or list
        Set subplot layout for shared axes. May be set separately for rows
        (**R**) and columns (**C**). E.g. ``layout=['Rl', 'Cb']``.
        Considerations for **C**: Use when all subplots in a **C**\\ olumn
        share a common *x*-range. The first (i.e., **t**\\ op) and the last
        (i.e., **b**\\ ottom) rows will have *x* annotations; append **t** or
        **b** to select only one of those two rows [both]. Append **+l** if
        annotated *x*-axes should have a label [none]; optionally append the
        label if it is the same for the entire subplot. Append **+t** to make
        space for subplot titles for each row; use **+tc** for top row titles
        only [no subplot titles]. Labels and titles that depends on which row
        or column are specified as usual via a subplot's own **frame** setting.
        Considerations for **R**: Use when all subplots in a **R**\\ ow share a
        common *y*-range. The first (i.e., **l**\\ eft) and the last (i.e.,
        **r**\\ ight) columns will have *y*-annotations; append **l** or **r**
        to select only one of those two columns [both]. Append **+l** if
        annotated *y*-axes will have a label [none]; optionally, append the
        label if it is the same for the entire subplot. Append **+p** to make
        all annotations axis-parallel [horizontal]; if not used you may have to
        set **clearance** to secure extra space for long horizontal
        annotations. Append **+w** to draw horizontal and vertical lines
        between interior panels using selected pen [no lines].

    title : str
        Overarching heading for the entire figure. Font is determined by
        setting ``FONT_HEADING``.

    Returns
    -------
    fig : :class:`pygmt.Figure`
        A PyGMT Figure instance.

    axs : numpy.ndarray
        Array of Axes objects.
    """
    # Get PyGMT Figure with SubPlot initiated
    fig = SubPlot(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        autolabel=autolabel,
        clearance=clearance,
        margins=margins,
        layout=layout,
        title=f'"{title}"' if title else None,
        **kwargs,
    )

    # Setup matplotlib-like Axes
    axs = np.empty(shape=(nrows, ncols), dtype=object)
    for index in range(nrows * ncols):
        i = index // ncols  # row
        j = index % ncols  # column
        axs[i, j] = index

    return fig, axs
