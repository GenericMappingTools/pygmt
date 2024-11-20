"""
coast - Plot land and water.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["coast"]


@fmt_docstring
@use_alias(
    A="area_thresh",
    B="frame",
    C="lakes",
    D="resolution",
    E="dcw",
    F="box",
    G="land",
    I="rivers",
    J="projection",
    L="map_scale",
    N="borders",
    R="region",
    S="water",
    V="verbose",
    W="shorelines",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def coast(self, **kwargs):
    r"""
    Plot continents, shorelines, rivers, and borders on maps.

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

    Full option list at :gmt-docs:`coast.html`

    {aliases}

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
    resolution : str
        **f**\|\ **h**\|\ **i**\|\ **l**\|\ **c**.
        Select the resolution of the data set to: (**f**\ )ull, (**h**\ )igh,
        (**i**\ )ntermediate, (**l**\ )ow, and (**c**\ )rude.
    land : str
        Select filling of "dry" areas.
    rivers : int, str, or list
        *river*\ [/*pen*].
        Draw rivers. Specify the type of rivers and [optionally] append
        pen attributes [Default is ``"0.25p,black,solid"``].

        Choose from the list of river types below; pass a list to ``rivers``
        to use multiple arguments.

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

        You can also choose from several preconfigured river groups:

        - ``"a"``: All rivers and canals (0-10)
        - ``"A"``: All rivers and canals except river-lakes (1-10)
        - ``"r"``: All permanent rivers (0-4)
        - ``"R"``: All permanent rivers except river-lakes (1-4)
        - ``"i"``: All intermittent rivers (5-7)
        - ``"c"``: All canals (8-10)

    map_scale : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\ **+w**\ *length*.
        Draw a simple map scale centered on the reference point specified.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the
        map scale or rose. Alternatively, specify a different pen with
        **+p**\ *pen*. Add **+g**\ *fill* to fill the scale panel [Default is
        no fill]. Append **+c**\ *clearance* where *clearance* is either gap,
        xgap/ygap, or lgap/rgap/bgap/tgap where these items are uniform,
        separate in x- and y-direction, or individual side spacings between
        scale and border. Append **+i** to draw a secondary, inner border as
        well. We use a uniform gap between borders of 2p and the
        :gmt-term:`MAP_DEFAULTS_PEN` unless other values are specified. Append
        **+r** to draw rounded rectangular borders instead, with a 6p corner
        radius. You can override this radius by appending another value.
        Finally, append **+s** to draw an offset background shaded region.
        Here, *dx/dy* indicates the shift relative to the foreground frame
        [Default is ``"4p/-4p"``] and shade sets the fill style to use for
        shading [Default is ``"gray50"``].
    borders : int, str, or list
        *border*\ [/*pen*].
        Draw political boundaries. Specify the type of boundary and
        [optionally] append pen attributes [Default is ``"0.25p,black,solid"``].

        Choose from the list of boundaries below. Pass a list to ``borders`` to
        use multiple arguments.

        - ``1``: National boundaries
        - ``2``: State boundaries within the Americas
        - ``3``: Marine boundaries
        - ``"a"``: All boundaries (1-3)

    water : str
        Select filling "wet" areas.
    shorelines : int, str, or list
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
        Append one or more comma-separated countries using the 2-character
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
    kwargs = self._preprocess(**kwargs)
    if not args_in_kwargs(args=["C", "G", "S", "I", "N", "E", "Q", "W"], kwargs=kwargs):
        raise GMTInvalidInput(
            """At least one of the following parameters must be specified:
            lakes, land, water, rivers, borders, dcw, Q, or shorelines"""
        )
    with Session() as lib:
        lib.call_module(module="coast", args=build_arg_list(kwargs))
