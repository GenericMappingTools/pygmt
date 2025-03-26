"""
Clip.
"""

from collections.abc import Sequence

from pygmt.clib import Session
from pygmt.helpers import build_arg_list, is_nonstr_iter


class ClipAccessor:
    """
    Accessor for the clip methods.
    """

    def __init__(self, fig):
        self._fig = fig  # The parent Figure object.

    def land(self, **kwargs):
        """
        Clip the land area (i.e., "dry" areas).

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the land areas.

        Parameters
        ----------
        kwargs
            Additional arguments passed to :meth:`pygmt.Figure.coast`.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.land():
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        self.data = None
        self.module_enter = self.module_exit = "coast"
        self.kwargs_enter = {"G": True} | kwargs
        self.kwargs_exit = {"Q": True}
        return self

    def water(self, **kwargs):
        """
        Clip the water areas (i.e., "wet" areas such as oceans and lakes).

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the water areas.

        Parameters
        ----------
        kwargs
            Additional arguments passed to :meth:`pygmt.Figure.coast`.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.water():
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        self.data = None
        self.module_enter = self.module_exit = "coast"
        self.kwargs_enter = {"S": True} | kwargs
        self.kwargs_exit = {"Q": True}
        return self

    def polygon(self, x, y, **kwargs):
        """
        Clip polygonal paths.

        Parameters
        ----------
        x/y
            Coordinates of polygon.
        kwargs
            Additional arguments passed to GMT's ``clip`` module.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.polygon(x=[-10, 10, 10, -10], y=[-10, -10, 10, 10]):
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        self.data = (x, y)
        self.module_enter = self.module_exit = "clip"
        self.kwargs_enter = kwargs
        self.kwargs_exit = {"C": True}

        return self

    def dcw(self, code: str | Sequence[str]):
        """
        Clip based on the Digital Chart of the World.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.dcw(code="JP"):
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        _code = ",".join(code) if is_nonstr_iter(code) else code
        self.data = None
        self.module_enter = "coast"
        self.kwargs_enter = {"E": _code + "+c"}
        self.module_exit = "coast"
        self.kwargs_exit = {"Q": True}
        return self

    def solar(self, **kwargs):
        """
        Clip the data to the solar terminator.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.solar(T="c"):
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        self.data = None
        self.module_enter = "solar"
        self.kwargs_enter = {"G": True} | kwargs
        self.module_exit = "clip"
        self.kwargs_exit = {"C": True}

        return self

    def mask(self, x, y, spacing, radius=None):
        """
        Clip the data to a mask.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="Q15c", frame=True)
        >>> with fig.clip.mask(
        ...     x=[180] * 16, y=np.arange(-80, 80, 10), spacing="30m", radius="5d"
        ... ):
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        self.data = (x, y)
        self.module_enter = self.module_exit = "mask"
        self.kwargs_enter = {"I": spacing, "S": radius}
        self.kwargs_exit = {"C": True}
        return self

    def __enter__(self):
        """
        Enter the context manager.
        """
        self._fig._preprocess()  # Activate the current figure.
        with Session() as lib:
            if self.data:
                with lib.virtualfile_in(x=self.data[0], y=self.data[1]) as vintbl:
                    lib.call_module(
                        module=self.module_enter,
                        args=build_arg_list(self.kwargs_enter, infile=vintbl),
                    )
            else:
                lib.call_module(
                    module=self.module_enter, args=build_arg_list(self.kwargs_enter)
                )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        self._fig._preprocess()  # Activate the current figure.
        with Session() as lib:
            lib.call_module(
                module=self.module_exit, args=build_arg_list(self.kwargs_exit)
            )
