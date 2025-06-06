"""
GMT logo
========

The :meth:`pygmt.Figure.logo` method allows to place the GMT logo on a figure.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 10, 0, 2], projection="X6c", frame=True)

# Add the GMT logo in the Top Right (TR) corner of the current plot, scaled up to be 3
# centimeters wide and offset by 0.3 cm in x-direction and 0.6 cm in y-direction.
fig.logo(position="jTR+o0.3c/0.6c+w3c")

fig.show()
