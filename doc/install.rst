.. _install:

Installing
==========

.. note::

    **This package is in early stages of development.**

    We welcome any feedback and ideas!
    Let us know by submitting
    `issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__
    or send us a message on our
    `Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.


Which Python?
-------------

You'll need **Python 3.5 or greater** to run GMT Python.

We recommend using the `Anaconda <http://continuum.io/downloads#all>`__ Python
distribution to ensure you have all dependencies installed and the ``conda``
package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Dependencies
------------

GMT/Python requires the following libraries:

* Current development version of GMT (6.0.0). ``conda`` packages for Linux and
  macOS are available through
  `conda-forge <https://github.com/conda-forge/gmt-feedstock/>`__.
* `numpy <http://www.numpy.org/>`__
* `pandas <https://pandas.pydata.org/>`__
* `xarray <http://xarray.pydata.org/>`__


Installing GMT and other dependencies
-------------------------------------

Before installing GMT/Python,
we must install GMT itself along with the other dependencies.
The easiest way to do this is using the ``conda`` package manager.
We recommend working in an isolated `conda environment
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`__
to avoid issues with competing versions of GMT and its dependencies.

First, we must configure conda to get packages from the `conda-forge
channel <https://conda-forge.org/>`__::

    conda config --add channels conda-forge

Now we can create a conda environment with only Python and ``pip`` installed
(we'll call it ``gmt-python`` but you can change it to whatever you want)::

     conda create --name gmt-python python=3.6 pip

Activate the environment by running::

    source activate gmt-python

From now on, all ``conda`` and ``pip`` commands will take place inside the
environment and won't affect your default installation.

Install the latest version of GMT 6::

    conda install gmt -c conda-forge/label/dev

And finally, install the rest of the dependencies::

    conda install numpy pandas xarray

.. note::

    **Currently, this only works on Linux and macOS.**

    We don't have a GMT conda package for Windows
    (`we're working on it <https://github.com/conda-forge/gmt-feedstock>`__).
    If you know how to
    build GMT from source, you can do that instead of the ``conda install
    gmt``. This is untested and we would love to get feedback from anyone who
    tries.


Installing GMT/Python
---------------------

Now that you have GMT installed and your conda environment activated,
use ``pip`` to install the latest source of GMT/Python from Github::

    pip install https://github.com/GenericMappingTools/gmt-python/archive/master.zip

Alternatively, you can clone the git repository and install using ``pip``::

    git clone https://github.com/GenericMappingTools/gmt-python.git
    cd gmt-python
    pip install .

This will allow you to use the ``gmt`` library from Python.


Testing your install
--------------------

GMT/Python ships with a full test suite.
You can run our tests after you install it but you will need a few extra
dependencies as well (be sure to have your conda env activated)::

    conda install pytest pytest-mpl ipython

Test your installation by running the following inside a Python interpreter::

    import gmt
    gmt.test()


Finding the GMT shared library
------------------------------

Sometimes, GMT/Python will be unable to find the correct version of the GMT
shared library. This can happen if you have multiple versions of GMT installed.

You can tell GMT/Python exactly where to look for ``libgmt`` by setting the
``GMT_LIBRARY_PATH`` environment variable. This should be set to the directory
where ``libgmt.so`` (or ``.dylib``) is found. **Only use this as a last
resort**. Setting the path in this way means that GMT/Python will not be able
to easily find the correct ``libgmt`` when you're changing conda environments.

If you installed GMT using conda using the instructions above and you're using
Linux or Mac, place the following in your ``~/.bashrc`` file::

    export GMT_LIBRARY_PATH=$HOME/anaconda3/envs/gmt-python/lib

You should change ``$HOME/anaconda3`` to wherever you installed Anaconda (this
is the default for Linux).
