import pygmt

fig = pygmt.Figure()
fig.timestamp()
fig.show()

# Plot the GMT timestamp logo with a custom label.
fig = pygmt.Figure()
fig.timestamp(label="Powered by PyGMT")
fig.show()
