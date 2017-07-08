"""
Tests psbasemap.
"""
import pytest

from .utils import figure_comparison_test
from .. import figure, psbasemap


def test_basemap_required_args():
    "psbasemap fails when not given required arguments"
    figure()
    with pytest.raises(AssertionError):
        psbasemap(R='10/70/-3/8', J='X4i/3i')


@figure_comparison_test
def test_basemap_d():
    "Make sure the D option works"
    figure()
    psbasemap(R='10/70/-300/800', J='X3i/5i', B='af',
              D='30/35/-200/500', F=True)


def test_basemap_d_raises():
    "Make sure the D raises an error when F not given."
    figure()
    with pytest.raises(AssertionError):
        psbasemap(R='10/70/-300/800', J='X3i/5i', B='af', D='30/35/-200/500')


@figure_comparison_test
def test_psbasemap():
    "Create a simple basemap plot"
    figure()
    psbasemap(R='10/70/-3/8', J='X4i/3i', B='afg', P=True)


@figure_comparison_test
def test_psbasemap_list_region():
    "Create a simple basemap plot passing the region as a list"
    figure()
    psbasemap(R=[-20, 50, 200, 500], J='X3i/3i', B='a')


@figure_comparison_test
def test_psbasemap_loglog():
    "Create a loglog basemap plot"
    figure()
    psbasemap(R='1/10000/1e20/1e25', J='X25cl/15cl',
              Bx='2+lWavelength', By='a1pf3+lPower', B='WS')


@figure_comparison_test
def test_psbasemap_power_axis():
    "Create a power axis basemap plot"
    figure()
    psbasemap(R=[0, 100, 0, 5000], J='x1p0.5/-0.001',
              B='x1p+l"Crustal age"y500+lDepth')


@figure_comparison_test
def test_psbasemap_polar():
    "Create a polar basemap plot"
    figure()
    psbasemap(R='0/360/0/1000', J='P6i', B='afg')


@figure_comparison_test
def test_psbasemap_winkel_tripel():
    "Create a Winkel Tripel basemap plot"
    figure()
    psbasemap(R='90/450/-90/90', J='R270/25c', B='afg')


@figure_comparison_test
def test_psbasemap_aliases():
    "Make sure the argument aliases work"
    figure()
    psbasemap(region=[0, 360, -90, 90], projection='W7i', frame=True,
              portrait=True)
