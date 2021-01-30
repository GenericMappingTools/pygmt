"""
Subplots
========

When you're preparing a figure for a paper, there will often be times when
you'll need to put many individual plots into one large figure, and label them
'abcd'. These individual plots are called subplots.

There are two main ways to create subplots in GMT:

- Use :meth:`pygmt.Figure.shift_origin` to manually move each individual plot
  to the right position.
- Use :meth:`pygmt.Figure.subplot` to define the layout of the subplots.

The first method is easier to use and should handle simple cases involving a
couple of subplots. For more advanced subplot layouts however, we recommend the
use of :meth:`pygmt.Figure.subplot` which offers finer grained control, and
this is what the tutorial below will cover.
"""

###############################################################################
# Let's start by importing the PyGMT library and initializing a Figure

import pygmt

fig = pygmt.Figure()

###############################################################################
# Define subplot layout
# ---------------------
#
# The :meth:`pygmt.Figure.subplot` command is used to setup the layout, size,
# and other attributes of the figure. It divides the whole canvas into regular
# grid areas with n rows and m columns. Each grid area can contain an
# individual subplot. For example:

###############################################################################
# .. code-block:: default
#
#     with fig.subplot(
#        nrows=2, ncols=3, figsize=("15c", "6c"), frame="lrtb"
#     ) as axs:
#         ...

###############################################################################
# will define our figure to have a 2 row and 3 column grid layout.
# ``figsize=("15c", "6c")`` defines the overall size of the figure to be 15cm
# wide by 6cm high. Using ``frame="lrtb"`` allows us to customize the map frame
# for all subplots instead of setting them individually. The figure layout will
# look like the following:

with fig.subplot(nrows=2, ncols=3, figsize=("15c", "6c"), frame="lrtb") as axs:
    for index in axs.flatten():
        i = index // axs.shape[1]  # row
        j = index % axs.shape[1]  # column
        fig.sca(ax=axs[i, j])  # sets the current Axes
        fig.text(
            position="MC",
            text=f"index: {index}, row: {i}, col: {j}",
            region=[0, 1, 0, 1],
        )
fig.show()

###############################################################################
# The :meth:`pygmt.Figure.sca` command activates a specified subplot, and all
# subsequent plotting commands will take place in that subplot. This is similar
# to matplotlib's ``plt.sca`` method. In order to specify a subplot, you will
# need to provide the identifier for that subplot via the ``ax`` argument. This
# can be found in the ``axs`` variable referenced by the ``row`` and ``col``
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
# Making your first subplot
# -------------------------
# Next, let's use what we learned above to make a 2 row by 2 column subplot
# figure. We'll also pick up on some new parameters to configure our subplot.

fig = pygmt.Figure()
with fig.subplot(
    nrows=2,
    ncols=2,
    figsize=("15c", "6c"),
    autolabel=True,
    margins=["0.1c", "0.2c"],
    title='"My Subplot Heading"',
) as axs:
    fig.basemap(
        region=[0, 10, 0, 10], projection="X?", frame=["af", "WSne"], ax=axs[0, 0]
    )
    fig.basemap(
        region=[0, 20, 0, 10], projection="X?", frame=["af", "WSne"], ax=axs[0, 1]
    )
    fig.basemap(
        region=[0, 10, 0, 20], projection="X?", frame=["af", "WSne"], ax=axs[1, 0]
    )
    fig.basemap(
        region=[0, 20, 0, 20], projection="X?", frame=["af", "WSne"], ax=axs[1, 1]
    )
fig.show()

###############################################################################
# In this example, we define a 2-row, 2-column (2x2) subplot layout using
# :meth:`pygmt.Figure.subplot`. The overall figure dimensions is set to be 15cm
# wide and 6cm high (``figsize=["15c", "6c"]``). In addition, we used some
# optional parameters to fine tune some details of the figure creation:
#
# - ``autolabel=True``: Each subplot is automatically labelled abcd
# - ``margins=["0.1c", "0.2c"]``: adjusts the space between adjacent subplots.
#   In this case, it is set as 0.1 cm in the X direction and 0.2 cm in the Y
#   direction.
# - ``title="My Subplot Heading"``: adds a title on top of the whole figure.
#
# Notice that each subplot was set to use a linear projection ``"X?"``.
# Usually, we need to specify the width and height of the map frame, but it is
# also possible to use a question mark ``"?"`` to let GMT decide automatically
# on what is the most appropriate width/height for the each subplot's map
# frame.

