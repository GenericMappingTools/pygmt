"""
Cartesian linear
================

``Xwidth/[height]``: Give the ``width`` of the figure and the optional argument ``height``.
"""
import pygmt

fig = pygmt.Figure()
fig.plot(
    # The ``x`` and ``y`` parameters are used to plot lines on the figure.
    x=[3, 9, 2],
    y=[4, 9, 37],
    pen="3p,red",
    # ``region`` sets the x and y ranges or the Cartesian figure.
    region=[0, 10, 0, 50],
    # The argument ``WSne`` is passed to ``frame`` to put axis labels only on the left and bottom axes.
    projection="X15c/10c",
    frame=["af", "WSne"],
)
fig.show()
