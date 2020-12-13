"""
Cartesian
=========

``Xwidth/[height]``: Give the ``width`` of the figure ``width`` and the optional argument ``height``.
"""
import pygmt

fig = pygmt.Figure()
# ``region`` sets the x and y ranges or the Cartesian figure.
# The argument ``WSne`` is passed to ``frame`` to put axis labels only on the left and bottom axes.
# The ``x`` and ``y`` parameters are used to plot lines on the figure.
fig.plot(
    x=[3, 9, 2],
    y=[4, 9, 37],
    pen="3p,red",
    region=[0, 10, 0, 50],
    projection="X15c/10c",
    frame=["af", "WSne"],
)
fig.show()
