"""
3. Figure elements
===============
The figure shows the naming of figure elements in PyGMT. 

* :meth:`pygmt.Figure`: having a number of plotting methods. Every plot or map
must start with the creation of a :meth:`pygmt.Figure` instance
* ``frame``: setting map boundary (**WSNE** or **wsne**), annonate and grid
(**afg**), axis label (**+l**) and title (**+t**) in
:meth:`pygmt.Figure.basemap`. The detail examples can be found at
`frame and axes attributes<https://www.pygmt.org/latest/tutorials/basics/
frames.html>`_.
* :meth:`pygmt.Figure.plot`: plotting the lines or symbols based on ``pen``
or ``style`` parameters, respectively
* :meth:`pygmt.Figure.text`: plottong text strings with ``font`` parameter
which adjusts the fontsize, fontstyle and color.
* :meth:`pygmt.Figure.legend`: showing the naming of lines or symbols while
the ``label`` given in :meth:`pygmt.Figure.plot`
* :meth:`pygmt.Figure.show`: previewing the figure you plotted
"""
import pygmt

fig = pygmt.Figure()


x = range(0, 11, 2)
y_1 = [10, 11, 15, 8, 9, 13]
y_2 = [4, 5, 6, 3, 5, 5]

fig.basemap(
    region=[0, 10, 0, 20],
    projection="X10c/8c",
    frame=["WSne+tTitle", "xa2f1g2+lxlabel", "ya5f1g5+lylabel"],
)
fig.plot(x=x, y=y_1, style="t0.3c", label="fig.plot (style)")
fig.plot(x=x, y=y_2, pen="1.5p,red", label="fig.plot (pen)")
# ============Figure
fig.text(x=12, y=22, text="Figure", font="12p,2,darkblue", justify="TC", no_clip=True)
fig.text(x=12, y=20.5, text="pygmt.Figure()", font="10p,8", justify="TC", no_clip=True)
# ============Title
fig.text(x=6, y=22, text='frame="+tTitle"', font="10p,8", justify="TL", no_clip=True)
# ============xlabel
fig.text(x=5, y=-3, text='frame="x+lxlabel"', font="10p,8", justify="CM", no_clip=True)
# ============ylabel
fig.text(
    x=-1.7,
    y=10,
    text='frame="y+lylabel"',
    font="10p,8",
    justify="CM",
    angle=90,
    no_clip=True,
)
# ============x-majorticks
fig.plot(x=10, y=-0.2, style="c1c", pen="2p,darkblue", no_clip=True)
fig.text(
    x=10, y=-1.4, text="Annonate", font="12p,2,darkblue", justify="TC", no_clip=True
)
fig.text(x=10, y=-2.6, text='frame="xa2"', font="10p,8", justify="CM", no_clip=True)
# ============y-majorticks
fig.plot(x=-0.2, y=20, style="c1c", pen="2p,darkblue", no_clip=True)
fig.text(
    x=0, y=23.2, text="Annonate", font="12p,2,darkblue", justify="TC", no_clip=True
)
fig.text(x=0, y=21.7, text='frame="ya5"', font="10p,8", justify="CM", no_clip=True)
# ============x-minorticks
fig.plot(x=1, y=-0.2, style="c0.7c", pen="2p,darkblue", no_clip=True)
fig.text(x=1, y=-1.4, text="Frame", font="12p,2,darkblue", justify="TC", no_clip=True)
fig.text(x=1, y=-2.6, text='frame="xf1"', font="10p,8", justify="CM", no_clip=True)
# ============y-minorticks
fig.plot(x=0, y=2, style="c0.7c", pen="2p,darkblue", no_clip=True)
fig.text(x=-0.2, y=1, text='frame="yf1"', font="10p,8", justify="MR", no_clip=True)
# ============grid
fig.plot(x=2, y=15, style="c0.5c", pen="2p,darkblue")
fig.text(x=2, y=16, text="Grid", font="12p,2,darkblue", justify="BC")
fig.text(x=2, y=17.5, text='frame="xg2"', font="10p,8", justify="BC")
# ============map boundaries
fig.plot(x=10, y=9, style="c0.5c", pen="2p,darkblue", no_clip=True)
fig.text(
    x=10.2, y=8, text="Map Boundary", font="12p,2,darkblue", justify="BL", no_clip=True
)
fig.text(x=10.2, y=7, text='frame="WSne"', font="10p,8", justify="BL", no_clip=True)
# ============fig.plot
fig.plot(x=6, y=8, style="c0.7c", pen="2p,darkblue")
fig.plot(x=4, y=6, style="c0.7c", pen="2p,darkblue")
fig.text(x=5, y=6, text="fig.plot()", font="10p,8", justify="BL")
# ============Legend
fig.legend()
fig.text(x=7.5, y=17, text="Legend", font="12p,2,darkblue", justify="TL", no_clip=True)
fig.text(x=7.5, y=15.8, text="fig.legend()", font="10p,8", justify="TL", no_clip=True)

fig.show()
