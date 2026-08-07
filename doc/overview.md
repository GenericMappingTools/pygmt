# Overview

## Why PyGMT

A beautiful map is worth a thousand words. To truly understand how powerful PyGMT is,
play with it online on [Binder](https://github.com/GenericMappingTools/try-gmt)! For a
quicker introduction, check out our [3 minute overview](https://youtu.be/4iPnITXrxVU)!

Afterward, try the [Intro to PyGMT](intro/index.rst) on your own, visit the
[Gallery](gallery/index.rst) for more impressions, go through the
[Tutorials](tutorials/index.rst) to learn things in more detail, look at the
available map [Projections](projections/index.rst), and finally do not forget
to check out some [external PyGMT examples](external_resources)!

## Background

PyGMT is a Python wrapper for the
[Generic Mapping Tools (GMT)](https://github.com/GenericMappingTools/gmt),
a command-line program widely used across the Earth, Ocean, and Planetary sciences and
beyond. It provides capabilities for processing spatial data (gridding, filtering,
masking, FFTs, etc) and making high quality plots and maps.

PyGMT is different from Python libraries like [Bokeh](https://bokeh.pydata.org/en/latest/)
and [Matplotlib](https://matplotlib.org/), which have a larger focus on interactivity
and allowing different backends. GMT uses the
[PostScript](https://en.wikipedia.org/wiki/PostScript) format to generate high quality
(static) vector graphics for publications, posters, talks, etc. It is memory efficient
and very fast. The PostScript figures can be converted to other formats like PDF, PNG,
and JPG for use on the web and elsewhere. In fact, PyGMT users will usually not have any
contact with the original PostScript files and get only the more convenient formats like
PDF and PNG.

The project was started in 2017 by [Leonardo Uieda](https://www.leouieda.com) and
[Paul Wessel](https://en.wikipedia.org/wiki/Pål_Wessel) (the co-creator and main developer
of GMT) at the University of Hawaiʻi at Mānoa. Currently the project is maintained by an
[international team](../team) with contributions from
[multiple contributors](https://github.com/GenericMappingTools/pygmt/graphs/contributors)
(see also [AUTHORS.md](https://github.com/GenericMappingTools/pygmt/blob/main/AUTHORS.md)).

We welcome any feedback and ideas! Let us know by submitting
[issues on GitHub](https://github.com/GenericMappingTools/pygmt/issues) or by posting on
our [Discourse forum](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a).

## Project goals

From the beginning, the project has aimed to achieve the following goals:

- Make GMT more accessible to new users.
- Build a Pythonic API for GMT.
- Interface with the GMT C API directly using ctypes (no system calls).
- Support for rich display in the Jupyter notebook.
- Integration with the [scientific Python ecosystem](https://scientific-python.org/):
  `numpy.ndarray` or `pandas.DataFrame` for data tables, `xarray.DataArray` for grids,
  and `geopandas.GeoDataFrame` for geographical data.

## Related projects

Other official GMT wrappers include:

- [GMT.jl](https://github.com/GenericMappingTools/GMT.jl): A Julia wrapper for GMT.
- [gmtmex](https://github.com/GenericMappingTools/gmtmex): A Matlab/Octave wrapper for GMT.

## Funding

The development of PyGMT has been supported by NSF grants
[OCE-1558403](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1558403) and
[EAR-1948602](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1948602).

## License

PyGMT is free software: you can redistribute it and/or modify it under the terms of the
BSD 3-clause License. A copy of this license is provided in
[LICENSE.txt](https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt).
