PyGMT
=====

    A Python interface for the Generic Mapping Tools

`Documentation (development version) <https://www.pygmt.org/dev>`__ |
`Contact <https://forum.generic-mapping-tools.org>`__ |
`Try Online <https://github.com/GenericMappingTools/try-gmt>`__

.. image:: http://img.shields.io/pypi/v/pygmt.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/pygmt
.. image:: https://img.shields.io/conda/v/conda-forge/pygmt?style=flat-square
    :alt: Latest version on conda-forge
    :target: https://anaconda.org/conda-forge/pygmt
.. image:: https://github.com/GenericMappingTools/pygmt/workflows/Tests/badge.svg
    :alt: GitHub Actions Tests status
    :target: https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests.yaml
.. image:: https://github.com/GenericMappingTools/pygmt/workflows/GMT%20Dev%20Tests/badge.svg
    :alt: GitHub Actions GMT Dev Tests status
    :target: https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml
.. image:: https://codecov.io/gh/GenericMappingTools/pygmt/branch/main/graph/badge.svg?token=78Fu4EWstx
    :alt: Test coverage status
    :target: https://app.codecov.io/gh/GenericMappingTools/pygmt
.. image:: https://img.shields.io/pypi/pyversions/pygmt.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/pygmt
.. image:: https://img.shields.io/discourse/status?label=forum&server=https%3A%2F%2Fforum.generic-mapping-tools.org%2F&style=flat-square
    :alt: Discourse forum
    :target: https://forum.generic-mapping-tools.org
.. image:: https://zenodo.org/badge/DOI/10.5281/3781524.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3781524
.. image:: https://tinyurl.com/y22nb8up
    :alt: PyOpenSci
    :target: https://github.com/pyOpenSci/software-review/issues/43
.. image:: https://img.shields.io/github/license/GenericMappingTools/pygmt?style=flat-square
    :alt: GitHub license
    :target: https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt
.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg
    :alt: Contributor Code of Conduct
    :target: CODE_OF_CONDUCT.md
.. image:: https://img.shields.io/twitter/follow/gmt_dev?style=social
    :alt: Twitter URL
    :target: https://twitter.com/gmt_dev

.. placeholder-for-doc-index


Why PyGMT?
----------

A beautiful map is worth a thousand words.
To truly understand how powerful PyGMT is, play with it online on `Binder <https://github.com/GenericMappingTools/try-gmt>`__!
For a quicker introduction, check out our `3 minute overview <https://youtu.be/4iPnITXrxVU>`__!

Afterwards, feel free to look at our `Tutorials <https://www.pygmt.org/latest/tutorials>`__,
visit the `PyGMT Gallery <https://www.pygmt.org/latest/gallery>`__, and check out
some `external PyGMT examples <https://www.pygmt.org/latest/external_resources.html>`__!

.. image:: https://user-images.githubusercontent.com/14077947/155809878-48b8f235-141b-460a-80ec-08bbf6c36e40.png
    :alt: Quick Introduction to PyGMT YouTube Video
    :align: center
    :target: https://youtu.be/4iPnITXrxVU
    :width: 80%

About
-----

PyGMT is a library for processing geospatial and geophysical data and making
publication quality maps and figures. It provides a Pythonic interface for the
`Generic Mapping Tools (GMT) <https://github.com/GenericMappingTools/gmt>`__, a
command-line program widely used in the Earth Sciences.

Project goals
-------------

* Make GMT more accessible to new users.
* Build a Pythonic API for GMT.
* Interface with the GMT C API directly using ctypes (no system calls).
* Support for rich display in the Jupyter notebook.
* Integration with the `PyData <https://pydata.org/>`__ ecosystem:
  ``numpy.ndarray`` or ``pandas.DataFrame`` for data tables,
  ``xarray.DataArray`` for grids and ``geopandas.GeoDataFrame``
  for geographical data.


Quickstart
----------

