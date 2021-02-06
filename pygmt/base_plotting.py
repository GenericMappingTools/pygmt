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

    from pygmt.src import (  # pylint: disable=import-outside-toplevel
        basemap,
        coast,
        colorbar,
        contour,
        grdcontour,
        grdimage,
        grdview,
        image,
        inset,
        legend,
        logo,
        meca,
        plot,
        plot3d,
        text,
    )
