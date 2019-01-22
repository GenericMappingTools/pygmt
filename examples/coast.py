"""
Coastlines
----------

Use :meth:`gmt.Figure.coast` to display coastlines.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="g", projection='W6i', frame=True, land='black', water='skyblue'
)
fig.show()
