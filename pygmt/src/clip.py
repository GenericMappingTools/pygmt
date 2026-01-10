"""
clip - Clip a path and only plot data inside or outside.
"""

from collections.abc import Sequence

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, is_nonstr_iter


class _ClipContext:
    """
    Base class for the clip context manager.
    """

    def __init__(self, figure, data=None, x=None, y=None, **kwargs):
        self._figure = figure  # The parent Figure object.
        self._data = data
        self._x = x
        self._y = y
        self._kwargs = kwargs

    def __enter__(self):
        self._figure._activate_figure()
        self._activate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._figure._activate_figure()
        self._deactivate()

    def _activate(self):
        """
        Activate clipping.
        """
        raise NotImplementedError

    def _deactivate(self):
        """
        Deactivate clipping.
        """
        raise NotImplementedError


class _ClipLand(_ClipContext):
    """
    Clip the land area (i.e., "dry" areas).
    """

    def _activate(self):
        self._figure.coast(land=True, **self._kwargs)

    def _deactivate(self):
        self._figure.coast(Q=True)


class _ClipWater(_ClipContext):
    """
    Clip the water areas (i.e., "wet" areas such as oceans and lakes).
    """

    def _activate(self):
        self._figure.coast(water=True, **self._kwargs)

    def _deactivate(self):
        self._figure.coast(Q=True)


class _ClipDcw(_ClipContext):
    """
    Clip based on the Digital Chart of the World.
    """

    def _activate(self):
        self._figure.coast(**self._kwargs)

    def _deactivate(self):
        self._figure.coast(Q=True)


class _ClipSolar(_ClipContext):
    """
    Clip the data to the solar terminator.
    """

    def _activate(self):
        self._figure.solar(fill=True, **self._kwargs)

    def _deactivate(self):
        with Session() as lib:
            lib.call_module(module="clip", args=build_arg_list({"C": True}))


class _ClipPolygon(_ClipContext):
    """
    Clip polygonal paths.
    """

    def _activate(self):
        with Session() as lib:
            with lib.virtualfile_in(data=self._data, x=self._x, y=self._y) as vintbl:
                lib.call_module(
                    module="clip",
                    args=build_arg_list(self._kwargs, infile=vintbl),
                )

    def _deactivate(self):
        with Session() as lib:
            lib.call_module(module="clip", args=build_arg_list({"C": True}))


class _ClipMask(_ClipContext):
    """
    Clip the data to a mask.
    """

    def _activate(self):
        with Session() as lib:
            with lib.virtualfile_in(data=self._data) as vintbl:
                lib.call_module(
                    module="mask",
                    args=build_arg_list(self._kwargs, infile=vintbl),
                )

    def _deactivate(self):
        with Session() as lib:
            lib.call_module(module="mask", args=build_arg_list({"C": True}))


