# PyGMT Ecosystem

The PyGMT ecosystem consists of the packages that PyGMT depends on and the packages that
depend on PyGMT. Besides [GMT][] itself, PyGMT integrates well with the
[scientific Python ecosystem](https://scientific-python.org/), with [NumPy][] for its
fundamental array data structure, [pandas][] for tabular data I/O and [xarray][] for
raster grids/images/cubes I/O. In addition to these core dependencies, it also relies on
several optional packages to provide additional functionality for users. In turn, a
growing number of packages build on PyGMT for geospatial data processing, analysis, and
visualization.

## PyGMT dependencies

![](https://github.com/user-attachments/assets/2e36bd3e-d8ae-4399-b7c0-af614cb414fb)

_The PyGMT ecosystem. This figure was originally published in the
[PyGMT paper](https://doi.org/10.1029/2026GC013105) in G-Cubed. The full publication is
released under CC BY-NC 4.0. No modifications were made._

_An asterisk (*) after the package name indicates the package is a required dependency of PyGMT._

[NumPy][]*
:  The fundamental package for scientific computing in Python, providing a
   multidimensional array object and an assortment of routines for fast operations on
   arrays.

[pandas][]*
:  A Python package providing fast, flexible, and expressive data structures designed to
   make working with tabular data easy and intuitive.

[xarray][]*
:  A Python package that introduces labels in the form of dimensions, coordinates, and
   attributes on top of raw NumPy-like arrays, which allows for more intuitive, more
   concise, and less error-prone user experience.

[IPython][]
:  A rich toolkit for using Python interactively, including a powerful interactive
   Python shell and a Jupyter kernel to work with Python code in Jupyter notebooks and
   other interactive frontends. PyGMT relies on it to provide a rich interactive
   experience in Jupyter notebooks.

[GeoPandas][]
:  A Python package that extends the datatypes used by [pandas][] to allow spatial
   operations on geometric types. PyGMT doesn't directly rely on it, but supports its
   two main data structures, {class}`geopandas.GeoDataFrame` and
   {class}`geopandas.GeoSeries`, in data processing and plotting functions/methods.

[contextily][]
:  A small Python package to retrieve tile maps from the internet. These tiles can
   be added as background of a map or saved to disk into geospatial raster files.
   In PyGMT, {func}`pygmt.datasets.load_tile_map` and
   {meth}`pygmt.Figure.tilemap` rely on it.

[rioxarray][]
:  A geospatial [xarray][] extension powered by [rasterio][], enabling seamless reading,
   writing, and manipulation of multi-dimensional arrays with geospatial attributes such
   as coordinate reference systems (CRS) and spatial extent (bounds). PyGMT relies on it
   in in several aspects:

   1. To save multi-band rasters to temporary files in GeoTIFF format, to support
      processing and plotting 3-D {class}`xarray.DataArray` images.
   2. To write CRS information to the {class}`xarray.DataArray` objects.
   3. To reproject raster tiles to the target CRS in {func}`pygmt.datasets.load_tile_map`.

   ```{note}
   We're working towards avoiding temporary files when processing/plotting multi-band
   rasters in [PR #3468](https://github.com/GenericMappingTools/pygmt/pull/3468).
   ```

[PyArrow][]
:  The Python bindings for [Apache Arrow][], a development platform for in-memory analytics
   that specifies a standardized language-independent columnar memory format for flat and
   hierarchical data, organized for efficient analytic operations on modern hardware.

   ```{note}
   If you have [PyArrow][] installed, PyGMT does have some initial support for
   `pandas.Series` and `pandas.DataFrame` objects with Apache Arrow-backed arrays.
   Specifically, only uint/int/float, date32/date64 and string types are supported for
   now. Support for Duration types and GeoArrow geometry types is still a work in
   progress. For more details, see
   [issue #2800](https://github.com/GenericMappingTools/pygmt/issues/2800).
   ```

## Packages depending on PyGMT

Various packages rely on PyGMT for geospatial data processing, analysis, and visualization.
Below is an incomplete list (in no particular order) of these tools.

```{note}
If your package relies on PyGMT, please
[let us know](https://github.com/GenericMappingTools/pygmt/issues/new) or
[add it by yourself](contributing.md).
```

*This page was adapted from [GeoPandas's Ecosystem](https://geopandas.org/en/latest/community/ecosystem.html) page.*


[apache arrow]: https://arrow.apache.org/
[contextily]: https://contextily.readthedocs.io/
[geopandas]: https://geopandas.org/
[gmt]: https://www.generic-mapping-tools.org/
[ipython]: https://ipython.org/
[numpy]: https://numpy.org/
[pandas]: https://pandas.pydata.org/
[pyarrow]: https://arrow.apache.org/docs/python/
[pyogrio]: https://pyogrio.readthedocs.io/
[rasterio]: https://rasterio.readthedocs.io/
[rioxarray]: https://corteva.github.io/rioxarray/
[xarray]: https://xarray.pydata.org/
