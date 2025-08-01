---
file_format: mystnb
---

# Justification codes

To adjust the position of plot embellishments, such as scalebars, directional roses,
colorbars, legends, and images, users can pass a two-character (order-independent)
code. Choose from

- Vertical: **T**\(op), **M**\(iddle), **B**\(ottom)
- Horizontal: **L**\(eft), **C**\(entre), **R**\(ight)


```{code-cell}
---
tags: [remove-input]
---
"""
Script to generate sketches so visualize justification codes.
"""
import pygmt

size = 5
x = [-size, 0, size, size, size, 0, -size, -size, 0]
y = [-size, -size, -size, 0, size, size, size, 0, 0]
codes =  ["BL","BC", "BR", "MR", "TR", "CT", "LT", "LM", "MC"]

fig = pygmt.Figure()
fig.basemap(projection="X10c/6c", region=[-size, size, -size, size], frame=0)

fig.text(
    font="15p,1,red",
    x=x,
    y=y,
    text=codes,
    justify=codes,
    offset="j0.5c/0.5c+v2p,gray30",
)

fig.plot(x=x, y=y, style="c0.3c", fill="lightred", no_clip=True)

fig.text(
    font="15p",
    offset="j0.5c/0.5c",
    no_clip=True,
    x=[size, size, size, -size, 0, size],
    y=[size, 0, -size, size, size, size],
    justify=["ML", "ML", "ML", "BC", "BC", "BC"],
    text=[
        "@%1%T@%%op", "@%1%M@%%iddle", "@%1%B@%%ottom", "@%1%L@%%eft",
        "@%1%C@%%enter", "@%1%R@%%ight"
    ],
)

fig.show(width=600)
```


Non-rectangular geographic basemap:

```{code-cell}
---
tags: [remove-input]
---
"""
Script to generate sketches so visualize justification codes for a non-rectangular geographic basemap.
"""
import pygmt

codes =  ["BL","BC", "BR", "MR", "TR", "CT", "LT", "LM", "MC"]

fig = pygmt.Figure()
fig.basemap(projection="H10c", region="g", frame=0)

for code in codes:
    fig.text(
        font="15p,1,red",
        position=code,
        justify=code,
        text=code,
        offset="j0.5c/0.5c+v2p,gray30",
    )
    fig.text(font="10p,lightred", position=code, justify="MC", text="●", no_clip=True)

fig.show(width=600)
```


Compasses, scalebars, legends, colorbars, text strings, etc. can also be abstracted by a rectangle.

```{code-cell}
---
tags: [remove-input]
---
"""
Script to generate sketches so visualize justification code for a colorbar.
"""
import pygmt

size = 5
codes =  ["BL","BC", "BR", "MR", "TR", "CT", "LT", "LM", "MC"]

fig = pygmt.Figure()
fig.basemap(projection="X10c/2c", region=[-size, size, -size, size], frame=0)

fig.colorbar(cmap="navia", frame=0, position="jMC+w10c/2c+h")

for code in codes:
    fig.text(
        font="10p,1,red",
        position=code,
        justify=code,
        text=code,
        offset="j0.3c/0.3c+v1p,gray30",
    )
fig.plot(x=x, y=y, style="c0.2c", fill="lightred", no_clip=True)

fig.show(width=600)
```
