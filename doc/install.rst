.. _install:

Installing
==========

.. note::

   🚨 **This package is in early stages of design and implementation.** 🚨

    We welcome any feedback and ideas!
    Let us know by submitting
    `issues on Github <https://github.com/GenericMappingTools/pygmt/issues>`__
    or send us a message on our
    `Gitter chatroom <https://gitter.im/GenericMappingTools/pygmt>`__.


Which Python?
-------------

You'll need **Python 3.6 or greater** to run PyGMT.

We recommend using the `Anaconda <http://continuum.io/downloads#all>`__ Python
distribution to ensure you have all dependencies installed and the ``conda``
package manager available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Which GMT?
----------

You'll need the latest development version available from
`the GitHub repository <https://github.com/GenericMappingTools/gmt>`__.
PyGMT is based on GMT 6, **which has not yet been officially released**.

We need the very latest GMT since there are many changes being made to GMT itself in
response to the development of PyGMT, mainly the new
`modern execution mode <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.


Dependencies
------------

PyGMT requires the following libraries:

* `numpy <http://www.numpy.org/>`__
* `pandas <https://pandas.pydata.org/>`__
* `xarray <http://xarray.pydata.org/>`__
* `packaging <https://pypi.org/project/packaging/>`__

The following are optional (but recommended) dependencies:

* `IPython <https://ipython.org/>`__: For embedding the figures in Jupyter notebooks.


Installing GMT
--------------

Unfortunately, you'll have to build GMT from source in order to get PyGMT working.
Please follow the instructions at http://gmt.soest.hawaii.edu/projects/gmt/wiki/BuildingGMT

.. note::

   We used to maintain conda packages for the latest GMT. That caused many problems and
   was very difficult to maintain updated. We have opted to not do that anymore so that
   we can develop more quickly. Once GMT 6 is officially released, we'll have conda
   packages available again. Please bear with us.


Installing PyGMT
---------------------

Now that you have GMT installed and your conda environment activated,
use ``pip`` to install the latest source of PyGMT from Github::

    pip install https://github.com/GenericMappingTools/pygmt/archive/master.zip

Alternatively, you can clone the git repository and install using ``pip``::

    git clone https://github.com/GenericMappingTools/pygmt.git
    cd pygmt
    pip install .

This will allow you to use the ``gmt`` library from Python.


Testing your install
--------------------

PyGMT ships with a full test suite.
You can run our tests after you install it but you will need a few extra dependencies as
well (be sure to have your conda env activated)::

    conda install pytest pytest-mpl sphinx jinja2 docutils ipython

Test your installation by running the following inside a Python interpreter::

    import gmt
    gmt.test()


Finding the GMT shared library
------------------------------

Sometimes, PyGMT will be unable to find the correct version of the GMT shared
library.
This can happen if you have multiple versions of GMT installed.

You can tell PyGMT exactly where to look for ``libgmt`` by setting the
``GMT_LIBRARY_PATH`` environment variable.
This should be set to the directory where ``libgmt.so`` (or ``.dylib``) is found.
**Only use this as a last resort**.
Setting the path in this way means that PyGMT will not be able to easily find the
correct ``libgmt`` when you're changing conda environments.

If you installed GMT using conda and the instructions above, place the following in your
``~/.bashrc`` file::

    export GMT_LIBRARY_PATH=$HOME/anaconda3/envs/pygmt/lib

You should change ``$HOME/anaconda3`` to wherever you installed Anaconda (this is the
default for Linux).
