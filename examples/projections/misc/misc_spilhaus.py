r"""
Spilhaus projection
===================

The Spilhaus projection is a world map projection that presents the world's
oceans as one contiguous body of water, with Antarctica at the top. It was
developed by Athelstan Spilhaus and is useful for oceanographic studies.

**+proj=spilhaus+width=**\ *width*

The projection is set as a PROJ string with ``+proj=spilhaus`` and the figure
size is set with *width*.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
# Use the PROJ string to set the Spilhaus projection
fig.coast(
    region="d",
    projection="+proj=spilhaus+width=12c",
    frame=Axis(annot=True, tick=True, grid=True),
    land="ivory",
    water="bisque4",
)
fig.show()

# sphinx_gallery_tags = ["misc"]
