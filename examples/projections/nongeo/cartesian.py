"""
Cartesian
=========

``Xwidth/[height]``: Give the ``width`` of the figure ``width`` and the optional argument ``height``.
"""
import pygmt

fig = pygmt.Figure()
# ``region`` sets the x and y ranges or the Cartesian figure.
# The argument ``WSne`` is passed to ``frame`` to put axis labels only on the left and bottom axes.
fig.basemap(projection="X15c/10c", region=[0, 10, 0, 50], frame=["af", "WSne"])
# ``fig.plot()`` is used to plot lines on the figure.
fig.plot(x=[3, 9, 2], y=[4, 9, 37], pen="3p,red")
fig.show()
