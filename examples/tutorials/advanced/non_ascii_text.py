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

# Here are some important tips when using non-ASCII characters:
#
# - Some characters may look similar but are actually different. For example,
#   ``Ω`` is simlar to ``Ω``, but the former one is "OHM SIGN" and the later one is
#   "GREEK CAPITAL LETTER OMEGA". PyGMT only supports the later one. Thus, if you
#   incorrectly type the former one then you'll get a suprising result. So, your best
#   bet is to visit the :doc:`/techref/encodings` to see which characters are supported,
#   and copy and paste the characters directly.
# - The default character encoding is "ISOLatin1+" in PyGMT. You can mix any characters
#   in the "Adobe ISOLatin1+", "Adobe Symbol" and "Adobe ZapfDingbats" encodings.
# - Non-ASCII characters is not supported if you have them in a text file and pass it
#   to ``Figure.text``. In this case, you may want to load the text file into
#   ``pandas.DataFrame`` and then pass it to the ``text`` parameter.

# sphinx_gallery_thumbnail_number = 1
