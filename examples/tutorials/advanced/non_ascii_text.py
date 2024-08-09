"""
Typesetting non-ASCII text
--------------------------

In addtion to ASCII characters, you may want to typeset non-ASCII characters on the plot,
such as, Greek letters, mathematical symbols, or special characters. In PyGMT, you can
directly use non-ASCII characters in the text strings.  Due to the
limitations of the underlying PostScript language, PyGMT only supports a limited set of
non-ASCII characters.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.basemap(
    region=[0, 5, 0, 5],
    projection="X15c/5c",
    frame=["xaf", "yaf", "WSen+tNon-ASCII Text"],
)
fig.text(
    x=[0, 0, 0, 0],
    y=[1, 2, 3, 4],
    text=[
        "ASCII: ABCDE12345!#$",
        "Non-ASCII in ISOLatin1+: ±°ÀÈÌÒÙ",
        "Greek letters: αβγδεζηθ",
        "ZapfDingbats: ✈♥♦♣♠",
    ],
    font="20p,Helvetica-Bold",
    justify="LM",
)
fig.show()

# Since many characters may have similar typography, it would be
# best to visit the :doc:`/techref/encodings` to see which characters are supported, and
# copy and paste the characters directly into your script.

# sphinx_gallery_thumbnail_number = 2
