"""
Making your first figure
========================

Welcome to PyGMT! Here we'll cover some of basic concepts, like creating simple
figures and naming conventions.
"""

###############################################################################
# Loading the library
# -------------------
#
# All modules and figure generation is accessible from the :mod:`pygmt` top
# level package:

import pygmt

###############################################################################
# Creating figures
# ----------------
#
# All figure generation in PyGMT is handled by the :class:`pygmt.Figure` class.
# Start a new figure by creating an instance of this class:

fig = pygmt.Figure()

###############################################################################
# Add elements to the figure using its methods. For example, let's use
# :meth:`pygmt.Figure.basemap` to start the creation of a map. We'll use the
# ``region`` parameter to provide the longitude and latitude bounds, the
# ``projection`` parameter to set the projection to Mercator (**M**) and the
# map width to 15 cm, and the ``frame`` parameter to generate a frame with
# automatic tick and annotation spacings.

fig.basemap(region=[-90, -70, 0, 20], projection="M15c", frame=True)

###############################################################################
# Now we can add coastlines using :meth:`pygmt.Figure.coast` to this map using
# the default resolution, line width, and color:

fig.coast(shorelines=True)

###############################################################################
# To see the figure, call :meth:`pygmt.Figure.show`:

fig.show()

###############################################################################
# You can also set the map region, projection, and frame type directly in other
# methods without calling :meth:`gmt.Figure.basemap`:

fig = pygmt.Figure()
fig.coast(shorelines=True, region=[-90, -70, 0, 20], projection="M15c", frame=True)
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
