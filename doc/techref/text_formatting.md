# Text Formatting

The table below shows how text added to a plot as well as the title of the plot and
labels of colorbars, Cartesian axes, and legend entries can be formatted. Changing
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
| @.                  | Print the degree symbol |
