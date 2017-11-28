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
  OSX are available through
  `conda-forge <https://github.com/conda-forge/gmt-feedstock/>`__.
* numpy


Installing GMT and other dependencies
-------------------------------------

Before installing GMT/Python,
we must install GMT itself along with the other dependencies.
The easiest way to do this is using the ``conda`` package manager.
We recommend working in an isolated `conda environment
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`__
to avoid issues with competing versions of GMT and its dependencies.

First, create a conda environment with only Python and ``pip`` installed
(we'll call it ``gmt-python`` but you can change it to whatever you want)::

     conda create --name gmt-python python=3.6 pip

Activate this environment by running::

    source activate gmt-python

From now on, all ``conda`` and ``pip`` commands will take place inside the
environment and won't affect your default installation.

Install the latest version of GMT 6::

    conda install gmt -c conda-forge/label/dev

And finally, install the rest of the dependencies::

    conda install numpy -c conda-forge

.. note::

    **Currently, this only works on Linux and OSX.**

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

This will allow you to use the GMT/Python library.
Test your installation by running the following inside a Python interpreter
(be sure to have your conda env activated)::

    import gmt
    gmt.test()


Finding the GMT shared library
------------------------------

You might have to set the ``LD_LIBRARY_PATH``
variable so that Python can find the GMT shared library ``libgmt``.

If you installed GMT using conda, place the following in your ``~/.bashrc``
file::

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/anaconda3/lib

You should change ``$HOME/anaconda3`` to wherever you installed Anaconda (this
is the default for Linux).
