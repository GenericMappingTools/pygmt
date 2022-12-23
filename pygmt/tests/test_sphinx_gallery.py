"""
Test the sphinx-gallery scraper and code required to make it work.
"""
import os
from tempfile import TemporaryDirectory

import pytest
from pygmt.figure import SHOWED_FIGURES, Figure

pygmt_sphinx_gallery = pytest.importorskip(
    "pygmt.sphinx_gallery", reason="Requires sphinx-gallery to be installed"
)
pytest.importorskip("IPython", reason="Requires IPython to be installed")


def test_pygmtscraper():
    """
    Make sure the scraper finds the figures and removes them from the pool.
    """
    showed = SHOWED_FIGURES.copy()
    for _ in range(len(SHOWED_FIGURES)):
        SHOWED_FIGURES.pop()
    try:
        fig = Figure()
        fig.coast(region="BR", projection="M6i", land="gray", frame=True)
        fig.show()
        assert len(SHOWED_FIGURES) == 1
        assert SHOWED_FIGURES[0] is fig
        scraper = pygmt_sphinx_gallery.PyGMTScraper()
        with TemporaryDirectory(dir=os.getcwd()) as tmpdir:
            conf = {"src_dir": "meh"}
            fname = os.path.join(tmpdir, "meh.png")
            block_vars = {"image_path_iterator": (i for i in [fname])}
            assert not os.path.exists(fname)
            scraper(None, block_vars, conf)
            assert os.path.exists(fname)
            assert not SHOWED_FIGURES
    finally:
        SHOWED_FIGURES.extend(showed)
