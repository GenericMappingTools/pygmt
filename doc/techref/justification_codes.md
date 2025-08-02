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
Script showing the justification codes used in GMT / PyGMT.
"""
import pygmt

size = 5
x1 = [-size, 0, size, size, size, 0, -size, -size, 0]
y1 = [-size, -size, -size, 0, size, size, size, 0, 0]
x2 = [-3, -2, -1, -1, -1, -2, -3, -3, -2]
y2 = [-1, -1, -1, 0, 1, 1, 1, 0, 0]
codes = ["BL", "BC", "BR", "MR", "TR", "TC", "TL", "ML", "MC"]

fig = pygmt.Figure()
fig.basemap(projection="X10c/6c", region=[-size, size, -size, size], frame=0)

fig.text(
    font="15p,1,black",
    x=x1,
    y=y1,
    text=codes,
    justify=codes,
    offset="j0.5c/0.5c+v2p,gray30",
)

fig.plot(x=x1, y=y1, style="c0.3c", fill="steelblue", no_clip=True)

fig.text(
    font="15p",
    offset="j0.5c/0.5c",
    no_clip=True,
    x=[size, size, size, -size, 0, size],
    y=[size, 0, -size, size, size, size],
    justify=["ML", "ML", "ML", "BC", "BC", "BC"],
    text=[
        "@%1%T@%%op",
        "@%1%M@%%iddle",
        "@%1%B@%%ottom",
        "@%1%L@%%eft",
        "@%1%C@%%enter",
        "@%1%R@%%ight",
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
Script showing justification codes for non-rectangular geographic basemaps.
"""
fig = pygmt.Figure()
fig.basemap(projection="H10c", region="g", frame=0)

for code in codes:
    fig.text(
        font="10p,1,black",
        position=code,
        justify=code,
        text=code,
        offset="j0.5c/0.5c+v2p,gray30",
    )
    fig.text(font="10p,steelblue", position=code, justify="MC", text="●", no_clip=True)

fig.show(width=600)
```


Compasses, scalebars, legends, colorbars, text strings, etc. can also be abstracted by a rectangle.

```{code-cell}
---
tags: [remove-input]
---
"""
Script showing justification codes for plot embellishments, e.g., a colorbar.
"""
fig = pygmt.Figure()
fig.basemap(projection="X10c/2c", region=[-size, size, -size, size], frame=0)

fig.colorbar(cmap="hawaii", frame=0, position="jMC+w10c/2c+h")

for code in codes:
    fig.text(
        font="10p,1,black",
        position=code,
        justify=code,
        text=code,
        offset="j0.3c/0.15c+v1p,gray30",
    )
fig.plot(x=x1, y=y1, style="c0.2c", fill="steelblue", no_clip=True)

fig.show(width=600)
```


Reference and anchor points:

```{code-cell}
---
tags: [remove-input]
---
"""
Script explaining reference and anchor points.
"""
fig = pygmt.Figure()
fig.basemap(projection="X10c/6c", region=[-size, size, -size, size], frame=0)

fig.text(
    text=codes,
    x=x1,
    y=y1,
    justify=codes,
    offset="j0.5c/0.2c+v1p,gray30",
    font="10p,1,black",
)

fig.plot(x=x2[0:-1], y=y2[0:-1], fill="bisque")

fig.plot(x=-size, y=size, style="s0.6c", fill="lightred", no_clip=True)
fig.plot(x=x1, y=y1, style="c0.25c", fill="steelblue", no_clip=True)

fig.plot(x=-3, y=1, style="s0.6c", fill="orange")
fig.plot(x=x2, y=y2, style="c0.15c", fill="darkblue")

fig.plot(x=[-5, -3], y=[5, 1], pen="0.5p,black")
fig.plot(x=[-5, -3], y=[1, 1], pen="0.5p,black,2_2")
fig.plot(x=[-3, -3], y=[1, 5], pen="0.5p,black,2_2")

fig.text(x=-4, y=1, text="dx", offset="0c/0.2c")
fig.text(x=-3, y=3, text="dy", offset="-0.2c/0c")

fig.show(width=600)
```
