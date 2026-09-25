---
file_format: mystnb
---

# Supported Fonts

PyGMT supports the 35 standard PostScript fonts. The table below lists them with their
font numbers and font names. When specifying fonts in PyGMT, you can either give the
font name or just the font number. For example, to use the font "Helvetica", you can use
either `"Helvetica"` or `"0"`. For the special fonts "Symbol" (**12**) and
"ZapfDingbats" (**34**), see the [](/techref/encodings.md) for the character set.
The image below the table shows a visual sample for each font.

```{code-cell}
---
tags: [remove-input]
---
from IPython.display import display, Markdown

fonts = [
    "Helvetica",
    "Helvetica-Bold",
    "Helvetica-Oblique",
    "Helvetica-BoldOblique",
    "Times-Roman",
    "Times-Bold",
    "Times-Italic",
    "Times-BoldItalic",
    "Courier",
    "Courier-Bold",
    "Courier-Oblique",
    "Courier-BoldOblique",
    "Symbol",
    "AvantGarde-Book",
    "AvantGarde-BookOblique",
    "AvantGarde-Demi",
    "AvantGarde-DemiOblique",
    "Bookman-Demi",
    "Bookman-DemiItalic",
    "Bookman-Light",
    "Bookman-LightItalic",
    "Helvetica-Narrow",
    "Helvetica-Narrow-Bold",
    "Helvetica-Narrow-Oblique",
    "Helvetica-Narrow-BoldOblique",
    "NewCenturySchlbk-Roman",
    "NewCenturySchlbk-Italic",
    "NewCenturySchlbk-Bold",
    "NewCenturySchlbk-BoldItalic",
    "Palatino-Roman",
    "Palatino-Italic",
    "Palatino-Bold",
    "Palatino-BoldItalic",
    "ZapfChancery-MediumItalic",
    "ZapfDingbats",
]

text = "| Font No. | Font Name | Font No. | Font Name |\n"
text += "|:---:|:---|:---:|:---|\n"
for i in range(17):
    j = i + 17
    text += f"| {i} | {fonts[i]} | {j} | {fonts[j]} |\n"
text += f"| | | 34 | {fonts[34]} |\n"

display(Markdown(text))
```

```{code-cell}
---
tags: [remove-input]
---
"""
Script to generate visual samples of the fonts.
"""
import pygmt

x1, x2, dx = 0, 7, 0.75

fig = pygmt.Figure()
# Draw the table
fig.basemap(region=[-0.5, 14, -1.5, 18], projection="X14c/-10c", frame=0)
fig.plot(x=[-0.5, 14], y=[-0.5, -0.5])
for x in (0.5, 6.5, 7.5):
    fig.plot(x=[x, x], y=[-1.5, 18])
# Table header
fig.text(
    x=[x1, x1 + dx, x2, x2 + dx],
    y=[-1] * 4,
    text=["#", "Font Name"] * 2,
    justify=["MC", "ML"] * 2,
    font="Helvetica-Bold",
)
# Fonts
for i, font in enumerate(fonts):
    x0 = x1 if i < 17 else x2
    y0 = i % 17
    font_no, font_name = i, font

    # Deal with special cases
    if font in ["Symbol", "ZapfDingbats"]:
        font_name = f"{font} @%0%({font})@%%"
    if font == "ZapfDingbats":
        font_no = "@%0%34@%%"
        y0 = 17

    fig.text(
        x=[x0, x0 + dx],
        y=[y0] * 2,
        text=[font_no, font_name],
        justify=["MC", "ML"],
        font=font,
    )
fig.show(width=600)
```
