"""
1. Making your first figure
===========================

This tutorial page covers the basics of creating a figure. It will only use
the ``coast`` module for plotting. Later examples will address other PyGMT
modules.
"""

###############################################################################
# Setting up the development environment
# --------------------------------------
#
# PyGMT can be used in both a Python script and a notebook environment, such
# as Jupyter. The tutorial's recommended method is to use a notebook, and the
# code will be for a notebook environment. If you use a Python script instead,
# there will be a difference in how the figure is shown that is explained in
# the first example.


###############################################################################
# Loading the library
# -------------------
#
# The first step is to import ``pygmt``. All modules and figure generation is
# accessible from the :mod:`pygmt` top level package.

import pygmt

###############################################################################
# Creating a figure
# -----------------
#
# All figure generation in PyGMT is handled by the :class:`pygmt.Figure` class.
# Start a new figure by creating an instance of this class:

fig = pygmt.Figure()

###############################################################################
# To add to a plot object (``fig`` in this example), the PyGMT module is used
# as a method on the class. This example will use the module ``coast``, which
# can be used to create a map without any other modules or external data. The
# ``coast`` module plots the coastlines, borders, and bodies of water using a
# database that is included in GMT.
#
# First, a region for the figure must be selected. This example will plot some
# of the coast of Maine in the northeastern US. A Python list can be passed to
# the ``region`` argument with the minimum and maximum X-values (longitude)
# and the minimum and maximum Y-values (latitude). For this example, the
# minimum (bottom left) coordinates are N43.75 W69 and the maximum (top right)
# coordinates are N44.75 W68. Negative values can be passed for latitudes in
# the southern hemisphere or longitudes in the western hemisphere.
#
# In addition to the region, a value needs to be passed to ``coast`` to tell
# it what to plot. In this example, ``coast`` will be told to plot the
# shorelines by passing the Boolean value ``True`` to the ``shorelines``
# parameter.

fig.coast(region=[-69, -68, 43.75, 44.75], shorelines=True)

###############################################################################
# To see the figure, call :meth:`pygmt.Figure.show`. If you are using a Python
# script instead of a notebook, use ``fig.show(method="external)`` to display
# the figure.

fig.show()

###############################################################################
# Color the land and water
# ------------------------
#
# This figure plots all of the coastlines in the given region, but it does not
# indicate where the land and water are. Color values can be passed to ``land``
# and ``water`` to set the colors on the figure.
#
# When plotting colors in PyGMT, there are multiple
# :gmt-docs:`color codes <gmtcolors.html>`, that can be used. This includes
# standard GMT color names (like ``skyblue``), R/G/B levels (like ``0/0/255``),
# a hex value (like ``#333333``), and a graylevel (like ``50``). For this
# example, GMT color names are used.

fig = pygmt.Figure()
fig.coast(
    region=[-69, -68, 43.75, 44.75],
    shorelines=True,
    land="lightgreen",
    water="lightblue",
)
fig.show()

###############################################################################
# Set the projection
# ------------------
#
# This figure now has its colors set, but there is not projection or size is
# not set for the map. Both of these values are set using the ``projection``
# parameter.
#
# The appropriate projection varies for the type of map. The available
# projections are explained in the "Projections" gallery. For this example,
# the Mercator projection is set using "M". The width of the figure will be
# 15 centimeters, as set by "15c"

fig = pygmt.Figure()
fig.coast(
    region=[-69, -68, 43.75, 44.75],
    shorelines=True,
    land="lightgreen",
    water="lightblue",
    projection="M15c",
)
fig.show()

###############################################################################
# Saving figures
# --------------
#
# Use the method :meth:`pygmt.Figure.savefig` to save your figure to a file.
# The figure format is inferred from the extension.
#
# .. code:: python
#
#     fig.savefig("central-america-shorelines.png")
#
# Note for experienced GMT users
# ------------------------------
#
# You have probably noticed several things that are different from classic
# command-line GMT. Many of these changes reflect the new GMT modern execution
# mode that is part of GMT 6.
#
# 1. As a general rule, the ``ps`` prefix has been removed from all ``ps*``
#    modules (PyGMT methods). For example, the name of the GMT 5 module
#    ``pscoast`` is ``coast`` in GMT 6 and PyGMT. The exceptions are: ``psxy``
#    which is now ``plot``, ``psxyz`` which is now ``plot3d``, and ``psscale``
#    which is now ``colorbar``.
#
# 2. More details can be found in the :gmt-docs:`GMT cookbook introduction to
#    modern mode </cookbook/introduction.html#modern-and-classic-mode>`.
#
# A few are PyGMT exclusive (like the ``savefig`` method).
#
# 1. The PyGMT parameters (called options or arguments in GMT) don't use the
#    GMT 1-letter syntax (**R**, **J**, **B**, etc). We use longer aliases for
#    these parameters and have some Python exclusive names. The mapping between
#    the GMT parameters and their PyGMT aliases should be straightforward.
#    For some modules, these aliases are still being developed.
# 2. Parameters like ``region`` can take :class:`lists <list>` as well as
#    strings like ``1/2/3/4``.
# 3. If a GMT option has no arguments (like ``-B`` instead of ``-Baf``), use a
#    ``True`` in Python. An empty string would also be acceptable. For repeated
#    parameters, such as ``-B+Loleron -Bxaf -By+lm``, provide a
#    :class:`list`: ``frame=["+Loleron", "xaf", "y+lm"]``.
# 4. There is no output redirecting to a PostScript file. The figure is
#    generated in the background and will only be shown or saved when you ask
#    for it.
