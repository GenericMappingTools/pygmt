"""
Text symbols
------------
The :meth:`pygmt.Figure.plot` method allows to plot text symbols.
"""

import pygmt

fig = pygmt.Figure()

fig.basemap(region=[0, 8, 0, 3], projection="X12c/4c", frame=True)

pen = "1.5p"
fig.plot(x=1, y=1.5, style="l3.5c+tA", color="dodgerblue3", pen=pen)
fig.plot(x=2.5, y=1, style="l3.5c+t*", color="red3", pen=pen)
fig.plot(
    x=4, y=1.5, style="l3.5c+tZ+f12p,Courier-Bold,black", color="seagreen3", pen=pen
)
fig.plot(x=5.5, y=1.5, style="l3.5c+ts+f12p,Times-Italic,black", color="gold", pen=pen)
fig.plot(x=7, y=1.5, style="l3.5c+t\160+fSymbol", color="magenta4", pen=pen)

fig.show()
