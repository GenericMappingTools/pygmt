.. _install:

Installing
==========

.. note::

   🚨 **This package is in the early stages of design and implementation.** 🚨

    We welcome any feedback and ideas!
    Let us know by submitting
    `issues on GitHub <https://github.com/GenericMappingTools/pygmt/issues>`__
    or by posting on our `Discourse forum
    <https://forum.generic-mapping-tools.org/c/questions/pygmt-q-a>`__.


Quickstart
----------

The fastest way to install PyGMT is with the
`conda <https://docs.conda.io/projects/conda/en/latest/user-guide/index.html>`__
package manager which takes care of setting up a virtual environment, as well
as the installation of GMT and all the dependencies PyGMT depends on::

    conda create --name pygmt --channel conda-forge pygmt

To activate the virtual environment, you can do::

    conda activate pygmt

After this, check that everything works by running the following in a Python
interpreter. If you are using Jupyter, make sure you have connected to the
'pygmt' kernel before running the below::

    import pygmt
    pygmt.show_versions()

You are now ready to make you first figure!
Start by looking at the tutorials on our sidebar, good luck!

The sections below provide a more detailed, step by step instructions to
installing and testing PyGMT for those who may have a slightly different setup.

Which Python?
-------------

PyGMT is tested to run on **Python 3.7 or greater**. Older Python versions may
work, but there is no guarantee that PyGMT will behave as expected.

We recommend using the `Anaconda <https://www.anaconda.com/distribution>`__
Python distribution to ensure you have all dependencies installed and the
``conda`` package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Which GMT?
----------

PyGMT requires Generic Mapping Tools (GMT) version 6 as a minimum, which is the
latest released version that can be found at
the `GMT official site <https://www.generic-mapping-tools.org>`__.
We need the latest GMT (>=6.1.1) since there are many changes being made to GMT
itself in response to the development of PyGMT, mainly the new
`modern execution mode <https://docs.generic-mapping-tools.org/latest/cookbook/introduction.html#modern-and-classic-mode>`__.

Compiled conda packages of GMT for Linux, macOS and Windows are provided
through `conda-forge <https://anaconda.org/conda-forge/gmt>`__.
Advanced users can also
`build GMT from source <https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md>`__
instead, which is not so recommended but we would love to get feedback from
anyone who tries.

We recommend following the instructions further on to install GMT 6.

Dependencies
------------

PyGMT requires the following libraries:

* `numpy <http://www.numpy.org/>`__
* `pandas <https://pandas.pydata.org/>`__
* `xarray <http://xarray.pydata.org/>`__
* `netCDF4 <https://github.com/Unidata/netcdf4-python>`__
* `packaging <https://pypi.org/project/packaging/>`__

The following are optional (but recommended) dependencies:

* `IPython <https://ipython.org/>`__: For embedding the figures in Jupyter
notebooks.


Installing GMT and other dependencies
-------------------------------------

Before installing PyGMT, we must install GMT itself along with the other
dependencies. The easiest way to do this is via the ``conda`` package manager.
We recommend working in an isolated
`conda environment <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
to avoid issues with conflicting versions of dependencies.

First, we must configure conda to get packages from the
`conda-forge channel <https://conda-forge.org/>`__::

    conda config --prepend channels conda-forge

Now we can create a new conda environment with Python and all our dependencies
installed (we'll call it ``pygmt`` but feel free to change it to whatever you
want)::

     conda create --name pygmt python=3.9 pip numpy pandas xarray netcdf4 packaging gmt

Activate the environment by running the following (**do not forget this step!**))::

    conda activate pygmt

From now on, all commands will take place inside the conda virtual environment
called 'pygmt' and won't affect your default 'base' installation.


Installing PyGMT
----------------

Now that you have GMT installed and your conda virtual environment activated,
you can install PyGMT using any of the following methods:

Using conda (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~

This installs the latest stable release of PyGMT from
`conda-forge <https://anaconda.org/conda-forge/pygmt>`__::

    conda install pygmt

Using pip
~~~~~~~~~

This installs the latest stable release from
`PyPI <https://pypi.org/project/pygmt>`__::

    pip install pygmt

Alternatively, you can install the latest development version from
`TestPyPI <https://test.pypi.org/project/pygmt>`__::

    pip install --pre --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pygmt

or from PyGMT's GitHub repository (slower as it downloads the whole archive)::

    pip install git+https://github.com/GenericMappingTools/pygmt.git#egg=pygmt

Any of the above methods (conda/pip) should allow you to use the ``pygmt``
library from Python.


Testing your install
--------------------

Quick check
~~~~~~~~~~~

To ensure that PyGMT and its depedencies are installed correctly, run the
following in your Python interpreter::

    import pygmt
    pygmt.show_versions()

Or run this in the command line::

    python -c "import pygmt; pygmt.show_versions()


Full test (optional)
~~~~~~~~~~~~~~~~~~~~

PyGMT ships with a full test suite.
You can run our tests after you install it but you will need a few extra
dependencies as well (be sure to have your conda environment activated)::

    conda install pytest pytest-mpl ipython

Test your installation by running the following inside a Python interpreter::

    import pygmt
    pygmt.show_versions()
    pygmt.test()


Finding the GMT shared library
------------------------------

Sometimes, PyGMT will be unable to find the correct version of the GMT shared
library.
This can happen if you have multiple versions of GMT installed.

You can tell PyGMT exactly where to look for ``libgmt`` by setting the
``GMT_LIBRARY_PATH`` environment variable.
This should be set to the directory where ``libgmt.so``, ``libgmt.dylib`` or
``gmt.dll`` can be found for Linux, macOS and Windows respectively.
e.g. on a command line, run::

    # Linux/macOS
    export GMT_LIBRARY_PATH=$HOME/anaconda3/envs/pygmt/lib
    # Windows
    set "GMT_LIBRARY_PATH=C:\Users\USERNAME\Anaconda3\envs\pygmt\Library\bin\"
