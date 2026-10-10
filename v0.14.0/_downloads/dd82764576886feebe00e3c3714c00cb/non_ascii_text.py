# ruff: noqa: RUF001,RUF003
"""
Typesetting non-ASCII text
--------------------------

In addition to ASCII printable characters, sometimes you may also want to typeset
non-ASCII characters on the plot, such as Greek letters, mathematical symbols, or
special characters.

Due to the limitations of the underlying PostScript language, PyGMT doesn't support
all characters in the Unicode standard. Instead, PyGMT supports a limited set of
characters in the "Adobe Symbol", "Adobe ZapfDingbats", "Adobe ISOLatin1+", and
"ISO-8859-*x*" (*x* can be 1-11, 13-16) encodings. Refer to :doc:`/techref/encodings`
for the complete list of supported characters.

In PyGMT, the supported (ASCII and non-ASCII) characters can be directly used in the
``text`` parameter of the :meth:`pygmt.Figure.text` method for typesetting text strings.
They can also be used in the arguments of other plotting functions (e.g., in the
``frame`` parameter to set the labels or title).

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
    x=[0.2] * 5,
    y=[5, 4, 3, 2, 1],
    text=["ASCII:", "ISOLatin1+:", "Symbol:", "ZapfDingbats:", "Mixed:"],
    font="20p,Helvetica-Bold,red",
    justify="LM",
)
fig.text(
    x=[2] * 5,
    y=[5, 4, 3, 2, 1],
    text=[
        "ABCDE12345!#$:;<=>?",  # ASCII only
        "±°ÀÁÂÃÄÅÈÌÒÙàèìòù",  # Non-ASCII characters from Adobe ISOLatin1+
        "αβγδεζηθ⊗⊕∅⊃⊇⊄⊂⊆",  # Non-ASCII characters from Adobe Symbol
        "✈♥♦♣♠❛❜❝❞❨❩❪❫❬❭❮❯→↔",  # Non-ASCII characters from Adobe ZapfDingbats
        "ABCD αβγδ ①②③ ➊➋➌",  # Mix characters from ISOLatin1+, Symbol and ZapfDingbats
    ],
    font="18p,Helvetica",
    justify="LM",
)

fig.show()

# %%
# Here are some important tips when using non-ASCII characters:
#
# - **Similar-looking characters**: Be cautious when using characters that appear
#   visually similar but are distinct. For example, ``Ω`` (OHM SIGN) and ``Ω`` (GREEK
#   CAPITAL LETTER OMEGA) may look alike, but PyGMT only supports the latter. Using the
#   incorrect character can lead to unexpected results. To avoid this, it's recommended
#   to copy and paste characters from the :doc:`/techref/encodings` documentation.
# - **Mix characters from different encodings**: As shown in the example above, you can
#   mix characters from different encodings in the same text string. However, due to the
#   limitations of the underlying PostScript language, you cannot mix characters from
#   the "Adobe ISOLatin1+" and "ISO-8859-*x*" encodings in the same text string. For
#   example, you cannot mix characters from "Adobe ISOLatin1+" and "ISO-8859-2". If
#   you need to use characters from different encodings, you can use them in different
#   PyGMT function/method calls.
# - **Non-ASCII characters in text files**: Non-ASCII characters are not supported if
#   you have them in a text file and pass it to :meth:`pygmt.Figure.text`. In this case,
#   you may want to load the text file into :class:`pandas.DataFrame` and then pass it
#   to the ``text`` parameter.

# sphinx_gallery_thumbnail_number = 1
