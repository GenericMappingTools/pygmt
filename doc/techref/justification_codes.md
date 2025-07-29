Justification codes
===================

To adjust the position of plot embellishments, such as scalbars, directional roses,
colorbars, legends, and images, user can adjust the *reference* and *anchor* points.

Pass to `position` parameter and if already implemented `justify`.

Reference point inside / outside of the map bounding box **j** (lower-case) / **J**
(upper-case), respectively.

Anchor point **+j**.

For both, specify a two-character (order independent) code. Choose from

- Vertical: **T**\(op), **M**\(iddle), **B**\(ottom)
- Horizontal: **L**\(eft), **C**\(entre), **R**\(ight)

Besides **j** / **J**, the reference point can be set based on

- **g**: Map coordinates as *longitude*/*latitude*
- **n**: Normalized bounding box coordinates as *nx*/*ny*
- **x**: Plot coordinates as *x*/*y*
