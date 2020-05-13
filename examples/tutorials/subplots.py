"""
Subplots
========

When you're preparing a figure for a paper, there will often be times when
you'll need to put many individual plots into one large figure, and label them
'abcd'. These individual plots are called subplots.

There are two main ways to create subplots in GMT:

- Use :meth:`pygmt.Figure.shift_origin` to manually move each individual plot
  to the right position.
- Use :meth:`pygmt.subplots` to define the layout of the subplots.

The first method is easier to use and should handle simple cases involving a
couple of subplots. For more advanced subplot layouts however, we recommend the
use of :meth:`pygmt.subplots` which offers finer grained control, and this is
what the tutorial below will cover.
"""

###############################################################################
# Let's start by importing the PyGMT library

import pygmt

###############################################################################
# Define subplot layout
# ---------------------
#
# The ``pygmt.subplots`` command is used to setup the layout, size, and other
# attributes of the figure. It divides the whole canvas into regular grid areas
# with n rows and m columns. Each grid area can contain an individual subplot.
# For example:

fig, axs = pygmt.subplots(nrows=2, ncols=3, figsize=("15c", "6c"), frame="lrtb")

###############################################################################
# will define our figure to have a 2 row and 3 column grid layout.
# ``figsize=("15c", "6c")`` defines the overall size of the figure to be 15cm
# wide by 6cm high. Using ``frame="lrtb"`` allows us to customize the map frame
# for all subplots instead of setting them individually. The figure layout will
# look like the following:

for index in axs.flatten():
    i = index // axs.shape[1]  # row
    j = index % axs.shape[1]  # column
    fig.sca(ax=axs[i, j])  # sets the current Axes
    fig.text(
        x=0.5, y=0.5, text=f"index: {index}, row: {i}, col: {j}", region=[0, 1, 0, 1]
    )
fig.end_subplot()
fig.show()

###############################################################################
# The ``fig.sca`` command activates a specified subplot, and all subsequent
# plotting commands will take place in that subplot. This is similar to
# matplotlib's ``plt.sca`` method. In order to specify a subplot, you will need
# to provide the identifier for that subplot via the ``ax`` argument. This can
# be found in the ``axs`` variable referenced by the ``row`` and ``col``
# number.

###############################################################################
# .. note::
#
#     The row and column numbering starts from 0. So for a subplot layout with
#     N rows and M columns, row numbers will go from 0 to N-1, and column
#     numbers will go from 0 to M-1.

###############################################################################
# For example, to activate the subplot on the top right corner (index: 2) at
# ``row=0`` and ``col=2``, so that all subsequent plotting commands happen
# there, you can use the following command:

###############################################################################
# .. code-block:: default
#
#     fig.sca(ax=axs[0, 2])

###############################################################################
# Finally, remember to use ``fig.end_subplot()`` to exit the subplot mode.

###############################################################################
# .. code-block:: default
#
#     fig.end_subplot()
