"""
Coastlines
----------

Use :meth:`gmt.Figure.coast` to display coastlines.
"""
import gmt

fig = gmt.Figure()
fig.coast(
    region="g", projection='W6i', frame=True, land='black', water='skyblue'
)
fig.show()
