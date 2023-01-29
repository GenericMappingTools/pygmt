r"""
Bit and Hachure Patterns
------------------------

The ``fill`` parameter can be used to fill polygons with bit or hachure patterns.
This includes symbols (:meth:`pygmt.Figure.plot`), histogram bars or sectors
(:meth:`pygmt.Figure.histogram` or :meth:`pygmt.Figure.rose`), and anomalies
(:meth:`pygmt.Figure.wiggle`) as well as land and water masses
(:meth:`pygmt.Figure.coast`):

**P**\ |**p**\ *pattern*\ [**+b**\ *color*\ ][**+f**\ *color*\ ][**+r**\ *dpi*]

TODO

An overview of all 90 predefined bit and hachure patterns can by found at
https://docs.generic-mapping-tools.org/latest/cookbook/predefined-patterns.html.
"""


import pygmt

y = 13

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 12],
    projection="X10c",
    frame="rlbt+glightgray+tBit and Hachure Patterns",
)

# To use a pattern as fill append "p" and the number of the desired
# pattern. By default, the pattern is plotted in black and white
# with a resolution of 300 dpi
for pattern in [
    # Plot a hachted pattern via pattern number 8
    "p8",
    # Plot a dotted pattern via pattern number 19
    "p19",
    # Set the background color ("+b") to "red3"
    # and the foreground color ("+f") to "lightgray"
    "p19+bred3+flightbrown",
    # Invert the pattern by using a capitalized "P"
    "P19+bred3+flightbrown",
    # Change the resolution ("+r") to 100 dpi
    "p19+bred3+flightbrown+r100",
    # Make the background transparent by not giving a color after "+b";
    # works analogous for the foreground
    "p19+b+flightbrown+r100",
]:
    y -= 2
    # Plot a square with the pattern as fill
    fig.plot(
        x=2,
        y=y,
        style="s2c",  # square with a width of 2 centimeters
        pen="1p,black",  # 1 point thick, black outline
        fill=pattern,
    )
    # Add a description of the pattern
    fig.text(
        x=4,
        y=y,
        text=pattern,
        font="Courier-Bold",
        justify="ML",  # justification of the text is Middle Left
    )

fig.show()
