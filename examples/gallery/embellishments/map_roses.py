r"""
Directional map roses
=========

The ``rose`` parameter of the :meth:`pygmt.Figure.basemap` and
:meth:`pygmt.Figure.coast` methods is used to add a directional map 
rose to a map. This example shows how such a map rose can be customized:

 - position: **g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**. Set the position
   of the reference point. Choose from

   - **g**: Give map coordinates as *longitude*\/\ *latitude*.
   - **j**\|\ **J**: Specify a two-character (order independent) code.
     Choose from vertical **T**\(op), **M**\(iddle), or **B**\(ottom) and
     horizontal **L**\(eft), **C**\(entre), or **R**\(ight). Lower /
     uppercase **j** / **J** mean inside / outside of the map bounding
     box.
   - **n**: Give normalized bounding box coordinates as *nx*\/\ *ny*.
   - **x**: Give plot coordinates as *x*\/\ *y*.

- width: **+w**. Set the width of the rose in plot coordinates (append
  **i** (inch), **cm** (centimeters), or **p** (points).

- fanciness: **+f**\[level]. Get a "fancy" rose, and optionally specify the
  level of fanciness. Level 1 draws the two principal E-W, N-S orientations,
  2 adds the two intermediate NW-SE and NE-SW orientations, while 3 adds
  the four minor orientations WNW-ESE, NNW-SSE, NNE-SSW, and ENE-WSW
  [Default is 1].

- justify: **+j**. Set the anchor point. Specify a two-character (order
  independent) code. Choose from vertical **T**\(op), **M**\(iddle), or
  **B**\(ottom) and horizontal **L**\(eft), **C**\(entre), or **R**\(ight).

- label: **+l**\[w,e,s,n]. Label the cardinal points W,E,S,N. Optionally,
  append your own four comma-separated strings to override the default.
  Skip a specific label by leaving it blank.

- offset: **+o**\ *offset* or **+o**\ *xoffset*/\ *yoffset*. Give either a
  common shift or individual shifts in x- (longitude) and y- (latitude)
  directions.

Colors of the map roses can be adjusted using :gmt-term:`MAP_DEFAULT_PEN`
and :gmt-term:`MAP_TICK_PEN_PRIMARY` via :func:`pygmt.config`. Customizing
label font and color can be done via :gmt-term:`FONT_TITLE`.
"""
import pygmt

fig = pygmt.Figure()

region = [-5,5,-5,5]
projection = "M?"

with fig.subplot(
    nrows=2, ncols=4, figsize=("20c", "10c"), sharex = True, sharey = True):

    # Plain rose of 2.5 cm width showing arrow towards north, a cross
    # indicating the cardinal directions, and corresponding label
    with fig.set_panel(panel=0):
        fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+jCM+l",
           frame = True)

    # Fancy, 2.5 cm wide rose of level 1 and labels indicating the different
    # directions
    with fig.set_panel(panel=1):

          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f1+jCM+l",
           frame = True)

    # Fancy, 2.5 cm wide rose of level 2 abels indicating the different
    # directions
    with fig.set_panel(panel=2):

          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f2+l+jCM",
           frame = True)
        
    # Fancy, 2.5 cm wide rose of level 3 abels indicating the different
    # directions
    with fig.set_panel(panel=3):

          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f3+l+jCM",
           frame = True)


    # Plain rose of 2.5 cm width showing arrow towards north, a cross
    # indicating the cardinal directions, and corresponding label.
    # Colors of the rose and labels are defined via
    # MAP_TICK_PEN_PRIMARY and FONT_TITLE, respectively
    with fig.set_panel(panel=4):

        with pygmt.config(MAP_TICK_PEN_PRIMARY="purple",
                          FONT_TITLE="8p,darkmagenta"):

        
            fig.basemap(region = region,
               projection = projection,
               rose = "g0/0+w2.5c+jCM+l",
               frame = True)

    # Fancy, 2.5 cm wide rose of level 1 with only one label indicating the North
    # direction. Colors of the rose and labels are defined via
    # MAP_DEFAULT_PEN, MAP_TICK_PEN_PRIMARY and FONT_TITLE, respectively.
    with fig.set_panel(panel=5):

        with pygmt.config(MAP_DEFAULT_PEN="default,pink",
                          MAP_TICK_PEN_PRIMARY="thick,red3",
                          FONT_TITLE="8p,Bookman-Light,red3"):
        
          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f1+jCM+l,,,N",
           frame = True)

    # Fancy, 2.5 cm wide rose of level 2 with two labels indicating the West and
    # East directions. Colors of the rose and labels are defined via
    # MAP_DEFAULT_PEN, MAP_TICK_PEN_PRIMARY and FONT_TITLE, respectively
    with fig.set_panel(panel=6):

        with pygmt.config(MAP_DEFAULT_PEN="default,lightorange",
                          MAP_TICK_PEN_PRIMARY="thick,darkorange",
                          FONT_TITLE="8p,Bookman-Light,darkorange"):
        
          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f2+jCM+lW,E,,",
           frame = True)

    # Fancy, 2.5 cm wide rose of level 3 with two labels indicating the North and
    # South directions. Colors of the rose and labels are defined via
    # MAP_DEFAULT_PEN, MAP_TICK_PEN_PRIMARY and FONT_TITLE, respectively
    with fig.set_panel(panel=7):

        with pygmt.config(MAP_DEFAULT_PEN="default,Dodgerblue4",
                          MAP_TICK_PEN_PRIMARY="thick,Dodgerblue",   
                          FONT_TITLE="8p,AvantGarde-Demi,Dodgerblue4"):

          fig.basemap(region = region,
           projection = projection,
           rose = "g0/0+w2.5c+f3+l,,South,North+jCM",
           frame = True)

fig.show()