Installation
++++++++++++

Simple installation using `conda <https://docs.conda.io/projects/conda/en/latest/user-guide/index.html>`__::

    conda install --channel conda-forge pygmt

If you use `mamba <https://mamba.readthedocs.org/>`__::

    mamba install --channel conda-forge pygmt

For other ways to install ``pygmt``, see `full installation instructions <https://www.pygmt.org/latest/install.html>`__.


Contacting Us
-------------

* Most discussion happens `on GitHub
  <https://github.com/GenericMappingTools/pygmt>`__. Feel free to `open an issue
  <https://github.com/GenericMappingTools/pygmt/issues/new>`__ or comment on any
  open issue or pull request.
* We have a `Discourse forum
  <https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a>`__ where you can ask
  questions and leave comments.


Contributing
------------

Code of conduct
+++++++++++++++

Please note that this project is released with a `Contributor Code of Conduct
<https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

Contributing Guidelines
+++++++++++++++++++++++

Please read our `Contributing Guide
<https://github.com/GenericMappingTools/pygmt/blob/main/CONTRIBUTING.md>`__ to
see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're not ready
to be an open source contributor; that your skills aren't nearly good enough to
contribute. What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equally important contributions include: writing or proof-reading documentation,
suggesting or implementing tests, or even giving feedback about the project (including
giving feedback about the contribution process). If you're coming to the project with
fresh eyes, you might see the errors and assumptions that seasoned contributors have
glossed over. If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from those
mistakes. That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


Citing PyGMT
------------

PyGMT is a community developed project. See the
`AUTHORS.md <https://github.com/GenericMappingTools/pygmt/blob/main/AUTHORS.md>`__
file on GitHub for a list of the people involved and a definition of the term "PyGMT
Developers". Feel free to cite our work in your research using the following BibTeX:

