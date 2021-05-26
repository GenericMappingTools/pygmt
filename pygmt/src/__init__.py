"""
Source code for PyGMT modules.
"""
# pylint: disable=import-outside-toplevel

from pygmt.src.basemap import basemap
from pygmt.src.blockm import blockmean, blockmedian
from pygmt.src.coast import coast
from pygmt.src.colorbar import colorbar
from pygmt.src.config import config
from pygmt.src.contour import contour
from pygmt.src.grd2cpt import grd2cpt
from pygmt.src.grdclip import grdclip
from pygmt.src.grdcontour import grdcontour
from pygmt.src.grdcut import grdcut
from pygmt.src.grdfill import grdfill
from pygmt.src.grdfilter import grdfilter
from pygmt.src.grdgradient import grdgradient
from pygmt.src.grdimage import grdimage
from pygmt.src.grdinfo import grdinfo
from pygmt.src.grdlandmask import grdlandmask
from pygmt.src.grdtrack import grdtrack
from pygmt.src.grdview import grdview
from pygmt.src.histogram import histogram
from pygmt.src.image import image
from pygmt.src.info import info
from pygmt.src.inset import inset
from pygmt.src.legend import legend
from pygmt.src.logo import logo
from pygmt.src.makecpt import makecpt
from pygmt.src.meca import meca
from pygmt.src.plot import plot
from pygmt.src.plot3d import plot3d
from pygmt.src.rose import rose
from pygmt.src.solar import solar
from pygmt.src.subplot import set_panel, subplot
from pygmt.src.surface import surface
from pygmt.src.text import text_ as text  # "text" is an argument within "text_"
from pygmt.src.velo import velo
from pygmt.src.which import which
from pygmt.src.wiggle import wiggle
from pygmt.src.x2sys_cross import x2sys_cross
from pygmt.src.x2sys_init import x2sys_init
