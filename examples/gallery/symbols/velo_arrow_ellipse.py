"""
Velocity arrows and confidence ellipse
--------------------------------------

The :meth:`pygmt.Figure.velo` method can be used to plot mean velocity arrow
and confidence ellipse on a map.
The example below, should make big red arrows with green ellipses,
outlined in red. Note that the 39% confidence scaling will give an ellipse
which fits inside a rectangle of dimension Esig by Nsig.
"""

import pandas as pd
import pygmt

fig = pygmt.Figure()
df = pd.DataFrame(
    data={
        "Long.": [0, -8, 0, -5, 5, 0],
        "Lat.": [-8, 5, 0, -5, 0, -5],
        "Evel": [0, 3, 4, 6, -6, 6],
        "Nvel": [0, 3, 6, 4, 4, -4],
        "Esig": [4, 0, 4, 6, 6, 6],
        "Nsig": [6, 0, 6, 4, 4, 4],
        "CorEN": [0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
        "SITE": ["4x6", "3x3", "NaN", "6x4", "-6x4", "6x-4"],
    }
)
fig.velo(
    data=df,
    region=[-10, 8, -10, 6],
    pen="0.6p,red",
    uncertainty_color="lightblue1",
    line=True,
    scaling="e0.2/0.39/18",
    frame=["WSne", "2g2f"],
    projection="x0.8c",
    vector="0.3c+p1p+e+gred",
)

fig.show()
