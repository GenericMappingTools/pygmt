"""
Legend
======

The :meth:`pygmt.Figure.legend` method can automatically create a legend for
symbols plotted using :meth:`pygmt.Figure.plot`. A legend entry is only added
when the ``label`` parameter is used to state the desired text. Optionally,
to adjust the legend, users can append different modifiers. A list of all
available modifiers can be found at :gmt-docs:`gmt.html#l-full`. To create a
multiple-column legend **+N** is used with the desired number of columns.
For more complicated legends, users may want to write an ASCII file with
instructions for the layout of the legend items and pass it to the ``spec``
parameter of :meth:`pygmt.Figure.legend`. For details on how to set up such a
file, please see the GMT documentation at :gmt-docs:`legend.html#legend-codes`.
In this example the same plot is created twice, first with a vertical (default)
and then with a horizontal legend.
"""

# %%
import pygmt

fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Left: Vertical legend (one column, default)
fig.basemap(projection="x2c", region=[0, 7, 3, 7], frame=["WSne", "af"])

fig.plot(
    data="@Table_5_11.txt",
    style="c0.40c",
    fill="lightgreen",
    pen="faint",
    label="Apples",
)
fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", label="My lines")
fig.plot(data="@Table_5_11.txt", style="t0.40c", fill="orange", label="Oranges")

fig.legend(position="JTR+jTR+o0.2c", box=True)

fig.shift_origin(xshift="+w1c")

# -----------------------------------------------------------------------------
# Right: Horizontal legend (here three columns)
fig.basemap(projection="x2c", region=[0, 7, 3, 7], frame=["wSne", "af"])

fig.plot(
    data="@Table_5_11.txt",
    style="c0.40c",
    fill="lightgreen",
    pen="faint",
    # +N sets the number of columns corresponding to the given number
    label="Apples+N3",
)
fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", label="My lines")
fig.plot(data="@Table_5_11.txt", style="t0.40c", fill="orange", label="Oranges")

# For multi-column legends users have to provide the width via +w, here it is
# set to 6.5 centimeters
fig.legend(position="JTR+jTR+o0.2c+w6.5c", box=True)

fig.show()
