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
    @use_alias(Ff="figsize", A="autolabel", B="frame", M="margins", T="title")
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
    margins=None,
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
        margins=margins,
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
