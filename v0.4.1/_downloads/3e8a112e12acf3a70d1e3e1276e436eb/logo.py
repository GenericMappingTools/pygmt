"""
Logo
----

The :meth:`pygmt.Figure.logo` method allows to place the GMT logo on a map.
"""

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 10, 0, 2], projection="X6c", frame=True)

# add the GMT logo in the Top Right corner of the current map,
# scaled up to be 3 cm wide and offset by 0.3 cm in X direction
# and 0.6 cm in Y direction.
fig.logo(position="jTR+o0.3c/0.6c+w3c")

fig.show()