.. code-block::

    @software{pygmt_2022_7481934,
      author       = {Uieda, Leonardo and
                      Tian, Dongdong and
                      Leong, Wei Ji and
                      Jones, Max and
                      Schlitzer, William and
                      Grund, Michael and
                      Toney, Liam and
                      Fröhlich, Yvonne and
                      Yao, Jiayuan and
                      Magen, Yohai and
                      Materna, Kathryn and
                      Belem, Andre and
                      Newton, Tyler and
                      Anant, Abhishek and
                      Ziebarth, Malte and
                      Quinn, Jamie and
                      Wessel, Paul},
      title        = {{PyGMT: A Python interface for the Generic Mapping Tools}},
      month        = dec,
      year         = 2022,
      publisher    = {Zenodo},
      version      = {0.8.0},
      doi          = {10.5281/zenodo.7481934},
      url          = {https://doi.org/10.5281/zenodo.7481934}
    }

To cite a specific version of PyGMT, go to our Zenodo page at
https://doi.org/10.5281/zenodo.3781524 and use the "Export to BibTeX" function there.
It is also strongly recommended to cite the
`GMT6 paper <https://doi.org/10.1029/2019GC008515>`__ (which PyGMT wraps around).
Note that some modules like ``surface`` and ``x2sys`` also have their dedicated citation.
Further information for all these can be found at https://www.generic-mapping-tools.org/cite.


License
-------

PyGMT is free software: you can redistribute it and/or modify it under the terms of
the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/GenericMappingTools/pygmt/blob/main/LICENSE.txt>`__.


Support
-------

The development of PyGMT has been supported by NSF grants
`OCE-1558403 <https://www.nsf.gov/awardsearch/showAward?AWD_ID=1558403>`__ and
`EAR-1948603 <https://www.nsf.gov/awardsearch/showAward?AWD_ID=1948602>`__.


Related projects
----------------

* `GMT.jl <https://github.com/GenericMappingTools/GMT.jl>`__: A Julia wrapper for GMT.
* `gmtmex <https://github.com/GenericMappingTools/gmtmex>`__: A Matlab/Octave wrapper
  for GMT.

Other Python wrappers for GMT (not maintained):

* `gmtpy <https://github.com/emolch/gmtpy>`__ by `Sebastian Heimann <https://github.com/emolch>`__
* `pygmt <https://github.com/ian-r-rose/pygmt>`__ by `Ian Rose <https://github.com/ian-r-rose>`__
* `PyGMT <https://github.com/glimmer-cism/PyGMT>`__  by `Magnus Hagdorn <https://github.com/mhagdorn>`__


Compatibility with GMT/Python/NumPy versions
--------------------------------------------

.. list-table::
    :widths: 25 30 15 20 15
    :header-rows: 1

    * - PyGMT Version
      - Documentation
      - GMT
      - Python
      - NumPy
    * - `Dev <https://github.com/GenericMappingTools/pygmt/milestones>`_ (upcoming release)
      - `Dev Documentation <https://www.pygmt.org/dev>`_ (reflects `main branch <https://github.com/GenericMappingTools/pygmt>`_)
      - >=6.3.0
      - >=3.8
      - >=1.20
    * - `v0.8.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.8.0>`_ (latest release)
      - `v0.8.0 Documentation <https://www.pygmt.org/v0.8.0>`_
      - >=6.3.0
      - >=3.8
      - >=1.20
    * - `v0.7.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.7.0>`_
      - `v0.7.0 Documentation <https://www.pygmt.org/v0.7.0>`_
      - >=6.3.0
      - >=3.8
      - >=1.20
    * - `v0.6.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.6.1>`_
      - `v0.6.1 Documentation <https://www.pygmt.org/v0.6.1>`_
      - >=6.3.0
      - >=3.8
      - >=1.19
    * - `v0.6.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.6.0>`_
      - `v0.6.0 Documentation <https://www.pygmt.org/v0.6.0>`_
      - >=6.3.0
      - >=3.8
      - >=1.19
    * - `v0.5.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.5.0>`_
      - `v0.5.0 Documentation <https://www.pygmt.org/v0.5.0>`_
      - >=6.2.0
      - >=3.7
      - >=1.18
    * - `v0.4.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.4.1>`_
      - `v0.4.1 Documentation <https://www.pygmt.org/v0.4.1>`_
      - >=6.2.0
      - >=3.7
      - >=1.17
    * - `v0.4.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.4.0>`_
      - `v0.4.0 Documentation <https://www.pygmt.org/v0.4.0>`_
      - >=6.2.0
      - >=3.7
      - >=1.17
    * - `v0.3.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.3.1>`_
      - `v0.3.1 Documentation <https://www.pygmt.org/v0.3.1>`_
      - >=6.1.1
      - >=3.7
      -
    * - `v0.3.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.3.0>`_
      - `v0.3.0 Documentation <https://www.pygmt.org/v0.3.0>`_
      - >=6.1.1
      - >=3.7
      -
    * - `v0.2.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.2.1>`_
      - `v0.2.1 Documentation <https://www.pygmt.org/v0.2.1>`_
      - >=6.1.1
      - >=3.6
      -
    * - `v0.2.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.2.0>`_
      - `v0.2.0 Documentation <https://www.pygmt.org/v0.2.0>`_
      - >=6.1.1
      - 3.6 - 3.8
      -
    * - `v0.1.2 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.1.2>`_
      - `v0.1.2 Documentation <https://www.pygmt.org/v0.1.2>`_
      - >=6.0.0
      - 3.6 - 3.8
      -
    * - `v0.1.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.1.1>`_
      - `v0.1.1 Documentation <https://www.pygmt.org/v0.1.1>`_
      - >=6.0.0
      - 3.6 - 3.8
      -
    * - `v0.1.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.1.0>`_
      - `v0.1.0 Documentation <https://www.pygmt.org/v0.1.0>`_
      - >=6.0.0
      - 3.6 - 3.8
      -
