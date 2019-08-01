"""
General Perspective
===================

The general perspective projection imitates the view of the Earth from a finite
point in space. In a full view of the earth one third of its surface area can
be seen.

``lon0/lat0/altitude/azimuth/tilt/twist/Width/Height/scale`` or ``width``

``lon0/lat0`` specifies the projection center, ``altitude`` the height
in km of the viewpoint above local sea level (If altitude is less than 10,
then it is the distance from the center of the earth to the viewpoint in earth
radii). With ``azimuth`` the direction (in degrees) in which you are looking is
specified, measured clockwise from north. ``tilt`` is given in degrees and is the
viewing angle relative to zenith. A tilt of 0° is looking straight down, 60° is
looking 30° above horizon. ``twist`` is the clockwise rotation of the image (in
degrees). ``Width`` and ``Height`` describe the viewport angle in degrees.

The example shows the coast of northern europe viewed from 250 km above sea
level looking 30° from north at a tilt of 45°. The height and width of the
viewing angle is both 60°, which imitates viewing with naked eye.
"""
import pygmt

fig = pygmt.Figure()
fig.coast(
    projection="G4/52/250/30/45/0/60/60/5i",
    region="g",
    frame=["x10g10", "y5g5"],
    land="gray",
)
fig.show()
