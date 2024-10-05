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

[GeoPandas](https://geopandas.org/) is an open source project to make working with
geospatial data in Python easier. GeoPandas extends the datatypes used by
[pandas](https://pandas.pydata.org/) to allow spatial operations on geometric types.
Geometric operations are performed by [shapely](https://shapely.readthedocs.io/).
Geopandas further depends on [pyogrio](https://pyogrio.readthedocs.io/en/) for file
access and [matplotlib](https://matplotlib.org/) for plotting.

PyGMT doesn't directly rely on GeoPandas, but provides support of GeoPandas's data
structure, {class}`geopandas.GeoDataFrame` and {class}`geopandas.GeoSeries`, which can
be directly used in data processing and plotting functions/methods of PyGMT.

#### Contextily

[contextily](https://contextily.readthedocs.io/) is a small Python package to retrieve
tile maps from the internet. It can add those tiles as basemap to matplotlib figures or
write tile maps to disk into geospatial raster files. Bounding boxes can be passed in
both WGS84 (EPSG:4326) and Spheric Mercator (EPSG:3857).

In PyGMT, {func}`pygmt.datasets.load_tile_map` and {class}`pygmt.Figure.tilemap` rely
on it.

#### RioXarray

#### PyArrow

## PyGMT ecosystem

*This page was adapted from [GeoPandas's Ecosystem](https://geopandas.org/en/latest/community/ecosystem.html) page.*
