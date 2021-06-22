"""
Custom symbols
-----------------------

The :meth:`pygmt.Figure.plot` method can plot individual custom symbols
by passing the corresponding symbol name together with the **k** shortcut to
the ``style`` parameter. In total 41 custom symbols are already included of
which the following plot shows five examplary ones. The symbols are shown
underneath their corresponding names. For the remaining symbols see
:gmt-docs:`cookbook/custom-symbols.html`
"""

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 8, 0, 3], projection="X12c/4c", frame=True)

# define pen and fontstlye for annotations
pen = "1p,black"
font = "15p,Helvetica-Bold"

y = 1.25

fig.plot(x=1, y=y, style="kvolcano/60p", pen=pen, color="seagreen")
fig.text(x=1, y=y + 1.25, text="volcano", font=font)

fig.plot(x=2.5, y=y, style="kastroid/60p", pen=pen, color="red3")
fig.text(x=2.5, y=y + 1.25, text="astroid", font=font)

fig.plot(x=4, y=y, style="kflash/60p", pen=pen, color="darkorange")
fig.text(x=4, y=y + 1.25, text="flash", font=font)

fig.plot(x=5.5, y=y, style="kstar4/60p", pen=pen, color="dodgerblue4")
fig.text(x=5.5, y=y + 1.25, text="star4", font=font)

fig.plot(x=7, y=y, style="khurricane/60p", pen=pen, color="magenta4")
fig.text(x=7, y=y + 1.25, text="hurricane", font=font)

fig.show()
