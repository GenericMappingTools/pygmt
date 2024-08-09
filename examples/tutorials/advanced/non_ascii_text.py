# ruff: noqa: RUF001,RUF003
"""
Typesetting non-ASCII text
--------------------------

In addtion to ASCII printable characters, sometimes you may also want to typeset
non-ASCII characters on the plot, such as Greek letters, mathematical symbols, or
special characters.

Due to the limitations of the underlying PostScript language, PyGMT doesn't support
all characters in the Unicode standard. Instead, PyGMT supports a limited set of
characters in the "Adobe ISOLatin1+", "Adobe Symbol", "Adobe ZapfDingbats" and
ISO-8859-*x* (*x* can be 1-11, 13-16) encodings. Refer to :doc:`/techref/encodings`
for the complete list of supported characters.

In PyGMT, the supported characters (ASCII and non-ASCII) can be directly used in the
``text`` parameters of the :meth:`pygmt.Figure.text` method. They can also be used in
the parameter arguments of other plotting functions (e.g., in the ``frame`` parameter to
set the labels or title).

In this example, we demonstrate how to typeset non-ASCII characters in PyGMT.
"""

# %%
import pygmt

fig = pygmt.Figure()
fig.basemap(
    region=[0, 5, 0, 6],
    projection="X14c/7c",
    frame=["xaf+lDistance (°)", "yaf+lValue (‰)", "WSen+tTitle: α² ± β²"],
)

fig.text(
    x=[0.2, 0.2, 0.2, 0.2, 0.2],
    y=[1, 2, 3, 4, 5],
    text=["Mixed:", "ZapfDingbats:", "Symbol:", "ISOLatin1+:", "ASCII:"],
    font="20p,Helvetica-Bold,red",
    justify="LM",
)
fig.text(
    x=[2, 2, 2, 2, 2],
    y=[1, 2, 3, 4, 5],
    text=[
        "ABCD αβγδ ①②③ ➊➋➌",
        "✈♥♦♣♠❛❜❝❞❨❩❪❫❬❭❮❯→↔",
        "αβγδεζηθ⊗⊕∅⊃⊇⊄⊂⊆",
        "±°ÀÁÂÃÄÅÈÌÒÙàèìòù",
        "ABCDE12345!#$:;<=>?",
    ],
    font="18p,Helvetica",
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
