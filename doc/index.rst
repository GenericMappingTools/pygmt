.. title:: Home

.. raw:: html

    <div class="banner">
        <h1>GMT/Python</h1>
        <h2>
            A modern Python interface for the
            <a href="http://gmt.soest.hawaii.edu/">Generic Mapping Tools</a>
        </h2>
    </div>


Getting started
---------------

1. :ref:`Install <install>` (tested and working on Linux and OSX)
2. Follow the :ref:`first-steps.ipynb` tutorial Jupyter notebook.
3. Take a look at the :ref:`api` for a list of modules that are already
   available.


.. note::

    **This package is in early stages development**.

    We welcome any feedback and ideas!
    Let us know by submitting
    `issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__
    or send us a message on our
    `Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.


Project goals
-------------

* Build a modern Pythonic API that appeals to Python programmers who want to
  use GMT.
* Implement readable and explicit aliases for the GMT command-line arguments
  (``region`` instead of ``R``, ``projection`` instead of ``J``, etc).
* Use the new `GMT modern mode
  <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__ for
  simplified execution and figure generation.
* Interface with the GMT C API directly using
  `ctypes <https://docs.python.org/3/library/ctypes.html>`__ (no system calls).
* Integration with the `Jupyter notebook <http://jupyter.org/>`__ to display
  plots and maps inline.
* Input and output using Python native containers: numpy ``ndarray`` or pandas
  ``DataFrame`` for data tables and `xarray <http://xarray.pydata.org>`__
  ``Dataset`` for netCDF grids.


Contacting Us
-------------

* Most discussion happens `on Github <https://github.com/GenericMappingTools/gmt-python>`__.
  Feel free to `open an issue
  <https://github.com/GenericMappingTools/gmt-python/issues/new>`__ or comment
  on any open issue or pull request.
* We have `chat room on Gitter <https://gitter.im/GenericMappingTools/gmt-python>`__
  where you can ask questions and leave comments.
* Please note that this project is released with a `Contributor Code of Conduct
  <https://github.com/GenericMappingTools/gmt-python/blob/master/CODE_OF_CONDUCT.md>`__.
  By participating in this project you agree to abide by its terms.


Contributing
------------

Please read our
`Contributing Guide <https://github.com/GenericMappingTools/gmt-python/blob/master/CONTRIBUTING.md>`__
to see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're
not ready to be an open source contributor; that your skills aren't nearly good
enough to contribute.
What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equality important contributions include:
writing or proof-reading documentation, suggesting or implementing tests, or
even giving feedback about the project (including giving feedback about the
contribution process).
If you're coming to the project with fresh eyes, you might see the errors and
assumptions that seasoned contributors have glossed over.
If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from
those mistakes.
That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


Related projects
----------------

* `GMT.jl <https://github.com/GenericMappingTools/GMT.jl>`__ -- A Julia wrapper
  for GMT.
* `gmtmex <https://github.com/GenericMappingTools/GMT.jl>`__ -- A Matlab/Octave
  wrapper for GMT.

Other Python wrappers for GMT:

* `gmtpy <https://github.com/emolch/gmtpy>`__ by
  `Sebastian Heimann <https://github.com/emolch>`__
* `pygmt <https://github.com/ian-r-rose/pygmt>`__ by
  `Ian Rose <https://github.com/ian-r-rose>`__
* `PyGMT <https://github.com/glimmer-cism/PyGMT>`__  by
  `Magnus Hagdorn <https://github.com/mhagdorn>`__


License
-------

GMT/Python is free software: you can redistribute it and/or modify it under the
terms of the :ref:`BSD 3-clause License <license>`.



.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Documentation

    first-steps.ipynb
    install.rst
    api/index.rst
    design.rst
    license.rst
