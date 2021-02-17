import textwrap
import difflib
import pygmt


gmt_doc = r"""
    Select painting or dumping country polygons from the Digital Chart of the World.
    This is another dataset independent of GSHHG and hence the **-A** and **-D** options do not apply.
    Append one or more comma-separated countries using the
    `2-character ISO 3166-1 alpha-2 convention <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_.
    To select a state of a country
    (if available), append .state, e.g, US.TX for Texas.  To specify a
    whole continent, prepend = to any of the continent codes AF (Africa),
    AN (Antarctica), AS (Asia), EU (Europe), OC (Oceania),
    NA (North America), or SA (South America).  Append **+l** to
    just list the countries and their codes [no data extraction or plotting takes place].
    Use **+L** to see states/territories for Argentina, Australia, Brazil, Canada, China, India, Russia and the US.
    Finally, you can append **+l**\|\ **+L** to **-E**\ =\ *continent* to only list countries in that continent;
    repeat if more than one continent is requested.
    Append **+p**\ *pen* to draw polygon outlines [no outline] and
    **+g**\ *fill* to fill them [no fill].  One of **+p**\|\ **g** must be
    specified unless **-M** is in effect, in which case only one **-E** option can be given;
    append **+z** to place the country code in the segment headers via **-Z**\ *code* settings.
    Otherwise, you may repeat **-E** to give different groups of items their own pen/fill settings.
    If neither **-J** nor **-M** are set then we just print the **-R**\ *wesn* string.
"""

# function to document
function = pygmt.Figure.coast

# translation
gmt_doc = gmt_doc.lstrip("\n")
pygmt_doc = gmt_doc
for key, value in function.aliases.items():
    pygmt_doc = pygmt_doc.replace(f"**-{key}**", f"**{value}**")


# output
diff = difflib.unified_diff(gmt_doc.splitlines(), pygmt_doc.splitlines(), lineterm="")
print("Diff view:\n")
print("\n".join(diff))
print("\n")

print("Raw GMT docstring:\n")
print(gmt_doc)

print("Translate PyGMT docstring:\n")
pygmt_doc = textwrap.indent(
    textwrap.fill(textwrap.dedent(pygmt_doc), width=72), " " * 8
)
print(pygmt_doc)
