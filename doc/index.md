<!--- Reference: https://sphinx-design.readthedocs.io/en/rtd-theme/index.html --->

:::{title} Home
:::

<!--- Add image of PyGMT logo --->
<!--- center image --->
::::{div} sd-d-flex-row sd-align-major-center
:::{image} ./_static/pygmtlogo.png
:width: 600px
:::
::::
<!--- Add short text what PyGMT is and does --->
<!--- sd-text-center centering, sd-fs fontsize, sd-pt padding top, sd-pb padding bottom --->
:::{div} sd-text-center sd-fs-3 sd-pt-3 sd-pb-3
A Python interface for the [Generic Mapping Tools](https://www.generic-mapping-tools.org/)
:::

:::{div} sd-text-center sd-fs-5 sd-pb-3
PyGMT is a library for processing geospatial and geophysical data and making
publication-quality maps and figures. It provides a Pythonic interface for the
[Generic Mapping Tools (GMT)](https://www.generic-mapping-tools.org/), a command-line
program widely used across the Earth, Ocean, and Planetary sciences and beyond.
:::



<!--- Set up grid --->
<!--- Number of default columns screen sizes dependent --->
<!--- extra-small (<576px) small (768px) medium (992px) large screens (>1200px) --->

<!--- Set up card --->
<!--- top bottom left right --->

:::::{grid} 1 3 3 3

::::{grid-item-card}
:margin: 0 3 0 0
<!--- Add icon --->
<!--- 3em size, sd-text-info color --->
{octicon}`rocket;2.5em;sd-text-info` **Getting Started**
^^^
```{button-ref} ../install
:color: secondary
:outline:
:shadow:
Installing
```
```{button-ref} ../intro/index
:color: secondary
:outline:
:shadow:
Intro to PyGMT
```
::::

::::{grid-item-card}
:margin: 0 3 0 0
{octicon}`globe;2.5em;sd-text-info` **Project Overview**
^^^
```{button-ref} ../overview
:color: secondary
:outline:
:shadow:
Why PyGMT
```
```{button-ref} ../ecosystem
:color: secondary
:outline:
:shadow:
PyGMT Ecosystem
```
```{button-ref} ../presentations
:color: secondary
:outline:
:shadow:
Presentations
```
```{button-ref} ../citing
:color: secondary
:outline:
:shadow:
Citing PyGMT
```
::::

::::{grid-item-card}
:margin: 0 3 0 0
{octicon}`mortar-board;2.5em;sd-text-info` **User Guide**
^^^
```{button-ref} ../gallery/index
:color: secondary
:outline:
:shadow:
Gallery
```
```{button-ref} ../tutorials/index
:color: secondary
:outline:
:shadow:
Tutorials
```
```{button-ref} ../projections/index
:color: secondary
:outline:
:shadow:
Projections
```
```{button-ref} ../external_resources
:color: secondary
:outline:
:shadow:
External Resources
```
::::

::::{grid-item-card}
:margin: 0 3 0 0
{octicon}`book;2.5em;sd-text-info` **Reference Guide**
^^^
```{button-ref} ../api/index
:color: secondary
:outline:
:shadow:
API Reference
```
```{button-ref} ../techref/index
:color: secondary
:outline:
:shadow:
Technical Reference
```
```{button-ref} ../changes
:color: secondary
:outline:
:shadow:
Changelog
```
```{button-ref} ../minversions
:color: secondary
:outline:
:shadow:
Minimum Supported Versions
```
::::

::::{grid-item-card}
:margin: 0 3 0 0
{octicon}`terminal;2.5em;sd-text-info` **Development**
^^^
```{button-ref} ../contributing
:color: secondary
:outline:
:shadow:
Contributors Guide
```
```{button-ref} ../maintenance
:color: secondary
:outline:
:shadow:
Maintainers Guide
```
```{button-ref} ../team
:color: secondary
:outline:
:shadow:
PyGMT Team
```
::::

::::{grid-item-card}
:margin: 0 3 0 0
{octicon}`light-bulb;2.5em;sd-text-info` **Getting Help**
^^^
```{button-link} https://forum.generic-mapping-tools.org
:color: secondary
:outline:
:shadow:
{octicon}`comment-discussion;1em;sd-text-info` GMT Forum
```
```{button-link} https://github.com/GenericMappingTools/pygmt
:color: secondary
:outline:
:shadow:
{octicon}`mark-github;1em;sd-text-info` Source Code
```
```{button-link} https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md
:color: secondary
:outline:
:shadow:
{octicon}`code-of-conduct;1em;sd-text-info` Code of Conduct
```
```{button-link} https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt
:color: secondary
:outline:
:shadow:
{octicon}`law;1em;sd-text-info` License
```
::::

:::::



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
:caption: Reference Guide

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
