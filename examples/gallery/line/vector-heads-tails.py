"""
Vector heads and tails
----------------------

The :meth:`pygmt.Figure.plot` method can plot vectors with individual 
heads and tails. We must specify the modifiers (together with the vector type)
by passing the corresponding shortcuts to the  ``style`` argument. 

"""

import pygmt

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 15], projection="X15c/10c", frame='+t"Vector heads and tails"'
)

x = 1
y = 14
angle = 0  # in degrees, measured counter-clockwise from horizontal
length = 7

for vecstyle in [
    "v0c",  # vector without head and tail (line)
    "v0.6c+bA+eA+a50",  # plain open arrow at the beginning and end of the vector path, angle of the vector head apex is set to 50
    "v0.4c+bI+eI",  # plain open tail at the beginning and end
    "v0.3c+bt+et+a80",  # terminal line at the beginning and end, angle of the vector head apep is set to 80
    "v0.6c+e",  # arrow head at the end
    "v0.6c+bc+ea",  # circle at the beginning and an arrow head at the end
    "v0.6c+bt+ea",  # terminal line at the beginning and an arrow head at the end
    "v1c+e+h0.5",  # arrow head at the end, shape of the vector head is set to 0.5
    "v1c+b+e+h0.5",  # modified arrow heads at the beginning and end
    "v1c+bi+ea+h0.5",  # tail at the beginning and an arrow with modified vector head at the end
    "v1c+bar+ea+h0.8",  # half-sided arrow head (right side) at the beginning and an arrow at the end
    "v1c+bar+eal+h0.5",  # half-sided arrow heads at the beginning (right side) and end (left side)
    "v1c+bi+ea+r+h0.5+a45",  # half-sided tail at the beginning and arrow at the at the end (right side for both)
]:
    fig.plot(
        x=x, y=y, style=vecstyle, direction=([angle], [length]), pen="2p", color="red3"
    )
    fig.text(x=6, y=y, text=vecstyle, justify="ML", offset="0.2c/0c")
    y -= 1  # move the next vector down

fig.show()
