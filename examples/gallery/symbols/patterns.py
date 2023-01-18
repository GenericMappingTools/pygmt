r"""
Bit and Hachure Patterns
------------------------

TODO

"""

import pygmt

y = 13

fig = pygmt.Figure()
fig.basemap(
    region=[0, 12, 0, 12],
    projection="X12c",
    frame="rlbt+glightgray+tBit and Hachure Patterns",
)

for pattern in [
    # To use a pattern as fill append "p" and the number of the desired
    # pattern. By default, the pattern is plotted in black and white
    # with a resolution of 300 dpi
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
        justify="ML",  # justification of the text is MiddleLeft
    )

fig.show()
