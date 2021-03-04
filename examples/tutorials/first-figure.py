"""
Making your first figure
========================

Welcome to PyGMT! Here we'll cover some of basic concepts, like creating simple figures
and naming conventions.

.. note::

    This tutorial assumes the use of a Python notebook, such as `IPython <https://ipython.org/>`__
    or `JupyterLab <https://jupyter.org/>`__.
    To see the figures while using a Python script instead, use
    ``fig.show(method="external")`` to display the figure in the default PDF viewer.

    To save the figure, use ``fig.savefig("figname.pdf")`` where ``"figname.pdf"``
    is the desired name and file extension for the saved figure.
"""

########################################################################################
# Loading the library
# -------------------
#
# All modules and figure generation is accessible from the :mod:`pygmt` top level
# package:

import pygmt

########################################################################################
# Creating figures
# ----------------
#
# All figure generation in PyGMT is handled by the :class:`pygmt.Figure` class.
# Start a new figure by creating an instance of this class:

fig = pygmt.Figure()

########################################################################################
# Add elements to the figure using its methods. For example, let's use
# :meth:`pygmt.Figure.basemap` to start a map for a region indicated by a given
# longitude and latitude bound, set the projection to Mercator (``M``), the
# map width to 8 centimeters, and frame type to be generated automatically:

fig.basemap(region=[-90, -70, 0, 20], projection="M8c", frame=True)

########################################################################################
# Now we can add coastlines using :meth:`pygmt.Figure.coast` to this map using the
# default resolution, line width, and color:

fig.coast(shorelines=True)

########################################################################################
# To see the figure, call :meth:`pygmt.Figure.show`:

fig.show()

########################################################################################
# You can also set the map region, projection, and frame type directly in other methods
# without calling :meth:`gmt.Figure.basemap`:

fig = pygmt.Figure()
fig.coast(shorelines=True, region=[-90, -70, 0, 20], projection="M8c", frame=True)
fig.show()

########################################################################################
# Saving figures
# --------------
#
# Use the method :meth:`pygmt.Figure.savefig` to save your figure to a file. The figure
# format is inferred from the extension.
#
# .. code:: python
#
#     fig.savefig("central-america-shorelines.png")
#
# Note for experienced GMT users
# ------------------------------
#
# You’ll probably have noticed several things that are different from classic
# command-line GMT. Many of these changes reflect the new GMT modern execution
# mode that are part of GMT 6.
#
# 1. The name of method is ``coast`` instead of ``pscoast``. As a general rule, all
#    ``ps*`` modules had their ``ps`` prefix removed. The exceptions are:
#    ``psxy`` which is now ``plot``, ``psxyz`` which is now ``plot3d``, and ``psscale``
#    which is now ``colorbar``.
#
# 2. More details can be found at https://docs.generic-mapping-tools.org/latest/cookbook/introduction.html?highlight=modern#modern-and-classic-mode
#
#  A few are PyGMT exclusive (like the ``savefig`` method).
#
# 1. The parameters don't use the GMT 1-letter syntax (**R**, **J**, **B**, etc). We use longer
#    aliases for these parameters and have some Python exclusive names. The mapping
#    between the GMT parameters and their Python counterparts should be straight
#    forward.
# 2. Parameters like ``region`` can take lists as well as strings like ``1/2/3/4``.
# 3. If a GMT parameter has no options (like ``-B`` instead of ``-Baf``), use a ``True``
#    in Python. An empty string would also be acceptable. For repeated parameters, such
#    as ``-B+Loleron -Bxaf -By+lm``, provide a list: ``frame=["+Loleron", "xaf", "y+lm"]``.
# 4. There is no output redirecting to a PostScript file. The figure is generated in the
#    background and will only be shown or saved when you ask for it.
