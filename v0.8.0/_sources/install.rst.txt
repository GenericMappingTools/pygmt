.. _install:

Installing
==========

Quickstart
----------

The fastest way to install PyGMT is with the
`conda <https://docs.conda.io/projects/conda/en/latest/user-guide/index.html>`__
or `mamba <https://mamba.readthedocs.io/en/latest/>`__
package manager which takes care of setting up a virtual environment, as well
as the installation of GMT and all the dependencies PyGMT depends on:

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda create --name pygmt --channel conda-forge pygmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba create --name pygmt --channel conda-forge pygmt

To activate the virtual environment, you can do:

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda activate pygmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba activate pygmt

After this, check that everything works by running the following in a Python
interpreter (e.g., in a Jupyter notebook)::

    import pygmt
    pygmt.show_versions()

You are now ready to make you first figure!
Start by looking at the tutorials on our sidebar, good luck!

.. note::

    The sections below provide more detailed, step by step instructions to
    install and test PyGMT for those who may have a slightly different setup or
    want to install the latest development version.

Which Python?
-------------

PyGMT is tested to run on **Python 3.8 or greater**.

We recommend using the `Anaconda <https://www.anaconda.com/distribution>`__
Python distribution to ensure you have all dependencies installed and the
`conda <https://docs.conda.io/projects/conda/en/latest/>`__
package manager is available. Installing Anaconda does not require administrative
rights to your computer and doesn't interfere with any other Python
installations on your system.


Which GMT?
----------

PyGMT requires Generic Mapping Tools (GMT) version 6 as a minimum, which is the
latest released version that can be found at
the `GMT official site <https://www.generic-mapping-tools.org>`__.
We need the latest GMT (>=6.3.0) since there are many changes being made to GMT
itself in response to the development of PyGMT, mainly the new
:gmt-docs:`modern execution mode <cookbook/introduction.html#modern-and-classic-mode>`.

Compiled conda packages of GMT for Linux, macOS and Windows are provided
through `conda-forge <https://anaconda.org/conda-forge/gmt>`__.
Advanced users can also
`build GMT from source <https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md>`__
instead.

We recommend following the instructions further on to install GMT 6.

Dependencies
------------

PyGMT requires the following libraries to be installed:

* `numpy <https://numpy.org>`__ (>= 1.20)
* `pandas <https://pandas.pydata.org>`__
* `xarray <https://xarray.dev/>`__
* `netCDF4 <https://unidata.github.io/netcdf4-python>`__
* `packaging <https://packaging.pypa.io>`__

The following are optional dependencies:

* `IPython <https://ipython.org>`__: For embedding the figures in Jupyter notebooks (recommended).
* `GeoPandas <https://geopandas.org>`__: For using and plotting GeoDataFrame objects.

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
want):

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda create --name pygmt python=3.9 numpy pandas xarray netcdf4 packaging gmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba create --name pygmt python=3.9 numpy pandas xarray netcdf4 packaging gmt

Activate the environment by running the following (**do not forget this step!**):

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda activate pygmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba activate pygmt

From now on, all commands will take place inside the conda virtual environment
called ``pygmt`` and won't affect your default ``base`` installation.


Installing PyGMT
----------------

Now that you have GMT installed and your conda virtual environment activated,
you can install PyGMT using any of the following methods:

Using conda/mamba (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This installs the latest stable release of PyGMT from
`conda-forge <https://anaconda.org/conda-forge/pygmt>`__:

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda install pygmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba install pygmt

This upgrades the installed PyGMT version to be the latest stable release:

.. tab-set::

    .. tab-item:: conda
        :sync: conda

        ::

            conda update pygmt

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba update pygmt

Using pip
~~~~~~~~~

This installs the latest stable release from
`PyPI <https://pypi.org/project/pygmt>`__::

    pip install pygmt

.. tip::

   You can also run ``pip install pygmt[all]`` to install pygmt with
   all of its optional dependencies.

Alternatively, you can install the latest development version from
`TestPyPI <https://test.pypi.org/project/pygmt>`__::

    pip install --pre --extra-index-url https://test.pypi.org/simple/ pygmt

To upgrade the installed stable release or development version to be the latest
one, just add ``--upgrade`` to the corresponding command above.

Any of the above methods (conda/pip) should allow you to use the PyGMT package
from Python.


Testing your install
--------------------

To ensure that PyGMT and its dependencies are installed correctly, run the
following in your Python interpreter::

    import pygmt
    pygmt.show_versions()

    fig = pygmt.Figure()
    fig.coast(region="g", frame=True, shorelines=1)
    fig.show()

If you see a global map with shorelines, then you're all set.


Finding the GMT shared library
------------------------------

Sometimes, PyGMT will be unable to find the correct version of the GMT shared
library (``libgmt``).
This can happen if you have multiple versions of GMT installed.

You can tell PyGMT exactly where to look for ``libgmt`` by setting the
``GMT_LIBRARY_PATH`` environment variable to the directory where ``libgmt.so``,
``libgmt.dylib`` or ``gmt.dll`` can be found on Linux, macOS or Windows,
respectively.

For Linux/macOS, add the following line to your shell configuration file
(usually ``~/.bashrc`` for Bash on Linux and ``~/.zshrc`` for Zsh on macOS)::

    export GMT_LIBRARY_PATH=$HOME/anaconda3/envs/pygmt/lib

For Windows, add the ``GMT_LIBRARY_PATH`` environment variable following these
`instructions <https://www.wikihow.com/Create-an-Environment-Variable-in-Windows-10>`__
and set its value to a path like::

    C:\Users\USERNAME\Anaconda3\envs\pygmt\Library\bin\

Notes for Jupyter users
-----------------------

If you can successfully import pygmt in a Python interpreter or IPython, but
get a ``ModuleNotFoundError`` when importing pygmt in Jupyter, you may need to
install a ``pygmt`` kernel following the commands below::

    conda activate pygmt
    python -m ipykernel install --user --name pygmt  # install conda environment properly
    jupyter kernelspec list --json

After that, you need to restart Jupyter, open your notebook, select the
``pygmt`` kernel and then import pygmt.
