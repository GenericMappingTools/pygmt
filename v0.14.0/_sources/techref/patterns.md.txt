# Bit and hachure patterns

PyGMT supports a variety of bit and hachure patterns that can be used to fill polygons.

These patterns can be defined using the following syntax:

**P**|**p**_pattern_[**+b**_color_][**+f**_color_][**+r**_dpi_]

*pattern* can either be a number in the range 1-90 or the name of a 1-, 8-, or 24-bit
image raster file. The former will result in one of the 90 predefined 64x64 bit-patterns
provided by GMT (see the figure below). The latter allows the user to create customized,
repeating images using image raster files.

By specifying upper case **P** instead of **p** the image will be bit-reversed, i.e.,
white and black areas will be interchanged (only applies to 1-bit images or predefined
bit-image patterns). For these patterns and other 1-bit images one may specify
alternative **b**ackground and **f**oreground colors (by appending **+b**_color_ and/or
**+f**_color_) that will replace the default white and black pixels, respectively.
Excluding *color* from a fore- or background specification yields a transparent image
where only the back- or foreground pixels will be painted. The **+r**_dpi_ modifier sets
the resolution in dpi.

The image below shows the 90 predefined bit patterns that can be used in PyGMT.

![](https://docs.generic-mapping-tools.org/6.5/_images/GMT_App_E.png)
