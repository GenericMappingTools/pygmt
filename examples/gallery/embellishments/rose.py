"""
Rose diagram
------------

The :meth:`pygmt.Figure.rose` method can plot windrose diagrams or polar histograms.
"""

import pygmt

data = pygmt.datasets.load_fractures_compilation()

fig = pygmt.Figure()

fig.rose(
    # use the remote file fractures_06.txt which contains a compilation
    # of fracture lengths and azimuth as hypothetically digitized from
    # geological maps
    data=data,
    # specify the "region" of interest in the (r,azimuth) space [r0, r1, az0, az1],
    # here, r0 is 0 and r1 is 1, for azimuth, az0 is 0 and az1 is 360 which means
    # we plot a full circle between 0 and 360 degrees
    region=[0, 1, 0, 360],
    # set the diameter of the rose diagram to 7.5 cm
    diameter="7.5c",
    # lengths are located in the second ([1]) column, directions in the first
    # one ([0]), zero-based indexing is used here
    columns=[1, 0],
    # define the sector width in degrees, we append +r here to draw a rose
    # diagram instead of a sector diagram
    sector="10r",
    # normalize bin counts by the largest value so all bin counts range from
    # 0 to 1
    norm=True,
    # use red3 as color fill for the sectors
    color="red3",
    # define the frame with ticks and gridlines every 0.2
    # lenght unit in radial direction and every 30 degrees
    # in azimuthal direction, set background color to
    # lightgray
    frame=["x0.2g0.2", "y30g30", "+glightgray"],
    # use a pen size of 1p to draw the outlines
    pen="1p",
)

fig.show()
