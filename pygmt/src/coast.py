"""
coast - Plot continents, countries, shorelines, rivers, and borders.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import args_in_kwargs, build_arg_list, fmt_docstring, use_alias
from pygmt.params import Box

__doctest_skip__ = ["coast"]


@fmt_docstring
@use_alias(A="area_thresh", C="lakes", E="dcw")
def coast(  # noqa: PLR0913
    self,
    resolution: Literal[
        "auto", "full", "high", "intermediate", "low", "crude", None
    ] = None,
    land: str | None = None,
    water: str | None = None,
    rivers: int | str | Sequence[int | str] | None = None,
    borders: int | str | Sequence[int | str] | None = None,
    shorelines: bool | str | Sequence[int | str] = False,
    map_scale: str | None = None,
    box: Box | bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot continents, countries, shorelines, rivers, and borders.

    Plots grayshaded, colored, or textured land masses [or water masses] on
    maps and [optionally] draws coastlines, rivers, and political
    boundaries. The data files come in 5 different resolutions: (**f**)ull,
    (**h**)igh, (**i**)ntermediate, (**l**)ow, and (**c**)rude. The full
    resolution files amount to more than 55 Mb of data and provide great
    detail; for maps of larger geographical extent it is more economical to
    use one of the other resolutions. If the user selects to paint the
    land areas and does not specify fill of water areas then the latter
    will be transparent (i.e., earlier graphics drawn in those areas will
    not be overwritten). Likewise, if the water areas are painted and no
    land fill is set then the land areas will be transparent.

    A map projection must be supplied.

    Full GMT docs at :gmt-docs:`coast.html`.

    $aliases
       - B = frame
       - D = resolution
       - F = box
       - G = land
       - I = rivers
       - J = projection
       - L = map_scale
       - R = region
       - S = water
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    $area_thresh
    lakes : str or list
        *fill*\ [**+l**\|\ **+r**].
        Set the shade, color, or pattern for lakes and river-lakes. The
        default is the fill chosen for "wet" areas set by the ``water``
        parameter. Optionally, specify separate fills by appending
        **+l** for lakes or **+r** for river-lakes, and passing multiple
        strings in a list.
    resolution
        Select the resolution of the coastline dataset to use. The available resolutions
        from highest to lowest are: ``"full"``, ``"high"``, ``"intermediate"``,
        ``"low"``, and ``"crude"``, which drops by 80% between levels. Default is
        ``"auto"`` to automatically select the most suitable resolution given the chosen
        map scale.
    land
        Select filling of "dry" areas.
    water
        Select filling of "wet" areas.
    rivers
        Draw rivers. Specify the type of rivers to draw, and optionally append a pen
        attribute, in the format *river*\ /*pen* [Default pen is
        ``"0.25p,black,solid"``]. Pass a sequence of river types or *river*\ /*pen*
        strings to draw different river types with different pens.

        Choose from the following river types:

        - ``0``: Double-lined rivers (river-lakes)
        - ``1``: Permanent major rivers
        - ``2``: Additional major rivers
        - ``3``: Additional rivers
        - ``4``: Minor rivers
        - ``5``: Intermittent rivers - major
        - ``6``: Intermittent rivers - additional
        - ``7``: Intermittent rivers - minor
        - ``8``: Major canals
        - ``9``: Minor canals
        - ``10``: Irrigation canals

        Or choose from the following preconfigured river groups:

        - ``"a"``: All rivers and canals (types ``0`` - ``10``)
        - ``"A"``: Rivers and canals except river-lakes (types ``1`` - ``10``)
        - ``"r"``: Permanent rivers (types ``0`` - ``4``)
        - ``"R"``: Permanent rivers except river-lakes (types ``1`` - ``4``)
        - ``"i"``: Intermittent rivers (types ``5`` - ``7``)
        - ``"c"``: Canals (types ``8`` - ``10``)

        Example usage:

        - ``rivers=1``: Draw permanent major rivers with default pen.
        - ``rivers="1/0.5p,blue"``: Draw permanent major rivers with a 0.5-point blue
          pen.
        - ``rivers=["1/0.5p,blue", "5/0.3p,cyan,dashed"]``: Draw permanent major rivers
          with a 0.5-point blue pen and intermittent major rivers with a 0.3-point
          dashed cyan pen.
    map_scale
        Draw a map scale bar on the plot.

        .. deprecated:: v0.19.0

            Use :meth:`pygmt.Figure.scalebar` instead. This parameter is maintained
            for backward compatibility and accepts raw GMT CLI strings for the ``-L``
            option.
    box
        Draw a background box behind the map scale or rose. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    borders
        Draw political boundaries. Specify the type of boundary to draw, and optionally
        append a pen attribute, in the format *border*\ /*pen* [Default pen is
        ``"0.25p,black,solid"``]. Pass a sequence of border types or *border*\ /*pen*
        strings to draw different border types with different pens.

        Choose from the following border types:

        - ``1``: National boundaries
        - ``2``: State boundaries within the Americas
        - ``3``: Marine boundaries
        - ``"a"``: All boundaries (types ``1`` - ``3``)

        Example usage:

        - ``borders=1``: Draw national boundaries with default pen.
        - ``borders="1/0.5p,red"``: Draw national boundaries with a 0.5-point red pen.
        - ``borders=["1/0.5p,red", "2/0.3p,blue,dashed"]``: Draw national boundaries
          with a 0.5-point red pen and state boundaries with a 0.3-point dashed blue
          pen.
    shorelines
        Draw shorelines. Specify the pen attributes for shorelines [Default pen is
        ``"0.25p,black,solid"``]. Shorelines have four levels; by default, the same pen
        is used for all levels. To specify the shoreline level, use the format
        *level*\ /*pen*. Pass a sequence of *level*\ /*pen* strings to draw different
        shoreline levels with different pens. When specific level pens are set, those
        not listed will not be drawn [Default draws all levels]. ``shorelines=True``
        draws all levels with the default pen.

        Choose from the following shoreline levels:

        - ``1``: Coastline
        - ``2``: Lakeshore
        - ``3``: Island-in-lake shore
        - ``4``: Lake-in-island-in-lake shore

        Example usage:

        - ``shorelines=True``: Draw all shoreline levels with default pen.
        - ``shorelines="0.5p,blue"``: Draw all shoreline levels with a 0.5-point blue
          pen.
        - ``shorelines="1/0.5p,black"``: Draw only coastlines with a 0.5-point black
          pen.
        - ``shorelines=["1/0.8p,black", "2/0.4p,blue"]``: Draw coastlines with a
          0.8-point black pen and lakeshores with a 0.4-point blue pen.
    dcw : str or list
        *code1,code2,…*\ [**+g**\ *fill*\ ][**+p**\ *pen*\ ][**+z**].
        Select painting country polygons from the `Digital Chart of the World
        <https://en.wikipedia.org/wiki/Digital_Chart_of_the_World>`__.
        Append one or more comma-separated countries using the 2-letter
        `ISO 3166-1 alpha-2 convention
        <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`__.
        To select a state of a country (if available), append .\ *state*,
        (e.g, ``"US.TX"`` for Texas). To specify a whole continent, prepend **=**
        to any of the continent codes (e.g. ``"=EU"`` for Europe). Append
        **+p**\ *pen* to draw polygon outlines [Default is no outline] and
        **+g**\ *fill* to fill them [Default is no fill].
    $projection
    $region
        *Required if this is the first plot command.*
    $frame
    $verbose
    $panel
    $perspective
    $transparency

    Example
    -------
    >>> import pygmt
    >>> # Create a new plot with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # Call the coast method for the plot
    >>> fig.coast(
    ...     # Set the projection to Mercator, and the plot width to 10 centimeters
    ...     projection="M10c",
    ...     # Set the region of the plot
    ...     region=[-10, 30, 30, 60],
    ...     # Set the frame of the plot, here annotations and major ticks
    ...     frame="a",
    ...     # Set the color of the land to "darkgreen"
    ...     land="darkgreen",
    ...     # Set the color of the water to "lightblue"
    ...     water="lightblue",
    ...     # Draw national borders with a 1-point black line
    ...     borders="1/1p,black",
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    self._activate_figure()

    # Update the current region tracking
    self._update_current_region(region)

    if (
        kwargs.get("G", land) is None
        and kwargs.get("S", water) is None
        and kwargs.get("I", rivers) is None
        and kwargs.get("N", borders) is None
        and kwargs.get("W", shorelines) is False
        and not args_in_kwargs(args=["C", "E", "Q"], kwargs=kwargs)
    ):
        raise GMTParameterError(
            at_least_one=[
                "land",
                "water",
                "rivers",
                "borders",
                "shorelines",
                "lakes",
                "dcw",
                "Q",
            ]
        )

    aliasdict = AliasSystem(
        D=Alias(
            resolution,
            name="resolution",
            mapping={
                "auto": "a",
                "full": "f",
                "high": "h",
                "intermediate": "i",
                "low": "l",
                "crude": "c",
            },
        ),
        F=Alias(box, name="box"),
        G=Alias(land, name="land"),
        I=Alias(rivers, name="rivers"),
        L=Alias(map_scale, name="map_scale"),  # Deprecated.
        N=Alias(borders, name="borders"),
        S=Alias(water, name="water"),
        W=Alias(shorelines, name="shorelines"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="coast", args=build_arg_list(aliasdict))
