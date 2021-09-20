"""
Vertical or horizontal bar
--------------------------
The :meth:`pygmt.Figure.plot` method can plot vertical (**b**) or
horizontal (**B**) bars by passing the corresponding shortcut to
the ``style`` parameter.
"""

import pandas as pd
import pygmt

fig = pygmt.Figure()

pygmt.makecpt(cmap="roma", series=[0, 4, 1])

with fig.subplot(
    nrows=2,
    ncols=2,
    subsize=("8c", "4c"),
    frame=["ag"],
    sharey=True,
    sharex=True,
    margins=["0.5c", "0.75c"],
):

    pen = "1.5p"
    with fig.set_panel(panel=0):
        color = "skyblue"
        fig.basemap(region=[0, 4, 0, 3], frame="+tvertical")
        fig.plot(x=1, y=2, style="b0.5c", color=color, pen=pen)
        fig.plot(x=2, y=2.5, style="b1c", color=color, pen=pen)
        fig.plot(x=3, y=2.5, style="b0.75c+b1", color=color, pen=pen)

    with fig.set_panel(panel=1):
        color = "tomato"
        fig.basemap(region=[0, 4, 0, 3], frame="+thorizontal")
        fig.plot(x=1.5, y=0.5, style="B0.75c", color=color, pen=pen)
        fig.plot(x=3, y=1.5, style="B1c", color=color, pen=pen)
        fig.plot(x=3.5, y=2.5, style="B0.5c+b2", color=color, pen=pen)

    # generate dataframe for plotting multi-band bars
    data = {
        "x1": [0.25, 1.25],
        "y": [1, 2],
        "x2": [1, 0.5],
        "x3": [0.75, 1.25],
        "x4": [1.25, 0.75],
    }
    df = pd.DataFrame(data=data)

    with fig.set_panel(panel=2):
        fig.basemap(region=[0, 4, 0, 3], frame='+t"stacked bars"')
        fig.plot(data=data, style="B0.75c+i4", cmap=True, pen=pen)

    with fig.set_panel(panel=3):
        fig.basemap(region=[0, 4, 0, 3], frame='+t"split bars"')
        fig.plot(data=data, style="B1c+i4+s4", cmap=True, pen=pen)

fig.show()
