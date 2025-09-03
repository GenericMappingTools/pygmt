---
file_format: mystnb
---

# Justification codes

To place plot embellishments, such as scalebars, directional roses, colorbars, legends,
text, or images on a figure, two points have to be specified (for details please see
[Reference and anchor points](/techref/reference_anchor_points.md) a point somewhere
on the figure (**reference point**) and a point on the feature (**anchor point**). For both,
users can use a two-character code, a combination of a vertical code and a horizontal code
(order-independent):

- Vertical: **T**(op), **M**(iddle), **B**(ottom)
- Horizontal: **L**(eft), **C**(entre), **R**(ight)

For example, `"TL"` means **T**op **L**eft.

The possible nine justification codes are visualized in the sketch below:

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

For a non-rectangular geographic basemap, the justification codes refer to the invisible,
rectangular map bounding box:

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


Plot embellishments can be abstracted as rectangles. Here, the justification codes are
shown exemplary for a colorbar.

```{code-cell}
---
tags: [remove-input]
---
"""
Script showing justification codes for plot embellishments, e.g., a colorbar.
"""
fig = pygmt.Figure()
fig.basemap(projection="X10c/2c", region=[-size, size, -size, size], frame=0)

fig.colorbar(cmap="buda", frame=0, position="jMC+w10c/2c+h")

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
