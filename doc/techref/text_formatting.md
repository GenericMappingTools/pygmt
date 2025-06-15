# GMT Text Formatting

The table below shows how text added via :meth:`Figure.text` as well as labels of colorbars
and Cartesian axis can be formatted.

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
