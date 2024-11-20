r"""
Perspective projection
======================

The perspective projection imitates the view of the Earth from a finite
point in space. In a full view of the earth one third of its surface area can
be seen.

**g**\ *lon0/lat0*\ */scale*\ [**+a**\ *azimuth*]\
[**+t**\ *tilt*]\ [**+v**\ *vwidth/vheight*]\ [**+w**\ *twist*]\
[**+z**\ *altitude*] or **G**\ *lon0/lat0*\ */width*\
[**+a**\ *azimuth*]\ [**+t**\ *tilt*]\ [**+v**\ *vwidth/vheight*]\
[**+w**\ *twist*]\ [**+z**\ *altitude*]

The projection type is set with **g** or **G**. *lon0/lat0* specifies the
projection center and *scale* or *width* determine the size of the figure.
With **+a**\ *azimuth* the direction (in degrees) in which you are looking is
specified, measured clockwise from north. **+t**\ *tilt* is given in degrees
and is the viewing angle relative to zenith. A tilt of 0° is looking straight
down, 60° is looking 30° above horizon. The viewport angle in degrees is
described via **+v**\ *vwidth/vheight* and **+w**\ *twist* is the clockwise
rotation of the image (in degrees). **+z**\ *altitude* sets the height in km
of the viewpoint above local sea level (If altitude is less than 10, then it is
the distance from the center of the earth to the viewpoint in earth radii).

The example shows the coast of Northern Europe viewed from 250 km above sea
level looking 30° from north at a tilt of 45°. The height and width of the
viewing angle is both 60°, which imitates viewing with naked eye.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="G4/52/12c+a30+t45+v60/60+w0+z250",
    frame="afg",
    land="khaki",
    water="white",
)
fig.show()
