# Ecosystem

## PyGMT dependencies

### Required dependencies

#### NumPy

#### Pandas

#### Xarray

#### packaging

#### netCDF4

### Optional dependencies

#### IPython

#### GeoPandas

#### Contextily

[contextily](https://contextily.readthedocs.io/) is a small Python package to retrieve
tile maps from the internet. It can add those tiles as basemap to matplotlib figures or
write tile maps to disk into geospatial raster files. Bounding boxes can be passed in
both WGS84 (EPSG:4326) and Spheric Mercator (EPSG:3857).
In PyGMT, {func}`pygmt.datasets.load_map_tiles` and {class}`pygmt.Figure.tilemap` rely
on it.

#### RioXarray

#### Rasterio

#### PyArrow

## PyGMT ecosystem
