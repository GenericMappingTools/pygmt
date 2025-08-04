---
file_format: mystnb
---

# Reference and anchor points

xxx

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
