# Ecosystem

PyGMT provides a Python interface to the Generic Mapping Tools (GMT), which is a command
line program that provides a wide range of tools for manipulating geospatial data and
making publication-quality maps and figures. PyGMT integrates well with the
[scientific Python ecosystem](https://scientific-python.org/), with [NumPy][] for its
fundamental array data structure, [Pandas][] for tabular data I/O and [Xarray][] for
raster grids/images/cubes I/O.

In addition to these core dependencies, PyGMT also relies on several optional packages to
provide additional functionality for users.

*This page was adapted from [GeoPandas's Ecosystem](https://geopandas.org/en/latest/community/ecosystem.html) page.*

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

[IPython][] provides a rich toolkit to help you make the most of using Python
interactively. Its main components are a powerful interactive Python shell and a Jupyter
kernel to work with Python code in Jupyter notebooks and other interactive frontends.

PyGMT relies on IPython to provide a rich interactive experience in Jupyter notebooks.

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

[rioxarray][] is a geospatial [Xarray][] extension powered by rasterio. Built on top of
[rasterio][], it enables seamless reading, writing, and manipulation of multi-dimensional
arrays with geospatial attributes such as coordinate reference systems (CRS) and spatial extent
(bounds).

Currently, PyGMT relies on [rioxarray][] to save multi-band rasters to temporary files
in GeoTIFF format, to support processing and plotting 3-D {class}`xarray.DataArray`
images.

```{note}
We're working towards removing the dependency of the [rioxarray][] package in
[PR #3468](https://github.com/GenericMappingTools/pygmt/pull/3468).
```

#### PyArrow

[Apache Arrow][] is a development platform for in-memory analytics. It contains a set of
technologies that enable big data systems to process and move data fast. It specifies a
standardized language-independent columnar memory format for flat and hierarchical data,
organized for efficient analytic operations on modern hardware. The Arrow Python bindings
(also named "PyArrow") have first-class integration with NumPy, pandas, and built-in
Python objects. They are based on the C++ implementation of Arrow.

```{note}
If you have PyArrow installed, PyGMT does have some initial support for {class}`pandas.Series`
and {class}`pandas.DataFrame` objects with Apache Arrow-backed arrays. Specifically, only
uint/int/float and date32/date64 dtypes are supported for now. Support for string Arrow
dtypes is still a work in progress. For more details, see
[issue #2800](https://github.com/GenericMappingTools/pygmt/issues/2800).
```

## PyGMT ecosystem

Various packages rely on PyGMT for geospatial data processing, analysis, and visualization.
Below is an incomplete list (in no particular order) of tools which form the PyGMT-related
Python ecosystem.

```{note}
If your package relies on PyGMT, please
[let us know](https://github.com/GenericMappingTools/pygmt/issues/new) or
[add it by yourself](contributing.md).
```

[apache arrow]: https://arrow.apache.org/
[contextily]: https://contextily.readthedocs.io/
[geopandas]: https://geopandas.org/
[ipython]: https://ipython.org/
[matplotlib]: https://matplotlib.org/
[numpy]: https://numpy.org/
[pandas]: https://pandas.pydata.org/
[pyarrow]: https://arrow.apache.org/docs/python/
[pyogrio]: https://pyogrio.readthedocs.io/
[rioxarray]: https://corteva.github.io/rioxarray/
[shapely]: https://shapely.readthedocs.io/
[xarray]: https://xarray.pydata.org/
