"""
Envelope
--------
The `close` parameter of the :meth:`pygmt.Figure.plot` method can be
used to build a symmetrical or an asymmetrical envelope. The user
can give either the deviations or the bounds in y direction.
"""


import pandas as pd
import pygmt


# Define DataFrame with columns for x and y as well as the y lower
# and upper errors
df = pd.DataFrame(
    data={
        "x": [1, 3, 5, 7, 9],
        "y": [0.5, -0.7, 0.8, -0.3, 0.1],
        "y-error-low": [0.2, 0.2, 0.3, 0.4, 0.2],
        "y-error-upp": [0.1, 0.3, 0.2, 0.4, 0.1],
    }
)

# Create Figure instance
fig = pygmt.Figure()

fig.basemap(
    region=[0, 10, -1.5, 1.5],
    projection="X10c",
    frame="a1f1g1",
)

# Plot a symmetrical envelope ("+d")
fig.plot(
    data=df,
    close="+d",
    # Fill the envelope in gray color with a transparency of 50 %
    fill="gray@50",
    pen="1p,gray30",
)

# Plot the data points on top
fig.plot(
    data=df,
    style="c0.2c",  # Circles with a diameter of 0.3 centimeters
    pen="1p,gray30",
    fill="darkgray",
)

# Shift plot origin 11 centimeters in x direction
fig.shift_origin(xshift="11c")

fig.basemap(
    region=[0, 10, -1.5, 1.5],
    projection="X10c",
    frame=["wSnE", "a1f1g1"],
)

# Plot a asymmetrical envelope ("+D")
fig.plot(
    data=df,
    # Add an outline around the envelope
    # Here, a dashed pen (+p) with 0.5 points thickness and
    # "gray30" color is used
    close="+D+p0.5p,gray30,dashed",
    fill="gray@50",
    pen="1p,gray30",
)

# Plot the data points on top
fig.plot(
    data=df,
    style="c0.2c",
    pen="1p,gray30",
    fill="darkgray",
)

fig.show()