"""
Functions to load GMT remote data and sample data.

Data are downloaded from the GMT data server.
"""

from pygmt.datasets.earth_age import load_earth_age
from pygmt.datasets.earth_day import load_blue_marble
from pygmt.datasets.earth_deflection import load_earth_deflection
from pygmt.datasets.earth_dist import load_earth_dist
from pygmt.datasets.earth_free_air_anomaly import load_earth_free_air_anomaly
from pygmt.datasets.earth_geoid import load_earth_geoid
from pygmt.datasets.earth_magnetic_anomaly import load_earth_magnetic_anomaly
from pygmt.datasets.earth_mask import load_earth_mask
from pygmt.datasets.earth_mean_dynamic_topography import (
    load_earth_mean_dynamic_topography,
)
from pygmt.datasets.earth_mean_sea_surface import load_earth_mean_sea_surface
from pygmt.datasets.earth_night import load_black_marble
from pygmt.datasets.earth_relief import load_earth_relief
from pygmt.datasets.earth_vertical_gravity_gradient import (
    load_earth_vertical_gravity_gradient,
)
from pygmt.datasets.mars_relief import load_mars_relief
from pygmt.datasets.mercury_relief import load_mercury_relief
from pygmt.datasets.moon_relief import load_moon_relief
from pygmt.datasets.pluto_relief import load_pluto_relief
from pygmt.datasets.samples import list_sample_data, load_sample_data
from pygmt.datasets.tile_map import load_tile_map
from pygmt.datasets.venus_relief import load_venus_relief
