"""
PyGMT logo
==========
The PyGMT logo coded in Python using PyGMT. The design of the logo is kindly provided
by `@sfrooti <https://github.com/sfrooti>`_. The logo consists of a visual and the
wordmark "PyGMT". There are different versions available:

- ``color_concept``: colors of the visual and workmark.
  Select between ``"colors"`` (colors for Python (blue and yellow) and GMT (red)) and
  ``"bw"`` for black and white.
  [Default is ``"color"``].
- ``bg_concept``: color of the background.
  Select between ``"light"`` (white) and ``"dark"`` (darkgray / gray20).
  [Default is ``"dark"``].
- ``shape``: shape of the visual.
  Select between ``"circle"`` and ``"hexagon"``.
  [Default is ``"circle"``].
- ``angle_rot``: rotation angle of the visual.
  Give an angle in degrees (mesuared contour-clockwise from the vertical).
  [Default is ``30``]. Should this be flexible ???
- ``wordmark``: add the wordmark "PyGMT".
  ``True`` or ``False``.
  [Default is ``True``]. ???
- ``orientation``: orientation of the wordmark.
  Select between ``"vertical"`` (at the bottom) and ``"horizontal"`` (at the right).
  [Default is ``"vertical"``].
"""

# %%
from pathlib import Path

import pygmt

# -----------------------------------------------------------------------------
# Changebale settings  (-> adjust for your needs; later input for function)
# -----------------------------------------------------------------------------
color_concept = "color"  # "color" | "bw"
bg_concept = "dark"  # "light" | "dark"
shape = "circle"  # "circle" | "hexagon"
angle_rot = 30  # degrees
wordmark = True  # True | False
orientation = "horizontal"  # "horizontal" | "vertical"
dpi_png = 720  # resolution of saved PNG image


# -----------------------------------------------------------------------------
# Define colors (-> can be discussed)
# -----------------------------------------------------------------------------
if color_concept == "color":
    color_blue = "48/105/152"  # Python blue
    color_yellow = "255/212/59"  # Python yellow
    color_red = "238/86/52"  # GMT red
elif color_concept == "bw" and bg_concept == "light":
    color_blue = color_yellow = color_red = "gray20"
elif color_concept == "bw" and bg_concept == "dark":
    color_blue = color_yellow = color_red = "white"

match bg_concept:
    case "light":
        color_bg = "white"
        color_py = color_blue
        color_gmt = "gray20"
    case "dark":
        color_bg = "gray20"
        color_py = color_yellow
        color_gmt = "white"


# -----------------------------------------------------------------------------
# Not-changebale settings (-> need to extended)
# -----------------------------------------------------------------------------
size = 5
region = [-size, size] * 2

xy_yellow_1 = 2.65
xy_yellow_2 = 1.3

pen_yellow = f"5p,{color_yellow}"
pen_red = f"10p,{color_red}"


# %%

# -----------------------------------------------------------------------------
# Start plotting
# -----------------------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Creating the visual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=region, projection=f"X{size * 2}c", frame=[0, "+gcyan@100"])

# .............................................................................
# blue circle / hexagon for Earth
# .............................................................................
match shape:
    case "circle":
        style = "c7.5c"
    case "hexagon":
        style = "h8.6c"
fig.plot(x=0, y=0, style=style, pen=f"15p,{color_blue}", fill=color_bg)

# .............................................................................
# yellow lines for compass
# .............................................................................
# horizontal yellow line
fig.plot(x=[-4, 4], y=[0, 0], pen=pen_yellow)
# diagonal yellow lines
# upper left
fig.plot(x=[-xy_yellow_1, -xy_yellow_2], y=[xy_yellow_1, xy_yellow_2], pen=pen_yellow)
# lower right
fig.plot(x=[xy_yellow_2, xy_yellow_1], y=[-xy_yellow_2, -xy_yellow_1], pen=pen_yellow)
# lower left
fig.plot(x=[-xy_yellow_1, -xy_yellow_2], y=[-xy_yellow_1, -xy_yellow_2], pen=pen_yellow)
# upper right
fig.plot(x=[xy_yellow_2, xy_yellow_1], y=[xy_yellow_2, xy_yellow_1], pen=pen_yellow)

# .............................................................................
# letter G
# .............................................................................
# horizontal red line
fig.plot(x=[0.1, 1.65], y=[0, 0], pen=f"12p,{color_red}")
# red ring sector
fig.plot(x=0, y=0, style="w3.3c/90/0+i2.35c", fill=color_red)
# space between yellow lines and ring sector
fig.plot(x=0, y=0, style="w3.7c/0/360+i3.3c", fill=color_bg)
# vertical yellow line
fig.plot(x=[0, 0], y=[-4, 4], pen=f"6p,{color_yellow}")
# cover yellow line in lower part of the ring sector
fig.plot(x=0, y=0, style="w3.3c/260/-80+i2.35c", fill=color_red)

