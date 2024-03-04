"""
Source code for PyGMT methods.
"""

from pygmt.src.basemap import basemap
from pygmt.src.binstats import binstats
from pygmt.src.blockm import blockmean, blockmedian, blockmode
from pygmt.src.coast import coast
from pygmt.src.colorbar import colorbar
from pygmt.src.config import config
from pygmt.src.contour import contour
from pygmt.src.dimfilter import dimfilter
from pygmt.src.filter1d import filter1d
from pygmt.src.grd2cpt import grd2cpt
from pygmt.src.grd2xyz import grd2xyz
from pygmt.src.grdclip import grdclip
from pygmt.src.grdcontour import grdcontour
from pygmt.src.grdcut import grdcut
from pygmt.src.grdfill import grdfill
from pygmt.src.grdfilter import grdfilter
from pygmt.src.grdgradient import grdgradient
from pygmt.src.grdhisteq import grdhisteq
from pygmt.src.grdimage import grdimage
from pygmt.src.grdinfo import grdinfo
from pygmt.src.grdlandmask import grdlandmask
from pygmt.src.grdproject import grdproject
from pygmt.src.grdsample import grdsample
from pygmt.src.grdtrack import grdtrack
from pygmt.src.grdview import grdview
from pygmt.src.grdvolume import grdvolume
from pygmt.src.histogram import histogram
from pygmt.src.image import image
from pygmt.src.info import info
from pygmt.src.inset import inset
from pygmt.src.legend import legend
from pygmt.src.logo import logo
from pygmt.src.makecpt import makecpt
from pygmt.src.meca import meca
from pygmt.src.nearneighbor import nearneighbor
from pygmt.src.plot import plot
from pygmt.src.plot3d import plot3d
from pygmt.src.project import project
from pygmt.src.rose import rose
from pygmt.src.select import select
from pygmt.src.shift_origin import shift_origin
from pygmt.src.solar import solar
from pygmt.src.sph2grd import sph2grd
from pygmt.src.sphdistance import sphdistance
from pygmt.src.sphinterpolate import sphinterpolate
from pygmt.src.subplot import set_panel, subplot
from pygmt.src.surface import surface
from pygmt.src.ternary import ternary
from pygmt.src.text import text_ as text  # "text" is an argument within "text_"
from pygmt.src.tilemap import tilemap
from pygmt.src.timestamp import timestamp
from pygmt.src.triangulate import triangulate
from pygmt.src.velo import velo
from pygmt.src.which import which
from pygmt.src.wiggle import wiggle
from pygmt.src.x2sys_cross import x2sys_cross
from pygmt.src.x2sys_init import x2sys_init
from pygmt.src.xyz2grd import xyz2grd
