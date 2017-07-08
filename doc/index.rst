GMT/Python
==========

**A Python interface for the Generic Mapping Tools**

Run GMT in your Python programs:

.. code-block:: python

    import gmt

    # Start a new figure.
    gmt.figure()
    # Creat a basemap with the Mercator projection
    # Use the command line arguments you know (like R)
    # or more Pythonic and descriptive aliases.
    gmt.psbasemap(region=[130, 150, 35, 50], projection='M6i',
                  frame=True, portrait=True)
    # Plot the quake data from the GMT tutorial
    gmt.psxy('@tut_quakes.ngdc', style='c0.4c', color='red',
             pen='faint', i='4,3')
    # Unlike the GMT command-line interface, no figure
    # file is generated unless explicitly asked
    gmt.psconvert(prefix='myfigure', fmt='g', crop=True)


.. image:: _static/front-page-example.png
    :width: 60%
    :alt: Example figure
    :align: center


See the :ref:`api` for a list of modules that are already available.


Disclaimer
----------

**This package in early stages of design and implementation.**

We welcome any feedback and ideas!
Code contributions are also very welcome.
Let us know by submitting
`issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__
or send us a message on `our Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.


.. toctree::
    :maxdepth: 2
    :hidden:

    install.rst
    first-steps.ipynb
    api.rst
    design.rst
    contribute.rst
    license.rst
