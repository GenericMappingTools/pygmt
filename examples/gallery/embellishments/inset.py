"""
Inset
-----

The :meth:`pygmt.Figure.inset` method adds an inset figure inside a larger
figure. The method is called using a ``with`` statement, and its
``position``, ``box``, ``offset``, and ``margin`` parameters are set. Plotting
methods called within the ``with`` statement are applied to the inset figure.
"""
import pygmt

fig = pygmt.Figure()
# Create the primary figure, setting the region to Madagascar, the land color
# to "brown", the water to "lightblue", the shorelines width to "thin", and
# adding a frame
fig.coast(region="MG+r2", land="brown", water="lightblue", shorelines="thin", frame="a")
# Create an inset, setting the position to top left, the width to 3.5 cm, and
# the x- and y-offsets to 0.2 cm. The margin is set to 0, and the border is
# "gold" with a pen size of 1.5p.
with fig.inset(position="jTL+w3.5c+o0.2c", margin=0, box="+p1.5p,gold"):
    # Create a figure in the inset using coast. This example uses the azimuthal
    # orthogonal projection centered at 47E, 20S. The land color is set to
    # "gray" and Madagascar is highlighted in "red3".
    fig.coast(
        region="g",
        projection="G47/-20/?",
        land="gray",
        water="white",
        dcw="MG+gred3",
    )
fig.show()
