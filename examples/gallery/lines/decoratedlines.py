"""
Decorated lines
---------------
Use ``style`` parameter with argument ``"~"`` in :meth:`pygmt.Figure.method`
Similarity to line fronts, for details see
:doc:`Line styles example </gallery/lines/linesfronts>`
Point out what is different
Also add link in example Line fronts
Hybrid of fronts and quoted lines
Unclear `"+a"` does nothing, should change angle similar to quoted lines
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
for frontstyle in [
    # xxx
    "~d1c:+sc0.5c",
    # xxx
    "~d1c:+sc0.5c+p1p,blue",
    # xxx
    "~d1c:+sc0.5c+p1p,blue,-",
    # xxx
    "~d1c:+sc0.5c+glightblue",
    # xxx
    "~d1c:+sc0.5c+glightblue+p1p,blue",
    # xxx
    "~d1c:+sc0.5c+gp8+p1p,blue",
    # xxx
    "~d1c:+st0.5c+gtan+p1p,black",
    # xxx
    "~d0.4c:+si0.3c+gtan+p1p,black",
    # xxx
    "~d1c:+ss0.7c+gtan+p1p,black",
    # xxx
    "~d1c:+sd0.5c+gtan+p1p,black+n-0.2c/0.1c",
    # xxx
    "~n6:+sn0.5c+gtan+p1p,black",
    # xxx
    "~N6:+sh0.5c+gtan+p1p,black",
    # xxx
    "~d1c:+sg0.5c+gtan+p1p,black+i",
    # xxx analog N+1 für Ende
    "~N-1:+sp0.2c+gblack",    
    # xxx
    "~d1c:+sa0.5c+ggold+p1p,black",
    # xxx
    "~d1c:+sx0.5c+p2p,red",
    # xxx
    "~d0.5c:+sy0.5c+p5p,brown",
    # xxx
    "~d1c:+sksquaroid/0.5c+ggray+p1p,black",
]:
    y = y - 1.2  # Move current line down
    fig.plot(x=x, y=y, pen="1.25p,black")
    fig.text(
        x=x[-1],
        y=y[-1],
        text=frontstyle,
        font="Courier-Bold",
        justify="ML",
        offset="0.75c/0c",
    )

fig.show()
