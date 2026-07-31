# Overview

## About

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
[Paul Wessel](https://en.wikipedia.org/wiki/Pål_Wessel) (the co-creator and main
developer of GMT) at the University of Hawaiʻi at Mānoa. The development of PyGMT
has been supported by NSF grants [OCE-1558403](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1558403)
and [EAR-1948602](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1948602).

We welcome any feedback and ideas! Let us know by submitting
[issues on GitHub](https://github.com/GenericMappingTools/pygmt/issues) or by posting on
our [Discourse forum](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a).
