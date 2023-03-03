import pygmt

# define static format string
pygmt.config(FORMAT_TIME_STAMP="2023-03-01T20:45:15")

fig = pygmt.Figure()
fig.timestamp()
fig.show()

# Plot the GMT timestamp logo with a custom label.
fig = pygmt.Figure()
fig.timestamp(label="Powered by PyGMT")
fig.show()
