import pygmt

fig = pygmt.Figure()

# Load sample grid and use area around the Hawaiian Islands
grid = pygmt.datasets.load_earth_relief(resolution="01m", region=[-162, -153, 18, 23])

# Plot original grid
fig.basemap(
    region=[-162, -153, 18, 23], projection="M12c", frame=["f", '+t"original grid"']
)
fig.grdimage(grid=grid, cmap="oleron")

fig.shift_origin(yshift="-9c")

# Set all grid points < 0 to a value of -2000.
grid = pygmt.grdclip(grid, below=[0, -2000])

# Plot clipped grid
fig.basemap(
    region=[-162, -153, 18, 23], projection="M12c", frame=["f", '+t"clipped grid"']
)
fig.grdimage(grid=grid)
fig.colorbar(frame=["x+lElevation", "y+lm"])

fig.show()
