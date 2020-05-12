PyGMT
=====

    A Python interface for the Generic Mapping Tools

`Documentation (development version) <https://www.pygmt.org/dev>`__ |
`Contact <https://forum.generic-mapping-tools.org>`__ |

.. image:: http://img.shields.io/pypi/v/pygmt.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/pygmt
.. image:: http://img.shields.io/travis/GenericMappingTools/pygmt/master.svg?style=flat-square&label=Linux
    :alt: Travis CI build status
    :target: https://travis-ci.org/GenericMappingTools/pygmt
.. image:: https://img.shields.io/azure-devops/build/GenericMappingTools/7682ad4e-76bb-4775-849e-7c4f8dce4e1a/3/master.svg?label=Mac|Windows&style=flat-square
    :alt: Azure Pipelines build status
    :target: https://dev.azure.com/GenericMappingTools/PyGMT/_build
.. image:: https://img.shields.io/codecov/c/github/GenericMappingTools/pygmt/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://codecov.io/gh/GenericMappingTools/pygmt
.. image:: https://img.shields.io/codacy/grade/e73169dcb8454b3bb0f6cc5389b228b4.svg?style=flat-square&label=codacy
    :alt: Code quality grade on codacy
    :target: https://www.codacy.com/app/leouieda/pygmt
.. image:: https://img.shields.io/pypi/pyversions/pygmt.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/pygmt
.. image:: https://img.shields.io/discourse/status?label=forum&server=https%3A%2F%2Fforum.generic-mapping-tools.org%2F&style=flat-square
    :alt: Discourse forum
    :target: https://forum.generic-mapping-tools.org
.. image:: https://zenodo.org/badge/DOI/10.5281/3781524.svg
    :alt: Digital Object Identifier for the Zenodo archive
    :target: https://doi.org/10.5281/zenodo.3781524

.. placeholder-for-doc-index


Disclaimer
----------

🚨 **This package is still undergoing rapid development.** 🚨

All of the API (functions/classes/interfaces) is subject to change until we reach v1.0.0
as per the `semantic versioning specification <https://semver.org/spec/v2.0.0.html>`__.
There may be non-backward compatible changes as we experiment with new design ideas and
implement new features. **This is not a finished product, use with caution**

We welcome any feedback and ideas!
Let us know by submitting
`issues on Github <https://github.com/GenericMappingTools/pygmt/issues>`__
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
* Integration with the Scipy stack: numpy.ndarray or pandas.DataFrame for data tables
  and xarray.DataArray for grids.


Contacting Us
-------------

* Most discussion happens `on Github
  <https://github.com/GenericMappingTools/pygmt>`__. Feel free to `open an issue
  <https://github.com/GenericMappingTools/pygmt/issues/new>`__ or comment on any
  open issue or pull request.
* We have a `Discourse forum <https://forum.generic-mapping-tools.org>`__
  where you can ask questions and leave comments.
* This project is released with a `Contributor Code of Conduct
  <https://github.com/GenericMappingTools/pygmt/blob/master/CODE_OF_CONDUCT.md>`__.
  By participating in this project you agree to abide by its terms.


Contributing
------------

Code of conduct
+++++++++++++++

Please note that this project is released with a `Contributor Code of Conduct
<https://github.com/GenericMappingTools/pygmt/blob/master/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

Contributing Guidelines
+++++++++++++++++++++++

Please read our `Contributing Guide
<https://github.com/GenericMappingTools/pygmt/blob/master/CONTRIBUTING.md>`__ to
see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're not ready
to be an open source contributor; that your skills aren't nearly good enough to
contribute. What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equality important contributions include: writing or proof-reading documentation,
suggesting or implementing tests, or even giving feedback about the project (including
giving feedback about the contribution process). If you're coming to the project with
fresh eyes, you might see the errors and assumptions that seasoned contributors have
glossed over. If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from those
mistakes. That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


Who we are
----------

PyGMT is a community developed project. See the
`AUTHORS.md <https://github.com/GenericMappingTools/pygmt/blob/master/AUTHORS.md>`__
file on Github for a list of the people involved and a definition of the term "PyGMT
Developers".


License
-------

PyGMT is free software: you can redistribute it and/or modify it under the terms of
the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/GenericMappingTools/pygmt/blob/master/LICENSE.txt>`__.


Support
-------

The development of PyGMT was funded by
`NSF grant OCE-1558403 <https://www.nsf.gov/awardsearch/showAward?AWD_ID=1558403>`__.


Related projects
----------------

* `GMT.jl <https://github.com/GenericMappingTools/GMT.jl>`__: A Julia wrapper for GMT.
* `gmtmex <https://github.com/GenericMappingTools/gmtmex>`__: A Matlab/Octave wrapper
  for GMT.

Other Python wrappers for GMT:

* `gmtpy <https://github.com/emolch/gmtpy>`__ by `Sebastian Heimann <https://github.com/emolch>`__
* `pygmt <https://github.com/ian-r-rose/pygmt>`__ by `Ian Rose <https://github.com/ian-r-rose>`__
* `PyGMT <https://github.com/glimmer-cism/PyGMT>`__  by `Magnus Hagdorn <https://github.com/mhagdorn>`__


Documentation for other versions
--------------------------------
* `Development <https://www.pygmt.org/dev>`__ (reflects the *master* branch on
  Github)
* `Latest release <https://www.pygmt.org/latest>`__
* `v0.1.0 <https://www.pygmt.org/v0.1.0>`__
* `v0.0.1a0 <https://www.pygmt.org/0.0.1a0>`__
