<!--- https://sphinx-design.readthedocs.io/en/rtd-theme/index.html --->

```{title} Home
```

<!--- Add image of PyGMT logo --->
<!--- center image --->
:::{div} sd-d-flex-row sd-align-major-center
```{image} ./_static/pygmtlogo.png
:width: 600px
```

:::
<!--- Add short text what PyGMT is and does --->
<!--- sd-text-center centering, sd-fs fontsize, sd-pt padding top, sd-pb padding bottom --->
:::{div} sd-text-center sd-fs-3 sd-pt-3 sd-pb-3
A Python interface for the [Generic Mapping Tools](https://www.generic-mapping-tools.org/)
:::

:::{div} sd-text-center sd-fs-5 sd-pb-3
PyGMT is a library for processing geospatial and geophysical data and making
publication-quality maps and figures. It provides a Pythonic interface for the
[Generic Mapping Tools (GMT)](https://github.com/GenericMappingTools/gmt), a command-line
program widely used across the Earth, Ocean, and Planetary sciences and beyond.
:::


```{toctree}
:maxdepth: 2
:hidden:
:caption: Getting Started

install.md
intro/index.rst
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Project Overview

overview.md
ecosystem.md
presentations.md
citing.md
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: User Guide

tutorials/index.rst
gallery/index.rst
projections/index.rst
external_resources.md
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Reference Documentation

api/index.rst
techref/index.md
changes.md
minversions.md
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Development

team.md
contributing.md
maintenance.md
```