# .............................................................................
# upper vertical red line
# .............................................................................
# space between red line and blue circle / hexagon
fig.plot(x=[0, 0], y=[4.01, 3.0], pen=f"18p,{color_bg}")
# red line
fig.plot(x=[0, 0], y=[4.00, 1.9], pen=f"12p,{color_red}")

# .............................................................................
# letter M
# .............................................................................
# space between letter M and yellow line at the right side
# fig.plot(x=[1.6, 1.6], y=[1.5, 1.775], pen=f"10p,{color_bg}")
fig.plot(x=[1.6, 1.6], y=[1.5, 2.0], pen=f"10p,{color_bg}")
# diagonal lines
fig.plot(x=[0.33, 0.90], y=[1.527, 1.00], pen=pen_red)
fig.plot(x=[0.90, 1.43], y=[1.00, 1.527], pen=pen_red)
# middle pick
fig.plot(x=0.9, y=0.9, style="d0.3c", fill=color_red)
# vertical lines
fig.plot(x=[0.285, 0.285], y=[0.00, 1.65], pen=pen_red)
fig.plot(x=[1.47, 1.47], y=[0.00, 1.65], pen=pen_red)

# .............................................................................
# letter T
# .............................................................................
# red curved horizontal line
fig.plot(x=0, y=0, style="w4.6c/240/-60+i3.7c", fill=color_red)
# vertical endings of curved horizontal line
fig.plot(x=[-1.05, -1.05], y=[-1.5, -2.5], pen=f"9p,{color_bg}")
fig.plot(x=[1.05, 1.05], y=[-1.5, -2.5], pen=f"9p,{color_bg}")
# arrow head as inverse triangle with pen for space to blue circle / hexagon
fig.plot(x=0, y=-3.55, style="i1.1c", fill=color_red, pen=f"3p,{color_bg}")
# arrow tail
fig.plot(x=[0, 0], y=[-2, -3.57], pen=f"12p,{color_red}")

# .............................................................................
# Save
# .............................................................................
# fig.show()
fig_name = f"pygmt_logo_{shape}_{color_concept}_{bg_concept}"
fig.savefig(fname=f"{fig_name}.eps", dpi=dpi_png)
print(fig_name)


# %%

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Replot and apply rotation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = pygmt.Figure()
pygmt.config(MAP_FRAME_PEN="cyan@100")
fig.basemap(region=region, projection=f"X{size * 2}c", frame=[0, f"+g{color_bg}"])

fig.image(
    imagefile=f"{fig_name}.eps",
    position=f"jMC+w{size * 2}c",
    # Rotation around z (vertical) axis placed in the center
    perspective=f"{angle_rot}+w0/0",
)

# .............................................................................
# Save
# .............................................................................
# fig.show()
fig_name_rot = f"{fig_name}_rot{angle_rot}deg"
exts = ["eps"] if wordmark is True else ["png", "pdf", "eps"]
for ext in exts:
    # transparent = True if ext == "png" else False  # problems with code style
    transparent = False
    if ext == "png":
        transparent = True
    fig.savefig(fname=f"{fig_name_rot}.{ext}", dpi=dpi_png, transparent=transparent)
print(fig_name_rot)


# %%

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Replot and add WordMark "PyGMT"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if wordmark is True:
    match orientation:
        case "vertical":
            projection = f"X{size * 2 - 2}c/{size * 2}c"
            position = f"jMC+w{size * 2}c+o0c/1.1c"
            args_text = {"x": -3.6, "y": -3.6, "justify": "LM"}
            args_cover = {"x": -2.4, "y": -3.6}
        case "horizontal":
            projection = f"X{size * 2}c/{size - 2}c"
            position = f"jLM+w{size - 1.5}c"
            args_text = {"x": -1.5, "y": 0, "justify": "LM"}
            args_cover = {"x": -0.5, "y": -0.2}

    fig = pygmt.Figure()
    pygmt.config(MAP_FRAME_PEN="cyan@100")
    fig.basemap(region=region, projection=projection, frame=[0, f"+g{color_bg}"])

    fig.image(imagefile=f"{fig_name_rot}.eps", position=position)

    fig.text(text="PyGMT", font=f"50p,AvantGarde-Book,{color_gmt}", **args_text)
    fig.plot(style="s2.9c", fill=color_bg, **args_cover)
    fig.text(text="Py", font=f"50p,AvantGarde-Book,{color_py}", **args_text)

    # .............................................................................
    # Save
    # .............................................................................
    fig_name_rot_text = f"{fig_name_rot}_wordmark_{orientation}"
    for ext in ["png", "pdf", "eps"]:
        # transparent = True if ext == "png" else False  # problems with code style
        transparent = False
        if ext == "png":
            transparent = True
        fig.savefig(
            fname=f"{fig_name_rot_text}.{ext}", dpi=dpi_png, transparent=transparent
        )
    print(fig_name_rot_text)
    Path.unlink(f"{fig_name_rot}.eps")


# %%
fig.show()
Path.unlink(f"{fig_name}.eps")
