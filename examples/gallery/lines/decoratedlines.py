"""
Decorated lines
---------------
To draw so-called *decorated lines*, i.e., lines with symbols,
use the ``style`` parameter of :meth:`pygmt.Figure.plot`
with argument ``"~"``. There are similarity to line fronts
(see :doc:`Line styles example </gallery/lines/linesfronts>`).
Point out what is different
Also add link in example Line fronts
Hybrid of fronts and quoted lines
Unclear `"+a"` does nothing, should change angle simliar to
quoted lines
Change base line via ``pen`` parameter, see the
:doc:`Line styles example </gallery/lines/linestyles>`.
Also, custom symbols can be used, see
:doc:`Custom symbols example </gallery/symbols/custom_symbols>`.
For more modifications, see upstream GMT documentation at xyz
TODO - nice formulation
"""


import numpy as np
import pygmt

# Generate a two-point line for plotting
x = np.array([1, 4])
y = np.array([24, 24])

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 24],
    projection="X15c",
    frame="+tDecorated Lines",
)

# Plot different decorated lines
for decoline in [
    # Line with circle ("+sc") of 0.5 centimeters radius in distance of
    # 1 centimeter
    "~d1c:+sc0.5c",
    # Adjust thickness, color, and style of the outline via "+p"
    # Here, we plot a 1-point thick, blue, dashed outline
    "~d1c:+sc0.5c+p1p,blue,-",
    # Add a fill color using "+g" with the desired color
    "~d1c:+sc0.5c+glightblue",
    # To use a pattern as fill by append "p" and give the pattern number
    "~d1c:+sc0.5c+gp8+p1p,blue",
    # Line with tringles ("t")
    "~d1c:+st0.5c+gtan+p1p,black",
    # Line with inverse triangles with a size of 0.3 centimeters in a
    # distance of 0.4 centimeters
    "~d0.4c:+si0.3c+gtan+p1p,black",
    # Line with squares ("s") with a size of 0.7 centimeters in a distance of
    # 1 centimeter
    "~d1c:+ss0.7c+gtan+p1p,black",
    # Shift symbols using "+n" in x and y directions relative to the base line
    "~d1c:+sd0.5c+gtan+p1p,black+n-0.2c/0.1c",
    # Give the number of equally spaced symbols by using "n" instead of "d"
    "~n6:+sn0.5c+gtan+p1p,black",
    # Use upper-case "N" to have symbols at start and end of the line
    "~N6:+sh0.5c+gtan+p1p,black",
    # Suppress the base line by appending "+i"
    "~d1c:+sg0.5c+gtan+p1p,black+i",
    # To only plot a symbol at the start of the line use "N-1"
     "~N-1:+sp0.2c+gblack",
    # To only plot a symbol at the end of the line use "N+1"
    "~N+1:+sp0.2c+gblack",
    # Line with stars ("a")
    "~d1c:+sa0.5c+ggold+p1p,black",
    # Line with crosses ("x")
    "~d1c:+sx0.5c+p2p,red",
    # Line with (vertical) lines or bars ("y")
    "~d0.5c:+sy0.5c+p5p,brown",
    # Use custom symbol ("k") "squaroid" with a size of 0.5 centimeters
    "~d1c:+sksquaroid/0.5c+ggray+p1p,black",
]:
    y = y - 1.2  # Move current line down
    fig.plot(x=x, y=y, style=decoline, pen="1.25p,black")
    fig.text(
        x=x[-1],
        y=y[-1],
        text=decoline,
        font="Courier-Bold",
        justify="ML",
        offset="0.75c/0c",
    )

fig.show()
