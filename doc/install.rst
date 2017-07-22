.. _install:

Installing
==========


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

Install the dependencies using ``conda``::

    conda install gmt numpy -c conda-forge/label/dev -c conda-forge

**Currently only works on Linux and OSX.**


Installing from source
----------------------

Use ``pip`` to install the latest source from Github::

    pip install https://github.com/GenericMappingTools/gmt-python/archive/master.zip

Alternatively, you can clone the git repository and install using ``pip``::

    git clone https://github.com/GenericMappingTools/gmt-python.git
    cd gmt-python
    pip install .


Finding the GMT shared library
------------------------------

You might have to set the ``LD_LIBRARY_PATH``
variable so that Python can find the GMT shared library ``libgmt``.

If you installed GMT using conda, place the following in your ``~/.bashrc``
file::

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/anaconda3/lib

You should change ``$HOME/anaconda3`` to wherever you installed Anaconda (this
is the default for Linux).
