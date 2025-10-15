"""
coast - Plot continents, countries, shorelines, rivers, and borders.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.params import Box

__doctest_skip__ = ["coast"]


@fmt_docstring
@use_alias(
    A="area_thresh",
    B="frame",
    C="lakes",
    E="dcw",
    G="land",
    I="rivers",
    L="map_scale",
    N="borders",
    S="water",
    W="shorelines",
    p="perspective",
)
@kwargs_to_strings(p="sequence")
def coast(
    self,
    projection: str | None = None,
    resolution: Literal[
        "auto", "full", "high", "intermediate", "low", "crude", None
    ] = None,
    box: Box | bool = False,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
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

    {aliases}
       - D = resolution
       - F = box
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    {projection}
    {region}
        *Required if this is the first plot command.*
    {area_thresh}
    {frame}
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
    land : str
        Select filling of "dry" areas.
    rivers : int, str, or list
        *river*\ [/*pen*].
        Draw rivers. Specify the type of rivers and [optionally] append
        pen attributes [Default is ``"0.25p,black,solid"``].

        Choose from the list of river types below; pass a list to ``rivers``
        to use multiple arguments.

        - ``0``: double-lined rivers (river-lakes)
        - ``1``: permanent major rivers
        - ``2``: additional major rivers
        - ``3``: additional rivers
        - ``4``: minor rivers
        - ``5``: intermittent rivers - major
        - ``6``: intermittent rivers - additional
        - ``7``: intermittent rivers - minor
        - ``8``: major canals
        - ``9``: minor canals
        - ``10``: irrigation canals

        You can also choose from several preconfigured river groups:

        - ``"a"``: rivers and canals (``0`` - ``10``)
        - ``"A"``: rivers and canals except river-lakes (``1`` - ``10``)
        - ``"r"``: permanent rivers (``0`` - ``4``)
        - ``"R"``: permanent rivers except river-lakes (``1`` - ``4``)
        - ``"i"``: intermittent rivers (``5`` - ``7``)
        - ``"c"``: canals (``8`` - ``10``)

    map_scale : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\ **+w**\ *length*.
        Draw a simple map scale centered on the reference point specified.
    box
        Draw a background box behind the map scale or rose. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    borders : int, str, or list
        *border*\ [/*pen*].
        Draw political boundaries. Specify the type of boundary and
        [optionally] append pen attributes [Default is ``"0.25p,black,solid"``].

        Choose from the list of boundaries below. Pass a list to ``borders`` to
        use multiple arguments.

        - ``1``: national boundaries
        - ``2``: state boundaries within the Americas
        - ``3``: marine boundaries
        - ``"a"``: all boundaries (``1`` - ``3``)

    water : str
        Select filling "wet" areas.
    shorelines : bool, int, str, or list
        [*level*\ /]\ *pen*.
        Draw shorelines [Default is no shorelines]. Append pen attributes
        [Default is ``"0.25p,black,solid"``] which apply to all four levels.
        To set the pen for a single level, pass a string with *level*\ /*pen*\ ,
        where level is 1-4 and represent coastline, lakeshore, island-in-lake shore,
        and lake-in-island-in-lake shore. Pass a list of *level*\ /*pen*
        strings to ``shorelines`` to set multiple levels. When specific
        level pens are set, those not listed will not be drawn.
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
    {panel}
    {perspective}
    {transparency}
    {verbose}

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
    if not args_in_kwargs(args=["C", "G", "S", "I", "N", "E", "Q", "W"], kwargs=kwargs):
        msg = (
            "At least one of the following parameters must be specified: "
            "lakes, land, water, rivers, borders, dcw, Q, or shorelines."
        )
        raise GMTInvalidInput(msg)

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
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="coast", args=build_arg_list(aliasdict))
