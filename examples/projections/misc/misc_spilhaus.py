r"""
Spilhaus projection
===================

The Spilhaus projection is a world map projection that presents the world's
oceans as one contiguous body of water, with Antarctica at the top. It was
developed by Athelstan Spilhaus and is useful for oceanographic studies.

**+proj=spilhaus+width=**\ *width*

- ``+proj=spilhaus``: Sets the projection type.
- *width*: Sets the figure width.

.. note::

    This projection works well for coastlines but currently has issues for filling
    land and water masses.
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
    shorelines=True,
)
fig.show()
