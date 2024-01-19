"""
Line segment caps and joints
============================
PyGMT offers different appearance of line segment caps and joints. The desired
appearance can be set via the GMT default parameters :gmt-term:`PS_LINE_CAP`
(``"butt"``, ``"round"``, or ``"square"`` [Default]) as well as :gmt-term:`PS_LINE_JOIN`
(``"bevel"``, ``"round"``, and ``"miter"`` [Default]) and :gmt-term:`PS_MITER_LIMIT`
(limit on the angle at the mitered joint below which a bevel is applied).
"""

# %%
import numpy as np
import pygmt

# Set up dictionary for colors
dict_col = {
    "round": "green4",
    "square": "steelblue",
    "butt": "orange",
    "miter": "steelblue",
    "bevel": "orange",
}

# Create new Figure instance
fig = pygmt.Figure()

# -----------------------------------------------------------------------------
# Top: PS_LINE_CAP

# Create sample data
x = np.array([30, 170])
y = np.array([70, 70])

fig.basemap(region=[0, 250, 0, 100], projection="x1p", frame="rltb")

for line_cap in ["butt", "round", "square"]:
    # Change GMT default locally using a context manager
    # The change applies only to the code under the with statement
    with pygmt.config(PS_LINE_CAP=line_cap):
        # Plot a dashed line
        color = dict_col[line_cap]
        fig.plot(x=x, y=y, pen=f"10p,{color},20_20:0")

    fig.plot(x=x, y=y, pen="1p")
    fig.plot(x=x, y=y, style="c0.1c", fill="white", pen="0.5p")
    fig.text(text=line_cap, x=x[-1] + 20, y=y[-1], justify="LM")

    y = y - 20

fig.shift_origin(yshift="-h")

# -----------------------------------------------------------------------------
# Bottom: PS_LINE_JOIN and PS_MITER_LIMIT

# Create sample data
x = np.array([[5, 95, 65], [80, 170, 140], [155, 235, 205]])
y = np.array([[10, 70, 10], [10, 70, 10], [10, 70, 10]])

fig.basemap(region=[0, 250, 0, 100], projection="x1p", frame="rltb")

for i_line, line_join in enumerate(["bevel", "round", "miter"]):
    x_temp = x[i_line, :]
    y_temp = y[i_line, :]
    # Change GMT default locally using a context manager
    # The change applies only to the code under the with statement
    with pygmt.config(PS_LINE_JOIN=line_join, PS_MITER_LIMIT=1):
        fig.plot(x=x_temp, y=y_temp, pen="7p," + dict_col[line_join])

    fig.plot(x=x_temp, y=y_temp, pen="1p")
    fig.plot(x=x_temp, y=y_temp, style="c0.1c", fill="white", pen="0.5p")
    fig.text(text=line_join, x=x_temp[1] - 10, y=y_temp[1], justify="RB")

fig.show()
