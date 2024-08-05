# Supported Fonts

PyGMT supports the 35 standard PostScript fonts. The table below lists the 35 fonts with
font number and the font name.

| Font Number | Font Name                  | Font Number | Font Name                  |
|-------------|----------------------------|-------------|----------------------------|
| 0           | Helvetica                  | 17          | Bookman-Demi               |
| 1           | Helvetica-Bold             | 18          | Bookman-DemiItalic         |
| 2           | Helvetica-Oblique          | 19          | Bookman-Light              |
| 3           | Helvetica-BoldOblique      | 20          | Bookman-LightItalic        |
| 4           | Times-Roman                | 21          | Helvetica-Narrow           |
| 5           | Times-Bold                 | 22          | Helvetica-Narrow-Bold      |
| 6           | Times-Italic               | 23          | Helvetica-Narrow-Oblique   |
| 7           | Times-BoldItalic           | 24          | Helvetica-Narrow-BoldOblique |
| 8           | Courier                    | 25          | NewCenturySchlbk-Roman     |
| 9           | Courier-Bold               | 26          | NewCenturySchlbk-Italic    |
| 10          | Courier-Oblique            | 27          | NewCenturySchlbk-Bold      |
| 11          | Courier-BoldOblique        | 28          | NewCenturySchlbk-BoldItalic|
| 12          | Symbol                     | 29          | Palatino-Roman             |
| 13          | AvantGarde-Book            | 30          | Palatino-Italic            |
| 14          | AvantGarde-BookOblique     | 31          | Palatino-Bold              |
| 15          | AvantGarde-Demi            | 32          | Palatino-BoldItalic        |
| 16          | AvantGarde-DemiOblique     | 33          | ZapfChancery-MediumItalic  |
|             |                            | 34          | ZapfDingbats               |

The figure below shows a visual sample for each font.

![Standard PostScript Fonts](https://docs.generic-mapping-tools.org/dev/_images/GMT_App_G.png){.align-center width="80%"}

For the special fonts Symbol (12) and ZapfDingbats (34), see the {doc}`/techref/encodings`
for the character set.

When specifying fonts in GMT, you can either give the entire font name or just the font
number listed in this table. For example, to use the Helvetica font, you can use either
`Helvetica` or `0`.
