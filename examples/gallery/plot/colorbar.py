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
fig.basemap(region=[0, 3, 6, 9], projection="x3c", frame=["af", 'WSne+t"Colorbars"'])

## Create a colorbar designed for seismic tomography- roma
# Colorbar is placed at bottom center (BC) by default if no position is given
fig.colorbar(cmap="roma", frame=["+Lvelocity", "y+lm/s"])

## Create a colorbar showing the scientific rainbow - batlow
fig.colorbar(
    cmap="batlow",
    # Colorbar positioned at map coordinates (g) longitude/latitude 0.2/8.7,
    # with a length/width (+w) of 4cm by 0.5cm, and plotted horizontally (+h)
    position="g0.3/8.7+w4c/0.5c+h",
    box=True,
    frame=["+Ltemperature", r"y+l\260C"],
    scale=100,
)

## Create a colorbar suitable for surface topography- oleron
fig.colorbar(
    cmap="oleron",
    # Colorbar position justified outside map frame (J) at Middle Right (MR),
    # offset (+o) by 1cm horizontally and 0cm vertically from anchor point,
    # with a length/width (+w) of 7cm by 0.5cm and a box for NaN values (+n)
    position="JMR+o1c/0c+w7c/0.5c+n+mc",
    # The label (+L) 'Elevation' is moved to opposite side and plotted
    # vertically as a column of text using (+mc) in the position argument above
    frame=["+LElevation", "y+lm"],
    scale=10,
)


fig.show()