class ClipAccessor:
    """
    Accessor for different clip methods.
    """

    def __init__(self, figure):
        """
        Initialize the ClipAccessor.
        """
        self._figure = figure  # The parent Figure object.

    def land(self, **kwargs):
        """
        Clip the land area (i.e., "dry" areas) and only plot data inside.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the land areas.

        Parameters
        ----------
        kwargs
            Additional keyword arguments passed to :meth:`pygmt.Figure.coast`. Not all
            parameters make sense in this context.

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
        return _ClipLand(self._figure, **kwargs)

    def water(self, **kwargs):
        """
        Clip the water areas (i.e., "wet" areas such as oceans and lakes) and only plot
        data inside.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the water areas.

        Parameters
        ----------
        kwargs
            Additional keyword arguments passed to :meth:`pygmt.Figure.coast`. Not all
            parameters make sense in this context.

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
        return _ClipWater(self._figure, **kwargs)

    def dcw(self, code: str | Sequence[str], **kwargs):
        """
        Clip based on the Digital Chart of the World.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the region defined by the codes.

        Parameters
        ----------
        code
            The codes of the region to clip to.
        kwargs
            Additional keyword arguments passed to :meth:`pygmt.Figure.coast`. Not all
            parameters make sense in this context.

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
        return _ClipDcw(self._figure, dcw=f"{_code}+c", **kwargs)

    def solar(self, invert: bool = False, **kwargs):
        """
        Clip the data to the solar terminator.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the solar terminator.

        Parameters
        ----------
        invert
            Invert the sense of what is inside and outside the terminator.
        kwargs
            Additional keyword arguments passed to :meth:`pygmt.Figure.solar`.
            Parameters ``frame`` and ``fill`` are not allowed here.

        Examples
        --------
        >>> from pygmt import Figure
        >>> from pygmt.datasets import load_earth_relief
        >>>
        >>> grid = load_earth_relief()
        >>> fig = Figure()
        >>> fig.basemap(region="g", projection="W15c", frame=True)
        >>> with fig.clip.solar(terminator="civil"):
        ...     fig.grdimage(grid, cmap="geo")
        >>> fig.show()
        """
        aliasdict = AliasSystem(
            N=Alias(invert, name="invert"),
        )
        aliasdict.merge(kwargs)
        return _ClipSolar(self._figure, **aliasdict)

    @fmt_docstring
    def polygon(self, data=None, x=None, y=None, **kwargs):
        """
        Clip polygonal paths.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the polygons.

        {aliases}

        Parameters
        ----------
        data
            Either a file name to an ASCII data table, a 2-D {table-classes}.
        x/y
            X and Y coordinates of the polygon.
        {frame}
        {region}
        {projection}
        {verbose}
        straight_line
            By default, line segments are connected as straight lines in the Cartesian
            and polar coordinate systems, and as great circle arcs (by resampling coarse
            input data along such arcs) in the geographic coordinate system. The
            ``straight_line`` parameter can control the connection of line segments.
            Valid values are:

            - ``True``: Draw line segments as straight lines in geographic coordinate
              systems.
            - ``"x"``: Draw line segments by first along *x*, then along *y*.
            - ``"y"``: Draw line segments by first along *y*, then along *x*.

            Here, *x* and *y* have different meanings depending on the coordinate system

            - **Cartesian** coordinate system: *x* and *y* are the X- and Y-axes.
            - **Polar** coordinate system: *x* and *y* are theta and radius.
            - **Geographic** coordinate system: *x* and *y* are parallels and meridians.

            .. attention::

                There exits a bug in GMT<=6.5.0 that, in geographic coordinate systems,
                the meaning of *x* and *y* is reversed, i.e., *x* means meridians and
                *y* means parallels. The bug is fixed by upstream
                `PR #8648 <https://github.com/GenericMappingTools/gmt/pull/8648>`__.
        invert
            Invert the sense of what is inside and outside. For example, when using a
            single path, this means that only points outside that path will be shown.
            Cannot be used together with ``frame``.
        pen
            Draw outline of clip path using given pen attributes before clipping is
            initiated [Default is no outline].

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
        return _ClipPolygon(self._figure, data=data, x=x, y=y, **kwargs)

    @fmt_docstring
    def mask(
        self,
        data=None,
        x=None,
        y=None,
        region=None,
        spacing=None,
        invert: bool = False,
        radius=None,
        **kwargs,
    ):
        """
        Clip the data to a mask.

        Must be used as a context manager. Any plotting operations within the context
        manager will be clipped to the mask.

        **Aliases**
        .. hlist::
           :columns: 3

           - I = spacing
           - N = invert
           - R = region
           - S = radius

        Parameters
        ----------
        data
            Either a file name to an ASCII data table, a 2-D {table-classes}.
        x/y
            X and Y coordinates of the mask.
        {spacing}
        invert
            Invert the sense of what is inside and outside.

        Examples
        --------
        >>> import numpy as np
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
        aliasdict = AliasSystem(
            I=Alias(spacing, name="spacing"),
            N=Alias(invert, name="invert"),
            S=Alias(radius, name="radius"),
        ).add_common(
            R=region,
        )
        aliasdict.merge(kwargs)

        return _ClipMask(self._figure, data=data, x=x, y=y, **aliasdict)
