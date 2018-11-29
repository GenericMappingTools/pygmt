.. _sphinxext:

Sphinx Extension
================

We provide a `Sphinx <http://www.sphinx-doc.org/>`__ extension for including GMT/Python
figures in your documentation. The extension defines the ``gmt-plot`` directive that
will take execute the given code and insert the generated figure into the document.

For example, the following rst code:

.. code:: rst

    .. gmt-plot::

        import gmt
        fig = gmt.Figure()
        fig.basemap(region="g", projection="W0/10i", frame="afg")
        fig.show()


will be rendered into the following in the compiled HTML pages:

.. gmt-plot::

    import gmt
    fig = gmt.Figure()
    fig.basemap(region="g", projection="W0/10i", frame="afg")
    fig.show()

The *last statement* of the code-block should contain a call to :meth:`gmt.Figure.show`.
Anything printed to STDOUT will be captured and included between the figure and the
code. For example:

.. gmt-plot::

    print("The variables from the previous block are preserved.")
    fig.coast(land="gray")
    fig.show()


The HTML rich display features that work in Jupyter notebooks also work for the
extension:

.. gmt-plot::

    quakes = gmt.datasets.load_usgs_quakes()

    fig2 = gmt.Figure()
    fig2.plot(x=quakes.longitude, y=quakes.latitude, region=[-180, 180, -90, 90],
              projection="X10id", color="yellow", style="c0.2c", pen="black")
    fig2.show(method="globe")


Installing
----------

The extension comes with GMT/Python. All you have to do is enable it in your ``conf.py``
file:

.. code:: python

    extensions = [
        ...,
        "gmt.sphinxext.gmtplot",
    ]

However, you will need to have IPython installed for the extension to work.

Options
-------

The directive has the following options::

    .. gmt-plot::
        :width: size   # Set the width of the image (should contain a unit, like 400px)
        :center:       # If set, will center the output image
        :hide-code:    # If set, then hide the code and only show the plot
        :namespace:    # Specify a plotting namespace that is persistent within the page
