.. title:: Home

.. raw:: html

    <div class="banner">
        <h1>PyGMT</h1>
        <h2>
            A Python interface for the
            <a href="http://gmt.soest.hawaii.edu/">Generic Mapping Tools</a>
        </h2>
    </div>

.. gmt-plot::
    :center:

    import pygmt

    # Load sample earthquake data in a pandas.DataFrame
    quakes = pygmt.datasets.load_usgs_quakes()

    # Load the builtin Earth relief grid as an xarray.DataArray.
    relief = pygmt.datasets.load_earth_relief(resolution="30m")

    # The Figure object controls all plotting functions
    fig = pygmt.Figure()
    # Setup a map with a global region, a Mollweide projection, and automatic ticks
    fig.basemap(region="g", projection="W200/8i", frame=True)
    # Plot the Earth relief grid in pseudo-color.
    fig.grdimage(relief, cmap="geo")
    # Plot earthquakes as circles. Size maps to magnitude and color to depth.
    fig.plot(x=quakes.longitude, y=quakes.latitude, sizes=0.01*2**quakes.mag,
             color=quakes.depth/quakes.depth.max(), cmap="viridis", style="cc")
    # Show a preview of the image (inline if in a Jupyter notebook).
    fig.show()

.. include:: ../README.rst
    :start-after: placeholder-for-doc-index

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Getting Started

    install.rst
    gallery/index.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: User Guide

    tutorials/plot-data-points.ipynb
    sphinxext.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Reference documentation

    api/index.rst
