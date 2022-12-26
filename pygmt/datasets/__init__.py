# pylint: disable=missing-docstring
#
# Load sample data included with GMT (downloaded from the GMT cache server).

from pygmt.datasets.earth_age import load_earth_age
from pygmt.datasets.earth_free_air_anomaly import load_earth_free_air_anomaly
from pygmt.datasets.earth_geoid import load_earth_geoid
from pygmt.datasets.earth_magnetic_anomaly import load_earth_magnetic_anomaly
from pygmt.datasets.earth_relief import load_earth_relief
from pygmt.datasets.earth_vertical_gravity_gradient import (
    load_earth_vertical_gravity_gradient,
)
from pygmt.datasets.samples import (
    list_sample_data,
    load_fractures_compilation,
    load_hotspots,
    load_japan_quakes,
    load_mars_shape,
    load_ocean_ridge_points,
    load_sample_bathymetry,
    load_sample_data,
    load_usgs_quakes,
)
