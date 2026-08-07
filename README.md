<picture align="center">
  <source media="(prefers-color-scheme: dark)" style="width: 65%" srcset="doc/_static/pygmtlogo_dark.png">
  <img alt="PyGMT - A Python interface for the Generic Mapping Tools" style="width: 65%" src="doc/_static/pygmtlogo.png">
</picture>

# A Python interface for the [Generic Mapping Tools](https://www.generic-mapping-tools.org/)

[![GitHub Release](https://img.shields.io/github/v/release/GenericMappingTools/pygmt?color=1f77b4)](https://github.com/GenericMappingTools/pygmt/releases)
[![Latest version on PyPI](https://img.shields.io/pypi/v/pygmt?color=1f77b4)](https://pypi.org/project/pygmt)
[![Latest version on conda-forge](https://img.shields.io/conda/v/conda-forge/pygmt?color=1f77b4)](https://anaconda.org/conda-forge/pygmt)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/pygmt?color=1f77b4)](https://pypi.org/project/pygmt) <br>
[![PyGMT paper](https://img.shields.io/badge/G3%20Paper%20DOI-10.1029/2026GC013105-2ca02c)](https://doi.org/10.1029/2026GC013105)
[![Digital Object Identifier for the Zenodo archive](https://img.shields.io/badge/Zenodo%20DOI-10.5281/zenodo.3781524-2ca02c)](https://doi.org/10.5281/zenodo.3781524)
[![GitHub license](https://img.shields.io/github/license/GenericMappingTools/pygmt?color=2ca02c)](https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt) <br>
[![GitHub Actions Tests status](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests.yaml/badge.svg)](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests.yaml)
[![GitHub Actions GMT Dev Tests status](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml/badge.svg)](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml)
[![Test coverage status](https://codecov.io/gh/GenericMappingTools/pygmt/graph/badge.svg?token=78Fu4EWstx)](https://app.codecov.io/gh/GenericMappingTools/pygmt)


## Why PyGMT?

PyGMT is a library for processing geospatial and geophysical data and making
publication-quality maps and figures. It provides a Pythonic interface for the
[Generic Mapping Tools (GMT)](https://github.com/GenericMappingTools/gmt), a command-line
program widely used across the Earth, Ocean, and Planetary sciences and beyond.

A beautiful map is worth a thousand words. To truly understand how powerful PyGMT is,
play with it online on [Binder](https://github.com/GenericMappingTools/try-gmt)! For a
quicker introduction, check out our [3 minute overview](https://youtu.be/4iPnITXrxVU)!

## Quickstart

Install PyGMT using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html):

```bash
conda install --channel conda-forge pygmt
```

Then try the following example in a Python interpreter or Jupyter notebook. You should
see a global map with land and water masses colored in tan and lightblue, respectively,
with the semi-transparent text "PyGMT" on top.

```python
import pygmt

fig = pygmt.Figure()
fig.basemap(projection="R7c", region=[0, 360, -90, 90], frame=True)
fig.coast(land="tan", water="lightblue")
fig.text(position="MC", text="PyGMT", font="40p,AvantGarde-Book,red@75")
fig.show()
```
For other ways to install PyGMT and more examples, please visit the
[PyGMT documentation](https://www.pygmt.org/).

## Dependencies

**Required**: GMT, Python, NumPy, pandas, xarray

**Optional**: GeoPandas, contextily, rioarray

For details on the versions, see [Minimum supported Versions](https://www.pygmt.org/latest/minversions.html)
and [PyGMT Ecosystem](https://www.pygmt.org/latest/ecosystem.html).

## Documentation

- [Gallery](https://www.pygmt.org/latest/gallery/index.html) and [Tutorials](https://www.pygmt.org/latest/tutorials/index.html)
- [Minimum Supported Versions](https://www.pygmt.org/dev/minversions.html)
- [Citing PyGMT](https://www.pygmt.org/dev/citing.html)
- [Related Projects](https://www.pygmt.org/dev/overview.html#related-projects)
- [Funding](https://www.pygmt.org/dev/overview.html#funding)

## Contacting us

- Most discussion happens [on GitHub](https://github.com/GenericMappingTools/pygmt).
  Feel free to [open an issue](https://github.com/GenericMappingTools/pygmt/issues/new)
  or comment on any open issue or pull request.
- We have a [Discourse forum](https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a)
  where you can ask questions and leave comments.

## Code of conduct

We want everyone to feel welcome to contribute to this project and participate in
discussions. In that spirit please have a look at our
[Code of Conduct](https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md).

## Contributing

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready
to be an open source contributor; that your skills aren't nearly good enough to
contribute. What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code.** Equally important contributions
include: writing or proof-reading documentation, suggesting or implementing tests, or
even giving feedback about the project (including giving feedback about the contribution
process). If you're coming to the project with fresh eyes, you might see the errors and
assumptions that seasoned contributors have glossed over. If you can write any code at
all, you can contribute code to open source. We are constantly trying out new skills,
making mistakes, and learning from those mistakes. That's how we all improve and we are
happy to help others learn.

Please read our [Contributing Guide](https://github.com/GenericMappingTools/pygmt/blob/main/CONTRIBUTING.md)
to see how you can help and give feedback.

*This disclaimer was adapted from the* [MetPy project](https://github.com/Unidata/MetPy).

## Related projects

Other official wrappers for GMT:

- [GMT.jl](https://github.com/GenericMappingTools/GMT.jl): A Julia wrapper for GMT.
- [gmtmex](https://github.com/GenericMappingTools/gmtmex): A Matlab/Octave wrapper for GMT.

## Funding

The development of PyGMT has been supported by NSF grants
[OCE-1558403](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1558403) and
[EAR-1948602](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=1948602).

## License

PyGMT is free software: you can redistribute it and/or modify it under the terms of the
**BSD 3-clause License**. A copy of this license is provided in
[LICENSE.txt](https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt).
