"""
Test the sphinx-gallery scraper and code required to make it work.
"""
import os
from tempfile import TemporaryDirectory
import pytest

try:
    import sphinx_gallery
except ImportError:
    sphinx_gallery = None

from ..figure import Figure, SHOWED_FIGURES
from ..sphinx_gallery import PyGMTScraper


@pytest.mark.skipif(sphinx_gallery is None, reason="requires sphinx-gallery")
def test_pygmtscraper():
    "Make sure the scraper finds the figures and removes them from the pool."

    showed = [fig for fig in SHOWED_FIGURES]
    for _ in range(len(SHOWED_FIGURES)):
        SHOWED_FIGURES.pop()
    try:
        fig = Figure()
        fig.coast(region="BR", projection="M6i", land="gray", frame=True)
        fig.show()
        assert len(SHOWED_FIGURES) == 1
        assert SHOWED_FIGURES[0] is fig
        scraper = PyGMTScraper()
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
