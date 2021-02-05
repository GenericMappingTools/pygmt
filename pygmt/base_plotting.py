"""
Base class with plot generating commands.

Does not define any special non-GMT methods (savefig, show, etc).
"""


class BasePlotting:
    """
    Base class for Figure and Subplot.

    Defines the plot generating methods and a hook for subclasses to insert
    special arguments (the _preprocess method).
    """

    def _preprocess(self, **kwargs):  # pylint: disable=no-self-use
        """
        Make any changes to kwargs or required actions before plotting.

        This method is run before all plotting commands and can be used to
        insert special arguments into the kwargs or make any actions that are
        required before ``call_module``.

        For example, the :class:`pygmt.Figure` needs this to tell the GMT
        modules to plot to a specific figure.

        This is a dummy method that does nothing.

        Returns
        -------
        kwargs : dict
            The same input kwargs dictionary.

        Examples
        --------

        >>> base = BasePlotting()
        >>> base._preprocess(resolution="low")
        {'resolution': 'low'}
        """
        return kwargs

    from pygmt.src import basemap  # pylint: disable=import-outside-toplevel
    from pygmt.src import coast  # pylint: disable=import-outside-toplevel
    from pygmt.src import colorbar  # pylint: disable=import-outside-toplevel
    from pygmt.src import contour  # pylint: disable=import-outside-toplevel
    from pygmt.src import grdcontour  # pylint: disable=import-outside-toplevel
    from pygmt.src import grdimage  # pylint: disable=import-outside-toplevel
    from pygmt.src import grdview  # pylint: disable=import-outside-toplevel
    from pygmt.src import image  # pylint: disable=import-outside-toplevel
    from pygmt.src import legend  # pylint: disable=import-outside-toplevel
    from pygmt.src import logo  # pylint: disable=import-outside-toplevel
    from pygmt.src import meca  # pylint: disable=import-outside-toplevel
    from pygmt.src import plot  # pylint: disable=import-outside-toplevel
    from pygmt.src import plot3d  # pylint: disable=import-outside-toplevel
    from pygmt.src import text  # pylint: disable=import-outside-toplevel
    from pygmt.src import inset, meca  # pylint: disable=import-outside-toplevel
