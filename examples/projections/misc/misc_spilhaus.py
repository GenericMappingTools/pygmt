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

fig = pygmt.Figure()
# Use the PROJ string to set the Spilhaus projection
fig.basemap(projection="+proj=spilhaus+width=15c", region="d", frame="none")
# Plot Earth relief with shading for better visual effect
fig.grdimage(grid="@earth_relief_01d", shading=True)
fig.coast(shorelines=True)
fig.basemap(frame="a30f30g")
fig.show()

# sphinx_gallery_tags = ["misc"]
