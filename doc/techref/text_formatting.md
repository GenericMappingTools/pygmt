# GMT Text Formatting

The table below shows how text add to a plot as well as labels of colorbars and
Cartesian axes can be formatted. Changing the font as well as its color and size
in this way allows to change those only for specific words of a longer text. The
supported fonts are listed at [](/techref/fonts.md). For Greek letters, is there
any official list for the assignment ??? .

| Symbol | Behavior |
| --- | --- |
| @%*font*%*text*@%%  | Change the font |
| @;*color*;*text*@;; | Change the font color |
| @:*size*:*text*@::  | Change the font size |
| @-*text*@-          | Toggle subscripts on/off |
| @+*text*@+          | Toggle superscript on/off |
| @#*text*@#          | Toggle small caps on/off |
| @_*text*@_          | Toggle underline on/off |
| @!*char1char2*      | Print two characters on top of each other (composite characters, e.g., overstrike) |
| @\~*text*@\~        | Toggle Greek letters on/off |
| @@                  | Print the @ sign |
| @.                  | Print the degree symbol |
