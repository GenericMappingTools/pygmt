# Ecosystem

## PyGMT dependencies

### Required dependencies

#### NumPy

[NumPy][] is the fundamental package for scientific computing in Python. It is a Python
library that provides a multidimensional array object, various derived objects (such as
masked arrays and matrices), and an assortment of routines for fast operations on arrays,
including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete
Fourier transforms, basic linear algebra, basic statistical operations, random simulation
and much more.

#### Pandas

[pandas][] is a Python package providing fast, flexible, and expressive data structures
designed to make working with "relational" or "labeled" data both easy and intuitive.
It aims to be the fundamental high-level building block for doing practical, real-world
data analysis in Python. Additionally, it has the broader goal of becoming the most
powerful and flexible open source data analysis/manipulation tool available in any
language. It is already well on its way toward this goal.

#### Xarray

[Xarray][] is an open source project and Python package that introduces labels in the
form of dimensions, coordinates, and attributes on top of raw NumPy-like arrays, which
allows for more intuitive, more concise, and less error-prone user experience.

### Optional dependencies

#### IPython

#### GeoPandas

[geopandas][] is an open source project to make working with geospatial data in Python
easier. GeoPandas extends the datatypes used by [pandas][] to allow spatial operations
on geometric types. Geometric operations are performed by [shapely][]. Geopandas further
depends on [pyogrio][] for file access and [matplotlib][] for plotting.

PyGMT doesn't directly rely on GeoPandas, but provides support of GeoPandas's data
structure, {class}`geopandas.GeoDataFrame` and {class}`geopandas.GeoSeries`, which can
be directly used in data processing and plotting functions/methods of PyGMT.

#### Contextily

[contextily][] is a small Python package to retrieve tile maps from the internet. It can
add those tiles as basemap to matplotlib figures or write tile maps to disk into
geospatial raster files. Bounding boxes can be passed in both WGS84 (EPSG:4326) and
Spheric Mercator (EPSG:3857).

In PyGMT, {func}`pygmt.datasets.load_tile_map` and {class}`pygmt.Figure.tilemap` rely
on it.

#### RioXarray

[rioxarray][] is a geospatial [xarray][] extension powered by rasterio. Built on top of
[rasterio][], it enables seamless reading, writing, and manipulation of multi-dimensional
arrays with geospatial attributes such as coordinate reference systems (CRS) and spatial extent
(bounds).

Currently, PyGMT relies on [rioxarray][] to to saving multi-band rasters to temporary files
in GeoTIFF format, to support processing and plotting 3-D :class:`xarray.DataArray`
images.

```{note}
We're working towards removing the dependency of the [rioxarray][] package in
[PR #3468](https://github.com/GenericMappingTools/pygmt/pull/3468).
```

#### PyArrow

## PyGMT ecosystem

*This page was adapted from [GeoPandas's Ecosystem](https://geopandas.org/en/latest/community/ecosystem.html) page.*


[contextily]: https://contextily.readthedocs.io/
[geopandas]: https://geopandas.org/
[matplotlib]: https://matplotlib.org/
[pandas]: https://pandas.pydata.org/
[pyarrow]: https://arrow.apache.org/docs/python/
[pyogrio]: https://pyogrio.readthedocs.io/
[rioxarray]: https://corteva.github.io/rioxarray/
[shapely]: https://shapely.readthedocs.io/
[xarray]: https://xarray.pydata.org/