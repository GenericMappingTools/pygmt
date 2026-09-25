r"""
Text symbols
------------
The :meth:`pygmt.Figure.plot` method allows to plot text symbols. Text is
normally placed with the :meth:`pygmt.Figure.text` method but there are times
we wish to treat a character or even a string as a plottable symbol.
A text symbol can be drawn by passing **l**\ *size*\ **+t**\ *string* to
the ``style`` parameter where *size* defines the size of the text symbol
(note: the size is only approximate; no individual scaling is done for
different characters) and *string* can be a letter or a text string
(less than 256 characters). Optionally, you can append
**+f**\ *font,outlinecolor* to select a particular font [Default is
:gmt-term:`FONT_ANNOT_PRIMARY`] and outline color [Default is black] as well
as **+j**\ *justify* to change the justification [Default is CM]. The fill
color of the text symbols can be set with the ``fill`` parameter, and the
outline width can be customized with the ``pen`` parameter.
For all supported octal codes and fonts see the GMT cookbook
:gmt-docs:`cookbook/octal-codes.html` and
:gmt-docs:`cookbook/postscript-fonts.html`.
"""

import pygmt

fig = pygmt.Figure()

fig.basemap(region=[0, 8, 0, 3], projection="X12c/4c", frame=True)

pen = "1.5p"
# plot an uppercase "A" of size 3.5c, color fill is set to "dodgerblue3"
fig.plot(x=1, y=1.5, style="l3.5c+tA", fill="dodgerblue3", pen=pen)
# plot an "asterisk" of size 3.5c, color fill is set to "red3"
fig.plot(x=2.5, y=1, style="l3.5c+t*", fill="red3", pen=pen)
# plot an uppercase "Z" of size 3.5c and use the "Courier-Bold" font,
# color fill is set to "seagreen"
fig.plot(x=4, y=1.5, style="l3.5c+tZ+fCourier-Bold", fill="seagreen", pen=pen)
# plot a lowercase "s" of size 3.5c and use the "Times-Italic" font,
# color fill is set to "gold"
fig.plot(x=5.5, y=1.5, style="l3.5c+ts+fTimes-Italic", fill="gold", pen=pen)
# plot the pi symbol (\160 is octal code for pi) of size 3.5c, for this use
# the "Symbol" font, the outline color of the symbol is set to
# "darkorange", the color fill is set to "magenta4"
fig.plot(x=7, y=1.5, style="l3.5c+t\160+fSymbol,darkorange", fill="magenta4", pen=pen)

fig.show()
