"""
Miller cylindrical
==================

This cylindrical projection, presented by Osborn Maitland Miller of the American
Geographic Society in 1942, is neither equal nor conformal. All meridians and
parallels are straight lines. The projection was designed to be a compromise between
Mercator and other cylindrical projections. Specifically, Miller spaced the parallels
by using Mercator’s formula with 0.8 times the actual latitude, thus avoiding the
singular poles; the result was then divided by 0.8.

``J[lon0/]width``: Give the optional central meridian ``lon0`` and the figure ``width``.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    region=[-180, 180, -80, 80],
    projection="J-65/12c",
    land="khaki",
    water="azure",
    shorelines="thinnest",
    frame="afg",
)
fig.show()
