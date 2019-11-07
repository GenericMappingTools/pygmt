.. _install:

Installing
==========

.. note::

   🚨 **This package is in the early stages of design and implementation.** 🚨

    We welcome any feedback and ideas!
    Let us know by submitting
    `issues on Github <https://github.com/GenericMappingTools/pygmt/issues>`__
    or by posting on our `Discourse forum <https://forum.generic-mapping-tools.org>`__.


Which Python?
-------------

You'll need **Python 3.6 or greater** to run PyGMT.

We recommend using the `Anaconda <https://www.anaconda.com/distribution>`__ Python
distribution to ensure you have all dependencies installed and the ``conda``
package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Which GMT?
----------

PyGMT requires Generic Mapping Tools (GMT) version 6 as a minimum, which is the latest
released version that can be found at
`this website <https://www.generic-mapping-tools.org>`__.

We need the very latest GMT since there are many changes being made to GMT itself in
response to the development of PyGMT, mainly the new
`modern execution mode <https://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.

Compiled conda packages of GMT for Linux, Mac and Windows are provided through
`conda-forge <https://anaconda.org/conda-forge/gmt>`__.
Advanced users can also
`build GMT from source <https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md>`__
instead, which is not so recommended but we would love to get feedback from anyone who
tries.

We recommend following the instructions further on to install GMT 6.

Dependencies
------------

PyGMT requires the following libraries:

* `numpy <http://www.numpy.org/>`__
* `pandas <https://pandas.pydata.org/>`__
* `xarray <http://xarray.pydata.org/>`__
* `packaging <https://pypi.org/project/packaging/>`__

The following are optional (but recommended) dependencies:

* `IPython <https://ipython.org/>`__: For embedding the figures in Jupyter notebooks.


Installing GMT and other dependencies
-------------------------------------

Before installing PyGMT, we must install GMT itself along with the other dependencies.
The easiest way to do this is using the ``conda`` package manager.
We recommend working in an isolated
`conda environment <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
to avoid issues with competing versions of its dependencies.

First, we must configure conda to get packages from the
`conda-forge channel <https://conda-forge.org/>`__::

    conda config --prepend channels conda-forge

Now we can create a new conda environment with Python and all our dependencies installed
(we'll call it ``pygmt`` but you can change it to whatever you want)::

     conda create --name pygmt python=3.6 pip numpy pandas xarray packaging gmt=6.0.0

Activate the environment by running::

    conda activate pygmt

From now on, all commands will take place inside the conda virtual environment and won't
affect your default installation.

.. note::

    **Currently, this has only been tested to work on Linux and macOS.**
    We don't have tests running on Windows yet, so things might be broken.
    Please report any errors by `creating an issue on Github <https://github.com/GenericMappingTools/pygmt/issues>`__.

Installing PyGMT
----------------

Now that you have GMT installed and your conda environment activated,
use ``pip`` to install the latest source of PyGMT from Github::

    pip install https://github.com/GenericMappingTools/pygmt/archive/master.zip

Alternatively, you can clone the git repository and install using ``pip``::

    git clone https://github.com/GenericMappingTools/pygmt.git
    cd pygmt
    pip install .

This will allow you to use the ``pygmt`` library from Python.


Testing your install
--------------------

PyGMT ships with a full test suite.
You can run our tests after you install it but you will need a few extra dependencies as
well (be sure to have your conda env activated)::

    conda install pytest pytest-mpl sphinx jinja2 docutils ipython

Test your installation by running the following inside a Python interpreter::

    import pygmt
    pygmt.test()


Finding the GMT shared library
------------------------------

Sometimes, PyGMT will be unable to find the correct version of the GMT shared
library.
This can happen if you have multiple versions of GMT installed.

You can tell PyGMT exactly where to look for ``libgmt`` by setting the
``GMT_LIBRARY_PATH`` environment variable.
This should be set to the directory where ``libgmt.so``, ``libgmt.dylib`` or ``gmt.dll``
can be found for Linux, MacOS and Windows respectively.
e.g. in a terminal run::

   export GMT_LIBRARY_PATH=$HOME/anaconda3/envs/pygmt/lib