###############################################################################
# .. tip::
#
#     In the above example, we used the following commands to activate the
#     four subplots explicitly one after another::
#
#         fig.basemap(..., ax=axs[0, 0])
#         fig.basemap(..., ax=axs[0, 1])
#         fig.basemap(..., ax=axs[1, 0])
#         fig.basemap(..., ax=axs[1, 1])
#
#     In fact, we can just use ``fig.basemap(..., ax=True)`` without specifying
#     any subplot index number, and GMT will automatically activate the next
#     subplot.

###############################################################################
# Shared X and Y axis labels
# --------------------------
# In the example above with the four subplots, the two subplots for each row
# have the same Y-axis range, and the two subplots for each column have the
# same X-axis range. You can use the **layout** option to set a common X and/or
# Y axis between subplots.

fig = pygmt.Figure()
with fig.subplot(
    nrows=2,
    ncols=2,
    figsize=("15c", "6c"),
    autolabel=True,
    margins=["0.3c", "0.2c"],
    title='"My Subplot Heading"',
    layout=["Rl", "Cb"],
    frame="WSrt",
) as axs:
    fig.basemap(region=[0, 10, 0, 10], projection="X?", ax=True)
    fig.basemap(region=[0, 20, 0, 10], projection="X?", ax=True)
    fig.basemap(region=[0, 10, 0, 20], projection="X?", ax=True)
    fig.basemap(region=[0, 20, 0, 20], projection="X?", ax=True)
fig.show()

###############################################################################
# **Rl** indicates that subplots within a **R**\ ow will share the y-axis, and
# only the **l**\ eft axis is displayed. **Cb** indicates that subplots in
# a column will share the x-axis, and only the **b**\ ottom axis is displayed.
#
# Of course, instead of using the **layout** option, you can also set a
# different **frame** for each subplot to control the axis properties
# individually for each subplot.

###############################################################################
# Advanced subplot layouts
# ------------------------
#
# Nested subplot are currently not supported. If you want to create more
# complex subplot layouts, some manual adjustments are needed.
#
# The following example draws three subplots in a 2-row, 2-column layout, with
# the first subplot occupying the first row.

fig = pygmt.Figure()
with fig.subplot(nrows=2, ncols=2, figsize=("15c", "6c"), autolabel=True):
    fig.basemap(
        region=[0, 10, 0, 10], projection="X15c/3c", frame=["af", "WSne"], ax=axs[0, 0]
    )
    fig.text(text="TEXT", x=5, y=5, projection="X15c/3c")
    fig.basemap(
        region=[0, 5, 0, 5], projection="X?", frame=["af", "WSne"], ax=axs[1, 0]
    )
    fig.basemap(
        region=[0, 5, 0, 5], projection="X?", frame=["af", "WSne"], ax=axs[1, 1]
    )
fig.show()

###############################################################################
#
# When drawing the three basemaps, the last two basemaps use
# ``projection="X?"``, so GMT will automatically determine the size of the
# subplot according to the size of the subplot area. In order for the first
# subplot to fill up the entire top row space, we use manually adjusted the
# subplot width to 15cm using ``projection="X15c/3c"``.

###############################################################################
# .. note::
#
#     There are bugs that have not been fixed in the above example.
#
#     In subplot mode, the size of each subgraph is controlled by the
#     ``figsize`` option of :meth:`pygmt.Figure.subplot`. Users can override
#     this and use``projection`` to specify the size of an individual subplot,
#     but this size will not be remembered. If the next command does not
#     specify``projection``, the default size of the subplot mode will be used,
#     and the resulting plot will be inccorect.
#
#     The current workaround is to use the same ``projection`` option in all
#     commands for the subplot. For example, we forced subplot (a) to have a
#     different size using ``projection="15c/3c``. The next command within the
#     subplot (e.g. ``text``) must also use ``projection="x15c/3c"``, otherwise
#     the placement will be wrong.

###############################################################################
# Since we skipped the second subplot, the auto label function will name the
# three subplots as a, c and d, which is not what we want, so we have to use
# ``fig.sca(autolabel=""(a)"`` to manually set the subplot label.
