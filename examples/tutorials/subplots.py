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
# The :meth:`pygmt.subplots` command is used to setup the layout, size, and
# other attributes of the figure. It divides the whole canvas into regular grid
# areas with n rows and m columns. Each grid area can contain an individual
# subplot. For example:

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
        position="MC", text=f"index: {index}, row: {i}, col: {j}", region=[0, 1, 0, 1]
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

###############################################################################
# Making your first subplot
# -------------------------
# Next, let's use what we learned above to make a 2 row by 2 column subplot
# figure. We'll also pick up on some new parameters to configure our subplot.
import pygmt

fig, axs = pygmt.subplots(
    nrows=2,
    ncols=2,
    figsize=("15c", "6c"),
    autolabel=True,
    margins=["0.3c", "0.1c"],
    title="My Subplot Heading",
)
fig.basemap(region=[0, 10, 0, 10], projection="X?", frame=["af", "WSne"], ax=axs[0, 0])
fig.basemap(region=[0, 20, 0, 10], projection="X?", frame=["af", "WSne"], ax=axs[0, 1])
fig.basemap(region=[0, 10, 0, 20], projection="X?", frame=["af", "WSne"], ax=axs[1, 0])
fig.basemap(region=[0, 20, 0, 20], projection="X?", frame=["af", "WSne"], ax=axs[1, 1])
fig.end_subplot()
fig.show()

###############################################################################
# In this example, we define a 2-row, 2-column (2x2) subplot layout using
# :meth:`pygmt.subplots`. The overall figure dimensions is set to be 15cm wide
# and 6cm high (``figsize=["15c", "6c"]``). In addition, we used some optional
# parameters to fine tune some details of the figure creation:
#
# - ``autolabel=True``: Each subplot is automatically labelled abcd
# - ``margins=["0.2c", "0.1c"]``: adjusts the space between adjacent subplots.
#   In this case, it is set as 0.2 cm in the X direction and 0.1 cm in the Y
#   direction.
# - ``title="My Subplot Heading"``: adds a title on top of the whole figure.
#
# Notice that each subplot was set to use a linear projection ``"X?"``.
# Usually, we need to specify the width and height of the map frame, but it is
# also possible to use a question mark ``"?"`` to let GMT decide automatically
# on what is the most appropriate width/height for the each subplot's map
# frame.
