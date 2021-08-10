PyGMT
=====

    A Python interface for the Generic Mapping Tools

`Documentation (development version) <https://www.pygmt.org/dev>`__ |
`Contact <https://forum.generic-mapping-tools.org>`__ |
`Try Online <https://github.com/GenericMappingTools/try-gmt>`__

.. image:: http://img.shields.io/pypi/v/pygmt.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/pygmt
.. image:: https://github.com/GenericMappingTools/pygmt/workflows/Tests/badge.svg
    :alt: GitHub Actions Tests status
    :target: https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests.yaml
.. image:: https://github.com/GenericMappingTools/pygmt/workflows/GMT%20Dev%20Tests/badge.svg
    :alt: GitHub Actions GMT Dev Tests status
    :target: https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml
.. image:: https://img.shields.io/codecov/c/github/GenericMappingTools/pygmt/main.svg?style=flat-square
    :alt: Test coverage status
    :target: https://codecov.io/gh/GenericMappingTools/pygmt
.. image:: https://img.shields.io/pypi/pyversions/pygmt.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/pygmt
.. image:: https://img.shields.io/discourse/status?label=forum&server=https%3A%2F%2Fforum.generic-mapping-tools.org%2F&style=flat-square
    :alt: Discourse forum
    :target: https://forum.generic-mapping-tools.org
.. image:: https://zenodo.org/badge/DOI/10.5281/3781524.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3781524
.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
    :alt: Contributor Code of Conduct
    :target: CODE_OF_CONDUCT.md

.. placeholder-for-doc-index


Why PyGMT?
----------

A beautiful map is worth a thousand words.
To truly understand how powerful PyGMT is, play with it online on `Binder <https://github.com/GenericMappingTools/try-gmt>`__!
But if you need some convincing first, watch this `1 hour introduction <https://www.youtube.com/watch?v=SSIGJEe0BIk>`__ to PyGMT!

Afterwards, feel free to look at our `Tutorials <https://www.pygmt.org/latest/tutorials>`__
or visit the `PyGMT Gallery <https://www.pygmt.org/latest/gallery>`__.

.. image:: https://user-images.githubusercontent.com/23487320/95393255-c0b72e80-0956-11eb-9471-24429461802b.png
    :alt: Remote Online Sessions for Emerging Seismologists (ROSES): Unit 8 - PyGMT
    :align: center
    :target: https://www.youtube.com/watch?v=SSIGJEe0BIk


Disclaimer
----------

🚨 **This package is still undergoing rapid development.** 🚨

All of the API (functions/classes/interfaces) is subject to change until we reach v1.0.0
as per the `semantic versioning specification <https://semver.org/spec/v2.0.0.html>`__.
There may be non-backward compatible changes as we experiment with new design ideas and
implement new features. **This is not a finished product, use with caution.**

We welcome any feedback and ideas!
Let us know by submitting
`issues on GitHub <https://github.com/GenericMappingTools/pygmt/issues>`__
or by posting on our `Discourse forum <https://forum.generic-mapping-tools.org>`__.

About
-----

PyGMT is a library for processing geospatial and geophysical data and making
publication quality maps and figures. It provides a Pythonic interface for the
`Generic Mapping Tools (GMT) <https://github.com/GenericMappingTools/gmt>`__, a
command-line program widely used in the Earth Sciences.

We rely heavily on new features that have been implemented in GMT 6.0. In particular,
a new *modern execution mode* that greatly simplifies figure creation. **These features
are not available in the 5.4 version of GMT**.


Project goals
-------------

* Make GMT more accessible to new users.
* Build a Pythonic API for GMT.
* Interface with the GMT C API directly using ctypes (no system calls).
* Support for rich display in the Jupyter notebook.
* Integration with the `PyData <https://pydata.org/>`__ ecosystem:
  ``numpy.ndarray`` or ``pandas.DataFrame`` for data tables and
  ``xarray.DataArray`` for grids.


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
<https://github.com/GenericMappingTools/pygmt/blob/main/CODE_OF_CONDUCT.md>`__.
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

    @software{pygmt_2021_5162003,
      author       = {Uieda, Leonardo and
                      Tian, Dongdong and
                      Leong, Wei Ji and
                      Schlitzer, William and
                      Toney, Liam and
                      Grund, Michael and
                      Jones, Meghan and
                      Yao, Jiayuan and
                      Materna, Kathryn and
                      Newton, Tyler and
                      Anant, Abhishek and
                      Ziebarth, Malte and
                      Magen, Yohai and
                      Wessel, Paul},
      title        = {{PyGMT: A Python interface for the Generic Mapping Tools}},
      month        = aug,
      year         = 2021,
      publisher    = {Zenodo},
      version      = {v0.4.1},
      doi          = {10.5281/zenodo.5162003},
      url          = {https://doi.org/10.5281/zenodo.5162003}
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

Other Python wrappers for GMT:

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
      - Numpy
    * - `v0.4.1 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.4.1>`_ (latest release)
      - `v0.4.1 Documentation <https://www.pygmt.org/v0.4.1>`_
      - >=6.2.0
      - >=3.7
      - >=1.17.0
    * - `v0.4.0 <https://github.com/GenericMappingTools/pygmt/releases/tag/v0.4.0>`_
      - `v0.4.0 Documentation <https://www.pygmt.org/v0.4.0>`_
      - >=6.2.0
      - >=3.7
      - >=1.17.0
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

The unstable development documentation, which reflects the `main branch <https://github.com/GenericMappingTools/pygmt>`_
on GitHub, can be found at https://www.pygmt.org/dev/.
