.. _install:

Installing
==========

Quickstart
----------

The fastest way to install PyGMT is with the
`mamba <https://mamba.readthedocs.io/en/latest/>`__ or
`conda <https://docs.conda.io/projects/conda/en/latest/user-guide/index.html>`__
package manager which takes care of setting up a virtual environment, as well
as the installation of GMT and all the dependencies PyGMT depends on:

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba create --name pygmt --channel conda-forge pygmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda create --name pygmt --channel conda-forge pygmt

To activate the virtual environment, you can do:

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba activate pygmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda activate pygmt

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

PyGMT is tested to run on Python |requires_python|.

We recommend using the `Mambaforge <https://github.com/conda-forge/miniforge#mambaforge>`__
Python distribution to ensure you have all dependencies installed and the
`mamba <https://mamba.readthedocs.io/en/stable/user_guide/mamba.html>`__
package manager in the base environment. Installing Mambaforge does not require
administrative rights to your computer and doesn't interfere with any other Python
installations on your system.


Which GMT?
----------

PyGMT requires Generic Mapping Tools (GMT) |requires_gmt| since there
are many changes being made to GMT itself in response to the development of PyGMT,
mainly the new :gmt-docs:`modern execution mode <cookbook/introduction.html#modern-and-classic-mode>`.

Compiled conda packages of GMT for Linux, macOS and Windows are provided
through `conda-forge <https://anaconda.org/conda-forge/gmt>`__.
Advanced users can also
`build GMT from source <https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md>`__
instead.

We recommend following the instructions further on to install GMT 6.

Dependencies
------------

PyGMT requires the following libraries to be installed:

* `numpy <https://numpy.org>`__ (>= 1.22)
* `pandas <https://pandas.pydata.org>`__
* `xarray <https://xarray.dev/>`__
* `netCDF4 <https://unidata.github.io/netcdf4-python>`__
* `packaging <https://packaging.pypa.io>`__

The following are optional dependencies:

* `IPython <https://ipython.org>`__: For embedding the figures in Jupyter notebooks (recommended).
* `Contextily <https://contextily.readthedocs.io>`__: For retrieving tile maps from the internet.
* `GeoPandas <https://geopandas.org>`__: For using and plotting GeoDataFrame objects.
* `RioXarray <https://corteva.github.io/rioxarray>`__: For saving multi-band rasters to GeoTIFFs.

Installing GMT and other dependencies
-------------------------------------

Before installing PyGMT, we must install GMT itself along with the other
dependencies. The easiest way to do this is via the ``mamba`` or ``conda`` package manager.
We recommend working in an isolated
`virtual environment <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
to avoid issues with conflicting versions of dependencies.

First, we must configure conda to get packages from the
`conda-forge channel <https://conda-forge.org/>`__::

    conda config --prepend channels conda-forge

Now we can create a new virtual environment with Python and all our dependencies
installed (we'll call it ``pygmt`` but feel free to change it to whatever you
want):

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba create --name pygmt python=3.11 numpy pandas xarray netcdf4 packaging gmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda create --name pygmt python=3.11 numpy pandas xarray netcdf4 packaging gmt

Activate the environment by running the following (**do not forget this step!**):

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba activate pygmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda activate pygmt

From now on, all commands will take place inside the virtual environment called
``pygmt`` and won't affect your default ``base`` installation.


Installing PyGMT
----------------

Now that you have GMT installed and your virtual environment activated, you can
install PyGMT using any of the following methods:

Using mamba/conda (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This installs the latest stable release of PyGMT from
`conda-forge <https://anaconda.org/conda-forge/pygmt>`__:

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba install pygmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda install pygmt

This upgrades the installed PyGMT version to be the latest stable release:

.. tab-set::

    .. tab-item:: mamba
        :sync: mamba

        ::

            mamba update pygmt

    .. tab-item:: conda
        :sync: conda

        ::

            conda update pygmt

Using pip
~~~~~~~~~

This installs the latest stable release from
`PyPI <https://pypi.org/project/pygmt>`__::

    python -m pip install pygmt

.. tip::

   You can also run ``python -m pip install pygmt[all]`` to install pygmt with
   all of its optional dependencies.

Alternatively, you can install the latest development version from
`TestPyPI <https://test.pypi.org/project/pygmt>`__::

    python -m pip install --pre --extra-index-url https://test.pypi.org/simple/ pygmt

To upgrade the installed stable release or development version to be the latest
one, just add ``--upgrade`` to the corresponding command above.

Any of the above methods (mamba/conda/pip) should allow you to use the PyGMT
package from Python.

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

    export GMT_LIBRARY_PATH=$HOME/mambaforge/envs/pygmt/lib

For Windows, add the ``GMT_LIBRARY_PATH`` environment variable following these
`instructions <https://www.wikihow.com/Create-an-Environment-Variable-in-Windows-10>`__
and set its value to a path like::

    C:\Users\USERNAME\Mambaforge\envs\pygmt\Library\bin\

Notes for Jupyter users
-----------------------

If you can successfully import pygmt in a Python interpreter or IPython, but
get a ``ModuleNotFoundError`` when importing pygmt in Jupyter, you may need to
activate your ``pygmt`` virtual environment (using ``mamba activate pygmt`` or
``conda activate pygmt``) and install a ``pygmt`` kernel following the commands below::

    python -m ipykernel install --user --name pygmt  # install virtual environment properly
    jupyter kernelspec list --json

After that, you need to restart Jupyter, open your notebook, select the
``pygmt`` kernel and then import pygmt.
