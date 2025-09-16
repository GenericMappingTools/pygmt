"""
Define the Pen class for specifying pen attributes (width, color, style).
"""

from dataclasses import dataclass


@dataclass
class Pen:
    r"""
    A GMT pen specified from three attributes: *width*, *color* and *style*.

    See also :gmt-docs:`cookbook/features.html#specifying-pen-attributes`

    Attributes
    ----------
    width : str or int
        [*width*\ [**c**\|\ **i**\|\ **p**]].
        *Width* is by default measured in points (1/72 of an inch). Append
        **c**, **i**, or **p** to specify pen width in cm, inch, or points,
        respectively. Minimum-thickness pens can be achieved by giving zero
        width. The result is device-dependent but typically means that as you
        zoom in on the feature in a display, the line thickness stays at the
        minimum. Finally, a few predefined pen names can be used: default,
        faint, and {thin, thick, fat}[er\|\ est], and wide.

        +------------+---------+------------+--------+
        +============+=========+============+========+
        | faint      | 0       | thicker    | 1.5p   |
        +------------+---------+------------+--------+
        | default    | 0.25p   | thickest   | 2p     |
        +------------+---------+------------+--------+
        | thinnest   | 0.25p   | fat        | 3p     |
        +------------+---------+------------+--------+
        | thinner    | 0.50p   | fatter     | 6p     |
        +------------+---------+------------+--------+
        | thin       | 0.75p   | fattest    | 10p    |
        +------------+---------+------------+--------+
        | thick      | 1.0p    | wide       | 18p    |
        +------------+---------+------------+--------+

    color : str
        The *color* can be specified in five different ways:

        - Gray. Specify a *gray* shade in the range 0-255 (linearly going
          from black [0] to white [255]).

        - RGB. Specify *r*/*g*/*b*, each ranging from 0-255. Here 0/0/0 is
          black, 255/255/255 is white, 255/0/0 is red, etc. Alternatively,
          you can give RGB in hexadecimal using the *#rrggbb* format.

        - HSV. Specify *hue*-*saturation*-*value*, with the former in the
          0-360 degree range while the latter two take on the range 0-1 [17]_.

        - CMYK. Specify *cyan*/*magenta*/*yellow*/*black*, each ranging
          from 0-100%.

        - Name. Specify one of 663 valid color names. See
          :gmt-docs:`gmtcolors` for a list of all valid names. A very small
          yet versatile subset consists of the 29 choices *white*, *black*, and
          [light\|\ dark]{*red, orange, yellow, green, cyan, blue, magenta,
          gray\|\ grey, brown*\ }. The color names are case-insensitive, so
          mixed upper and lower case can be used (like *DarkGreen*).

    style : str
        [*style*\ [**c**\|\ **i**\|\ **p**]].
        The *style* attribute controls the appearance of the line. Giving
        "dotted" or "." yields a dotted line, whereas a dashed pen is requested
        with "dashed" or "-". Also combinations of dots and dashes, like ".-"
        for a dot-dashed line, are allowed. To override a default style and
        secure a solid line you can specify "solid" for style. The lengths of
        dots and dashes are scaled relative to the pen width (dots has a length
        that equals the pen width while dashes are 8 times as long; gaps
        between segments are 4 times the pen width). For more detailed
        attributes including exact dimensions you may specify
        *string*\ [:*offset*], where *string* is a series of numbers separated
        by underscores. These numbers represent a pattern by indicating the
        length of line segments and the gap between segments. The optional
        *offset* phase-shifts the pattern from the beginning the line [0]. For
        example, if you want a yellow line of width 0.1 cm that alternates
        between long dashes (4 points), an 8 point gap, then a 5 point dash,
        then another 8 point gap, with pattern offset by 2 points from the
        origin, specify ``style="0.1c,yellow,4_8_5_8:2p"``. Just as with pen
        width, the default style units are points, but can also be explicitly
        specified in cm, inch, or points (see *width* discussion above).

    Examples
    --------
    >>> import pygmt

    >>> # 0.5 point wide line of default color and style
    >>> pen = pygmt.param.Pen(width="0.5p")

    >>> # Green line with default width and style
    >>> pen = pygmt.param.Pen(color="green")

    >>> # Dashed, thin red line
    >>> pen = pygmt.param.Pen(width="thin", color="red", style="-")

    >>> # Fat dotted line with default color
    >>> pen = pygmt.param.Pen(width="fat", style=".")

    >>> # Green (in h-s-v) pen, 1 mm thick
    >>> pen = pygmt.param.Pen(width="0.1c", color="120-1-1")

    >>> # Very thin, cyan (in c/m/y/k), dot-dot-dashed line
    >>> pen = pygmt.param.Pen(width="faint", color="100/0/0/0", style="..-")

    >>> # Thick, purple, dashed-dot-dashed border line around some text
    >>> pen = pygmt.param.Pen(width="thick", color="purple", style="-.-")
    >>> print(pen)
    thick,purple,-.-
    >>> fig = pygmt.Figure()
    >>> fig.text(x=1, y=1, region=[0, 2, 0, 2], pen=pen, text=pen)
    >>> fig.show()
    """

    width: str = None
    color: str = None
    style: str = None

    def __str__(self):
        return ",".join(
            str(attr or "") for attr in (self.width, self.color, self.style)
        )
