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

- **g** or **G**: Sets the projection type.
- *lon0/lat0*: Sets the projection center.
- *scale* or *width*: Sets the figure size.
- **+a**\ *azimuth*: The direction in which you are looking, measured clockwise
  from north in degrees. [Optional]
- **+t**\ *tilt*: The viewing angle relative to zenith in degrees. A tilt of 0°
  is looking straight down, 60° is looking 30° above horizon. [Optional]
- **+v**\ *vwidth/vheight*: The viewport angle in degrees. [Optional]
- **+w**\ *twist*: The clockwise rotation of the image in degrees. [Optional]
- **+z**\ *altitude*: The height of the viewpoint above local sea level in km.
  If altitude is less than 10, it is the distance from the center of the earth
  to the viewpoint in earth radii. [Optional]

The example shows the coast of Northern Europe viewed from 250 km above sea
level looking 30° from north at a tilt of 45°. The height and width of the
viewing angle is both 60°, which imitates viewing with naked eye.
"""

# %%
import pygmt
from pygmt.params import Axis

fig = pygmt.Figure()
fig.coast(
    region="g",
    projection="G4/52/12c+a30+t45+v60/60+w0+z250",
    frame=Axis(annot=True, tick=True, grid=True),
    land="khaki",
    water="white",
)
fig.show()
