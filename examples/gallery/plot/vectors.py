"""
Cartesian, circular, and geographic vectors
-------------------------------------------

The :meth:`pygmt.Figure.plot` method can plot Cartesian, circular, and geographic vectors.
The ``style`` parameter controls vector attributes.

"""
import numpy as np
import pygmt

# create a plot with coast, Mercator projection (M) over the continental US
fig = pygmt.Figure()
fig.coast(
    region=[-127, -64, 24, 53],
    projection="M15c",
    frame=True,
    borders=1,
    area_thresh=4000,
    shorelines="0.25p,black",
)


# plot 12 Cartesian vectors with different lengths
x = np.linspace(-116, -116, 12)  # x vector coordinates
y = np.linspace(33.5, 42.5, 12)  # y vector coordinates
direction = np.zeros(x.shape)  # direction of vectors
length = np.linspace(0.5, 2.4, 12)  # length of vectors
style = "v0.2+e+a40+gred+h0+p1p,red"  # vectors with red pen and red fill, vector head at end, and 40 degree angle for vector head
fig.plot(x=x, y=y, style=style, pen="1p,red", direction=[direction, length])
fig.text(text="CARTESIAN", x=-112, y=44.2, font="13p,Helvetica-Bold,red", fill="white")


# plot math angle arcs with different radii
x = -95
y = 37
startdir = 90  # in degrees
stopdir = 180  # in degrees
radius = 1.8
arcstyle = "m0.5c+ea"
data = np.array([]).reshape((0, 5));  # empty array to hold circular vector data
for i in range(7):
    single_vector = np.array([[x, y, radius, startdir, stopdir]])
    data = np.vstack((data, single_vector));   # append next vector to circular vector data
    stopdir += 40  # set the stop direction of the next circular vector
    radius -= 0.2  # reduce radius of the next circular vector 
fig.plot(data=data, style=arcstyle, color="red3", pen="1.5p,black") 
fig.text(text="CIRCULAR", x=-95, y=44.2, font="13p,Helvetica-Bold,black", fill="white")


# plot geographic vectors using endpoints
NYC = [-74.0060, 40.7128]
CHI = [-87.6298, 41.8781]
SEA = [-122.3321, 47.6062]
NO = [-90.0715, 29.9511]
style = "=0.5+e+a30+gblue+h0.5+p1p,blue+s"  # = for geographic coordinates, +s for coord end points
data = np.array([NYC + CHI, NYC + SEA, NYC + NO])
fig.plot(data=data, style=style, pen="1.0p,blue")
fig.text(
    text="GEOGRAPHIC", x=-74.5, y=44.2, font="13p,Helvetica-Bold,blue", fill="white"
)
fig.show()
