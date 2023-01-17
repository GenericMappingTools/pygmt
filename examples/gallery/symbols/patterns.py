r"""
Bit and Hachure Patterns
------------------------

TODO

"""

import pygmt

y = 11

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 10],
    projection="X10c",
    frame="rlbt+glightgray+tBit and Hachure Patterns",
)

for pattern in [
    # To use a pattern as fill append "p" and the number of the desired
    # patten. By default, the pattern is plotted in black and white with
    # a resolution of 300 dpi
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
    # Plot a square with a pattern as fill
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
        justify="ML",  # justification of text is MiddelLeft
    )

fig.show()
