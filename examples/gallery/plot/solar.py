"""
Solar
-----

Use :meth:`pygmt.Figure.solar` to plot the day-night terminator line, 
and civil, nautical, astronomical twilights.
"""
import datetime

import pygmt

fig = pygmt.Figure()
# Create a figure showing the global region on a Mollweide projection
# Land color is set to dark green and water color is set to light blue
fig.coast(region="d", projection="W0/15c", land="darkgreen", water="lightblue")
# Set a time for the day-night terminator and twilights, 1700 UTC on January 1, 2000
terminator_datetime = datetime.datetime(
    year=2000, month=1, day=1, hour=17, minute=0, second=0
)
# Set the pen line to be 1p thick
# Set the fill for the night area to be navy blue at 80% transparency

fig.solar(
    terminator="day_night",
    terminator_datetime=terminator_datetime,
    fill="navyblue@95",
    pen="1p",
)
fig.solar(
    terminator="civil",
    terminator_datetime=terminator_datetime,
    fill="navyblue@85",
    pen="1p",
)
fig.solar(
    terminator="nautical",
    terminator_datetime=terminator_datetime,
    fill="navyblue@80",
    pen="1p",
)
fig.solar(
    terminator="astronomical",
    terminator_datetime=terminator_datetime,
    fill="navyblue@80",
    pen="1p",
)
fig.show()
