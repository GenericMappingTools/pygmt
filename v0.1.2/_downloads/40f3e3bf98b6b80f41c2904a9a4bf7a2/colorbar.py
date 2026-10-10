"""
Colorbar
--------

The :meth:`pygmt.Figure.colorbar` method creates a color scalebar. We must specify the
colormap via the ``cmap`` argument, and set the placement via the ``position`` argument.
The full list of color paletted tables can be found at :gmt-docs:`cookbook/cpts.html`.
You can set the `position` of the colorbar using the following options:

- j/J: justified inside/outside the mapframe using any 2 character combination of
  vertical (**T** op, **M** iddle, **B** ottom) and horizontal (**L** eft, **C** enter,
  **R** ight) alignment codes, e.g. `position="jTR"` for top right.
- g: using map coordinates, e.g. `position="g170/-45"` for longitude 170E, latitude 45S.
- x: using paper coordinates, e.g. `position="x5c/7c"` for 5cm,7cm from anchor point.
- n: using normalized (0-1) coordinates, e.g. `position="n0.4/0.8"`.

Note that the anchor point defaults to the bottom left (BL). Append +h to ``position``
to get a horizontal colorbar instead of a vertical one. For more advanced styling
options, see the full option list at :gmt-docs:`colorbar.html`.
"""
import pygmt

fig = pygmt.Figure()
fig.basemap(region=[0, 3, 6, 9], projection="t0/3c", frame=True)

# Create a colorbar suitable for surface topography- oleron

fig.colorbar(
    cmap="oleron",
    position="jTC+w6c/1c+h",  # justified inside map frame (j) at Top Center (TC)
    box=True,
    frame=["+Loleron", "xaf", "y+lm"],
    scale=10,
)
# Create a colorbar designed for seismic tomography- roma
fig.colorbar(
    cmap="roma",
    position="x1.2c/4.75c+w6c/1c+h",  # plot using paper coordinates (x) at 1.2cm,4.75cm
    box=True,
    frame=["+Lroma", "xaf", "y+lm/s"],
    scale=10,
)
# Create a colorbar showing the scientific rainbow - batlow
fig.colorbar(
    cmap="batlow",
    position="g0.45/6.6+w6c/1c+h",  # plot using map coordinates (g) at lon/lat 0.45/6.6
    box=True,
    frame=["+Lbatlow", "xaf", r"y+l\260C"],
    scale=10,
)

fig.show()
