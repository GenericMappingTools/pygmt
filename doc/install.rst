.. _install:

Installing
==========


Which Python?
-------------

You'll need **Python 3.5 or greater** to run GMT Python.

We recommend using the Anaconda_ Python distribution to ensure you have all
dependencies installed and the ``conda`` package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


From source
-----------

Use ``pip`` to install the latest source from Github::

    pip install https://github.com/GenericMappingTools/gmt-python/archive/master.zip

If you have git installed, you can clone the repository and install using
``pip``::

    git clone https://github.com/GenericMappingTools/gmt-python.git
    cd gmt-python
    pip install .


Installing GMT trunk
--------------------

You'll need the current *trunk* version of GMT (future 6.0 release).
One way to get it is from their Subversion repository.
See the `build instructions`_.

Alternatively, if you are on Linux and using the Anaconda_ Python distribution,
you can install a pre-compiled version as a conda package from `conda-forge`_.
First, install the required dependencies::

    conda install -c conda-forge fftw gdal ghostscript libnetcdf hdf5=1.8.18.* zlib blas curl pcre

Next, install the development version of GMT::

    conda install -c conda-forge/channel/dev gmt


Finding the library
-------------------

After you have GMT installed, you'll need to set the ``LD_LIBRARY_PATH``
variable so that ``gmt-python`` can find the shared library ``libgmt``.

If you installed GMT using conda, place the following in your ``~/.bashrc``
file::

    export LD_LIBRARY_PATH=$HOME/anaconda3/lib:$LD_LIBRARY_PATH

You should change ``$HOME/anaconda3`` to wherever you installed Anaconda (this
is the default for Linux).


.. _build instructions: http://gmt.soest.hawaii.edu/projects/gmt/wiki/BuildingGMT
.. _Anaconda: https://www.continuum.io/downloads
.. _conda-forge: https://conda-forge.github.io/
