"""
Line fronts
----------------------

TODO

"""

import numpy as np
import pygmt

# Generate a two-point line for plotting
x = np.array([1, 4])
y = np.array([20, 20])

fig = pygmt.Figure()
fig.basemap(
    region=[0, 10, 0, 20], projection="X16c/15c", frame='+t"Line Fronts"'
)

# Plot the line using different front styles
for frontstyle in [
    # line with "faults" front style, same as +f (default) 
    "f1c/0.25c", 
    # line with box front style
    "f1c/0.25c+b",  
    # line with circle front style
    "f1c/0.25c+c", 
    # line with triangle front style
    "f1c/0.3c+t",  
    # line with left-lateral "slip" front style, angle is set to 45 and 
    # offset to 2.25 cm
    "f5c/1c+l+s45+o2.25c",  
    # line with "faults" front style, symbols are plotted on the left side of the front
    "f1c/0.4c+l",   
    # line with circle front style, symbols are plotted on the right side of the front
    "f1c/0.4c+c+r",
    # line with box front style, symbols are plotted on the left side of the front
    "f1c/0.3c+b+l", 
    # line with triangle front style, symbols are plotted on the left side of the front
    "f1c/0.3c+l+t", 
    # line with triangle front style, symbols are plotted on the right side of the front
    # and offset is set to 0.5 cm, use other pen for the outline of the symbol
    "f1c/0.4c+r+t+o0.5c+p1.5p,dodgerblue", 
    # line with triangle front style, symbols are plotted on the right side of the front
    # and offset is set to 0.3 cm, skip the outline
    "f0.5c/0.3c+r+t+o0.3c+p", 
    # line with triangle front style, symbols are plotted on the right side of the front
    # and offset is set to 0.3 cm, skip the outline and make the main front line invisible
    "f0.5c/0.3c+r+t+o0.3c+p+i",  
]:
    y -= 1  # vove the current line down
    fig.plot(x=x, y=y, pen="1.25p", style=frontstyle, color="red3")
    fig.text(x=x[-1], y=y[-1], text=frontstyle, font="Courier-Bold", justify="ML", offset="0.75c/0c")

fig.show()
