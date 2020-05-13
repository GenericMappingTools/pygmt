import numpy as np

from .figure import SubPlot


def subplots(nrows=1, ncols=1, figsize=(6.4, 4.8), **kwargs):
    """
    Create a figure with a set of subplots.

    Parameters
    ----------
    nrows : int
        Number of rows of the subplot grid.

    ncols : int
        Number of columns of the subplot grid.

    figsize : tuple
        Figure dimensions as ``(width, height)``.

    Returns
    -------
    fig : :class:`pygmt.Figure`
        A PyGMT Figure instance.

    axs : numpy.ndarray
        Array of Axes objects.
    """
    # Get PyGMT Figure with SubPlot initiated
    fig = SubPlot(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)

    # Setup matplotlib-like Axes
    axs = np.empty(shape=(nrows, ncols), dtype=object)
    for index in range(nrows * ncols):
        i = index // ncols  # row
        j = index % ncols  # column
        axs[i, j] = index

    return fig, axs
