# Text Formatting

The table below shows how text added to a plot, such as text strings added via `Figure.text`, plot title, labels of Cartesian axes and colorbars, and legend entries.
Changing
the font as well as its color and size in this way allows to change those only for
specific characters of a longer text. The supported fonts are listed at
[](/techref/fonts.md).

| Symbol | Behavior |
| --- | --- |
| @%*font*%*TEXT*@%%  | Change the *font* of *TEXT* |
| @;*color*;*TEXT*@;; | Change the font *color* of *TEXT* |
| @:*size*:*TEXT*@::  | Change the font *size* of *TEXT* |
| @-*TEXT*@-          | Toggle subscripts on/off |
| @+*TEXT*@+          | Toggle superscript on/off |
| @#*TEXT*@#          | Toggle small caps on/off |
| @\_*TEXT*@\_        | Toggle underline on/off |
| @!*CHAR1CHAR2*      | Print two characters on top of each other (composite characters, e.g., overstrike) |
| @\~*TEXT*@\~        | Toggle Greek letters on/off |
| @@                  | Print the @ sign |
| @.                  | Print the ° (degree) symbol |
| @s                  | Print letter ß |
| @i                  | Print letter í |
| @a or @A            | Print letter å or Å |
| @c or @C            | Print letter ç or Ç |
| @e or @E            | Print letter æ or Æ |
| @n or @N            | Print letter ñ or Ñ |
| @o or @O            | Print letter ø or Ø |
| @u or @U            | Print letter ü or Ü |
