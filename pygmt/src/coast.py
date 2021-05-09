"""
coast - Plot land and water.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    A="area_thresh",
    C="lakes",
    B="frame",
    D="resolution",
    E="dcw",
    I="rivers",
    L="map_scale",
    N="borders",
    W="shorelines",
    G="land",
    S="water",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def coast(self, **kwargs):
    r"""
    Plot continents, shorelines, rivers, and borders on maps

    Plots grayshaded, colored, or textured land-masses [or water-masses] on
    maps and [optionally] draws coastlines, rivers, and political
    boundaries.  Alternatively, it can (1) issue clip paths that will
    contain all land or all water areas, or (2) dump the data to an ASCII
    table. The data files come in 5 different resolutions: (**f**)ull,
    (**h**)igh, (**i**)ntermediate, (**l**)ow, and (**c**)rude. The full
    resolution files amount to more than 55 Mb of data and provide great
    detail; for maps of larger geographical extent it is more economical to
    use one of the other resolutions. If the user selects to paint the
    land-areas and does not specify fill of water-areas then the latter
    will be transparent (i.e., earlier graphics drawn in those areas will
    not be overwritten).  Likewise, if the water-areas are painted and no
    land fill is set then the land-areas will be transparent.

    A map projection must be supplied.

    Full option list at :gmt-docs:`coast.html`

    {aliases}

    Parameters
    ----------
    {J}
    {R}
    area_thresh : int, float, or str
        *min_area*\ [/*min_level*/*max_level*][**+a**\[**g**\|\ **i**]\
        [**s**\|\ **S**][**+l**\|\ **r**][**+p**\ *percent*].
        Features with an area smaller than *min_area* in km\ :sup:`2` or of
        hierarchical level that is lower than *min_level* or higher than
        *max_level* will not be plotted.
    {B}
    lakes : str or list
        *fill*\ [**+l**\|\ **+r**].
        Set the shade, color, or pattern for lakes and river-lakes. The
        default is the fill chosen for wet areas set by the ``water``
        parameter. Optionally, specify separate fills by appending
        **+l** for lakes or **+r** for river-lakes, and passing multiple
        strings in a list.
    resolution : str
        **f**\|\ **h**\|\ **i**\|\ **l**\|\ **c**.
        Selects the resolution of the data set to: (**f**\ )ull,
        (**h**\ )igh, (**i**\ )ntermediate, (**l**\ )ow,
        and (**c**\ )rude.
    land : str
        Select filling or clipping of "dry" areas.
    rivers : int or str or list
        *river*\ [/*pen*].
        Draw rivers. Specify the type of rivers and [optionally] append
        pen attributes [Default pen is width = default, color = black,
        style = solid].

        Choose from the list of river types below; pass a list to
        ``rivers`` to use multiple arguments.

        0 = Double-lined rivers (river-lakes)

        1 = Permanent major rivers

        2 = Additional major rivers

        3 = Additional rivers

        4 = Minor rivers

        5 = Intermittent rivers - major

        6 = Intermittent rivers - additional

        7 = Intermittent rivers - minor

        8 = Major canals

        9 = Minor canals

        10 = Irrigation canals

        You can also choose from several preconfigured river groups:

        a = All rivers and canals (0-10)

        A = All rivers and canals except river-lakes (1-10)

        r = All permanent rivers (0-4)

        R = All permanent rivers except river-lakes (1-4)

        i = All intermittent rivers (5-7)

        c = All canals (8-10)
    map_scale : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*.
        Draws a simple map scale centered on the reference point specified.
    borders : int or str or list
        *border*\ [/*pen*].
        Draw political boundaries. Specify the type of boundary and
        [optionally] append pen attributes [Default pen is width = default,
        color = black, style = solid].

        Choose from the list of boundaries below. Pass a list to
        ``borders`` to use multiple arguments.

        1 = National boundaries

        2 = State boundaries within the Americas

        3 = Marine boundaries

        a = All boundaries (1-3)
    water : str
        Select filling or clipping of "wet" areas.
    {U}
    shorelines : int or str or list
        [*level*\ /]\ *pen*.
        Draw shorelines [Default is no shorelines]. Append pen attributes
        [Default is width = default, color = black, style = solid] which
        apply to all four levels. To set the pen for a single level,
        pass a string with *level*\ /*pen*\ , where level is
        1-4 and represent coastline, lakeshore, island-in-lake shore, and
        lake-in-island-in-lake shore. Pass a list of *level*\ /*pen*
        strings to ``shorelines`` to set multiple levels. When specific
        level pens are set, those not listed will not be drawn.
    dcw : str or list
        *code1,code2,…*\ [**+l**\|\ **L**\ ][**+g**\ *fill*\ ]
        [**+p**\ *pen*\ ][**+z**].
        Select painting or dumping country polygons from the
        `Digital Chart of the World
        <https://en.wikipedia.org/wiki/Digital_Chart_of_the_World>`__.
        Append one or more comma-separated countries using the 2-character
        `ISO 3166-1 alpha-2 convention
        <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`__.
        To select a state of a country (if available), append
        .\ *state*, (e.g, US.TX for Texas).  To specify a whole continent,
        prepend **=** to any of the continent codes (e.g. =EU for Europe).
        Append **+p**\ *pen* to draw polygon outlines
        (default is no outline) and **+g**\ *fill* to fill them
        (default is no fill). Append **+l**\|\ **+L** to =\ *continent* to
        only list countries in that continent; repeat if more than one
        continent is requested.
    {XY}
    {c}
    {p}
    {t}
    {V}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if not args_in_kwargs(args=["C", "G", "S", "I", "N", "E", "Q", "W"], kwargs=kwargs):
        raise GMTInvalidInput(
            """At least one of the following parameters must be specified:
            lakes, land, water, rivers, borders, dcw, Q, or shorelines"""
        )
    with Session() as lib:
        lib.call_module("coast", build_arg_string(kwargs))
