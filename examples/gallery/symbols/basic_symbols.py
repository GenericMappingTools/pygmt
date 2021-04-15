"""
Basic geometric symbols
-----------------------

The :meth:`pygmt.Figure.plot` method can plot individual geometric symbols
by passing the corresponding shortcuts to the ``style`` parameter. The 14 basic
geometric symbols are shown underneath their corresponding shortcut codes.
"""

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 8, 0, 3], projection="X12c/4c", frame=True)

# define fontstlye for annotations
font = "15p,Helvetica-Bold"

# upper row
y = 2

# use a dash in x direction (-) with a size of 0.9 cm,
# linewidth is set to 2p and the linecolor to "gray40"
x = 1
fig.plot(x=x, y=y, style="-0.9c", pen="2p,gray40")
fig.text(x=x, y=y + 0.6, text="-", font=font)

# use a plus (+) with a size of 0.9,
# linewidth is set to 2p and the linecolor to "gray40"
x += 1
fig.plot(x=x, y=y, style="+0.9c", pen="2p,gray40")
fig.text(x=x, y=y + 0.6, text="+", font=font)

# use a star (a) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" (default) and the
# color fill to "darkorange"
x += 1
fig.plot(x=3, y=y, style="a0.9c", pen="1p,black", color="darkorange")
fig.text(x=x, y=y + 0.6, text="a", font=font)

# use a circle (c) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "darkred"
x += 1
fig.plot(x=4, y=y, style="c0.9c", pen="1p,black", color="darkred")
fig.text(x=x, y=y + 0.6, text="c", font=font)

# use a diamond (d) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "seagreen"
x += 1
fig.plot(x=5, y=y, style="d0.9c", pen="1p,black", color="seagreen")
fig.text(x=x, y=y + 0.6, text="d", font=font)

# use a octagon (g) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "dodgerblue4"
x += 1
fig.plot(x=6, y=y, style="g0.9c", pen="1p,black", color="dodgerblue4")
fig.text(x=x, y=y + 0.6, text="g", font=font)

# use a hexagon (h) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "lightgray"
x += 1
fig.plot(x=7, y=y, style="h0.9c", pen="1p,black", color="lightgray")
fig.text(x=x, y=y + 0.6, text="h", font=font)

# lower row
y = 0.5

# use an inverted triangle (i) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "tomato"
x = 1
fig.plot(x=x, y=y, style="i0.9c", pen="1p,black", color="tomato")
fig.text(x=x, y=y + 0.6, text="i", font=font)

# use pentagon (n) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "lightseagreen"
x += 1
fig.plot(x=x, y=y, style="n0.9c", pen="1p,black", color="lightseagreen")
fig.text(x=x, y=y + 0.6, text="n", font=font)

# use a point (p) with a size of 0.9,
# color fill is set to "lightseagreen"
x += 1
fig.plot(x=3, y=y, style="p0.9c", color="slateblue")
fig.text(x=x, y=y + 0.6, text="p", font=font)

# use square (s) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "gold2"
x += 1
fig.plot(x=4, y=y, style="s0.9c", pen="1p,black", color="gold2")
fig.text(x=x, y=y + 0.6, text="s", font=font)

# use triangle (t) with a size of 0.9,
# linewidth is set to 1p, the linecolor to "black" and the
# color fill to "magenta4"
x += 1
fig.plot(x=5, y=y, style="t0.9c", pen="1p,black", color="magenta4")
fig.text(x=x, y=y + 0.6, text="t", font=font)

# use cross (x) with a size of 0.9,
# linewidth is set to 2p and the linecolor to "gray40"
x += 1
fig.plot(x=6, y=y, style="x0.9c", pen="2p,gray40")
fig.text(x=x, y=y + 0.6, text="x", font=font)

# use a dash in y direction (y) with a size of 0.9,
# linewidth is set to 2p and the linecolor to "gray40"
x += 1
fig.plot(x=7, y=y, style="y0.9c", pen="2p,gray40")
fig.text(x=x, y=y + 0.6, text="y", font=font)

fig.show()
