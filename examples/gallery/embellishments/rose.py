"""
Rose diagram
------------

The :meth:`pygmt.Figure.rose` method can plot windrose diagrams or polar histograms.
"""

import pygmt

fig = pygmt.Figure()

# use the remote file fractures_06.txt which contains a compilation of fracture
# lengths and directions as digitized from geological maps
fig.rose(
    data="@fractures_06.txt",
    diameter="7.5c",
    columns=[1, 0],
    sector="10r",
    norm=True,
    region=[0, 1, 0, 360],
    color="red3",
    frame=["x0.2g0.2", "y30g30", "+glightgray"],
    pen="1p",
)

fig.show()
