r"""
Text symbols
------------
The :meth:`pygmt.Figure.plot` method allows to plot text symbols.
A text symbol can be drawn by passing **l**\ *size*\ **+t**\ *string* to
the ``style`` parameter where *size* defines the size of the text symbol
(note: the size is only approximate; no individual scaling is done for
different characters) and *string* can be a letter or a text string
(less than 256 characters). Optionally, you can append **+f**\ *font* select
a particular font [Default is FONT_ANNOT_PRIMARY] as well as **+j**\ *justify*
to change the justification [Default is CM]. Outline and fill color of the
text symbols can be customized via the ``pen`` and ``color`` parameters,
respectively.
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
