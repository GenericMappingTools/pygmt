"""
Grdfill
=======

xxx
"""

import pygmt

earth_relief_holes = pygmt.datasets.load_sample_data(name="earth_relief_holes")

# %%
filled_grid = pygmt.grdfill(grid=earth_relief_holes, mode="c20")

# %%
filled_grid = pygmt.grdfill(grid=earth_relief_holes, constantfill="c20")

# %%
filled_grid = pygmt.grdfill(grid=earth_relief_holes, constant_fill="c20")
