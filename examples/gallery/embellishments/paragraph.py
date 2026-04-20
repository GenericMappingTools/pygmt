"""
Paragraph
=========

To plot longer text as one or several paragraphs the `pygmt.Figure.paragraph`
method can be used. The ``parwidth`` and ``linespacing`` parameters allow to set
the line length and spacing of the paragraph, respectively.` Two paragraphs are
automatically separated by a blank line.

For details on text formatting see the gallery example
:doc:`Text formatting </gallery/embellishments/text_formatting>`.
"""

import pygmt

fig = pygmt.Figure()
fig.basemap(region=[-5, 5, -5, 5], projection="X10c/10c", frame=True)

fig.paragraph(
    x=0,
    y=0,
    text=[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    ],
    parwidth="4.5c",
    linespacing="12p",
    font="10p,Helvetica-Bold,steelblue",
    angle=45,
    justify="MC",
    alignment="center",
    fill="lightgray",  # font color ignored
    pen="1p,gray10",  # font color ignored
)

fig.show()
