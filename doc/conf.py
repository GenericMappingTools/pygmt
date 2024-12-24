"""
Sphinx documentation configuration file.
"""

import datetime
import importlib

from packaging.requirements import Requirement
from pygmt import __commit__, __version__
from pygmt.clib import required_gmt_version
from pygmt.sphinx_gallery import PyGMTScraper
from sphinx_gallery.sorting import ExampleTitleSortKey, ExplicitOrder

# Dictionary for dependency name and minimum required versions
requirements = {
    Requirement(requirement).name: str(Requirement(requirement).specifier)
    for requirement in importlib.metadata.requires("pygmt")
}
requirements.update(
    {
        "python": importlib.metadata.metadata("pygmt")["Requires-Python"],
        "gmt": f">={required_gmt_version}",
    }
)

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
]

# Suppress warnings
suppress_warnings = [
    "myst.header",  # Document headings start at H2, not H1
]

# Autosummary pages will be generated by sphinx-autogen instead of sphinx-build
autosummary_generate = []

# Auto-generate header anchors with MyST parser
myst_heading_anchors = 4
# MyST extensions
# Reference: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "attrs_inline",  # Allow inline attributes after images
    "colon_fence",  # Allow code fences using colons
    "substitution",  # Allow substituitions
]
# These enable substitutions using {{ key }} in the Markdown files
myst_substitutions = {
    "requires": requirements,
}

# Configure MyST-NB
# Reference: https://myst-nb.readthedocs.io/en/latest/configuration.html
nb_render_markdown_format = "myst"  # Format for text/markdown rendering

# Render the return argument and attribute lists in the same way as the parameter lists
napoleon_use_rtype = False
napoleon_use_ivar = True

# Configure sphinx_auto_typehints
typehints_defaults = "comma"

# Define links to GMT docs
extlinks = {
    "gmt-docs": ("https://docs.generic-mapping-tools.org/6.5/%s", None),
    "gmt-term": ("https://docs.generic-mapping-tools.org/6.5/gmt.conf#term-%s", "%s"),
    "gmt-datasets": ("https://www.generic-mapping-tools.org/remote-datasets/%s", None),
}

# Configure intersphinx
intersphinx_mapping = {
    "contextily": ("https://contextily.readthedocs.io/en/stable/", None),
    "geopandas": ("https://geopandas.org/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pyarrow": ("https://arrow.apache.org/docs/", None),
    "python": ("https://docs.python.org/3/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "rasterio": ("https://rasterio.readthedocs.io/en/stable/", None),
    "rioxarray": ("https://corteva.github.io/rioxarray/stable/", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
    "xyzservices": ("https://xyzservices.readthedocs.io/en/stable", None),
}

# Configure sphinx-copybutton
# Reference: https://sphinx-copybutton.readthedocs.io
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True
copybutton_remove_prompts = True

sphinx_gallery_conf = {
    # Set paths to your examples scripts
    "examples_dirs": [
        "../examples/intro",
        "../examples/tutorials",
        "../examples/gallery",
        "../examples/projections",
    ],
    # Set paths where to save the generated examples
    "gallery_dirs": ["intro", "tutorials", "gallery", "projections"],
    "subsection_order": ExplicitOrder(
        [
            "../examples/intro",
            "../examples/tutorials/basics",
            "../examples/tutorials/advanced",
            "../examples/gallery/maps",
            "../examples/gallery/lines",
            "../examples/gallery/symbols",
            "../examples/gallery/images",
            "../examples/gallery/3d_plots",
            "../examples/gallery/seismology",
            "../examples/gallery/basemaps",
            "../examples/gallery/histograms",
            "../examples/gallery/embellishments",
            "../examples/projections/azim",
            "../examples/projections/conic",
            "../examples/projections/cyl",
            "../examples/projections/misc",
            "../examples/projections/nongeo",
            "../examples/projections/table",
        ]
    ),
    # Pattern to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery examples by the file names instead of number of lines [Default]
    "within_subsection_order": ExampleTitleSortKey,
    # Directory where function granular galleries are stored
    "backreferences_dir": "api/generated/backreferences",
    # Modules for which function level galleries are created (given as tuple of strings)
    "doc_module": ("pygmt",),
    # Insert links to documentation of objects in the examples
    "reference_url": {"pygmt": None},
    "image_scrapers": (PyGMTScraper(),),
    # Remove configuration comments from scripts
    "remove_config_comments": True,
    # Disable "nested_sections" [Default is True], to generate only a single index file
    # for the whole gallery. This is a new feature up on Sphinx-Gallery 0.11.0.
    "nested_sections": False,
}

# Configure Sphinx project
templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    # Workaround from https://github.com/executablebooks/MyST-NB/issues/363 to prevent
    # MyST-NB from parsing the .ipynb and .py files generated by Sphinx-Gallery.
    "intro/**.ipynb",
    "tutorials/**.ipynb",
    "gallery/**.ipynb",
    "projections/**.ipynb",
    "intro/**.py",
    "tutorials/**.py",
    "gallery/**.py",
    "projections/**.py",
]

source_suffix = ".rst"
needs_sphinx = "6.2"
# Encoding of source files
source_encoding = "utf-8-sig"
root_doc = "index"

# General information about the project
year = datetime.date.today().year
project = "PyGMT"
copyright = f"2017-{year}, The PyGMT Developers"  # noqa: A001
if len(__version__.split("+")) > 1 or __version__ == "unknown":
    version = "dev"
    # Set base URL for dev version
    html_baseurl = "https://pygmt.org/dev/"
else:
    version = __version__
    # Set base URL for stable version
    html_baseurl = "https://pygmt.org/latest/"
release = __version__

html_last_updated_fmt = "%b %d, %Y"
html_title = "PyGMT"
html_short_title = "PyGMT"
html_logo = ""
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_css_files = ["style.css"]
html_extra_path = []
pygments_style = "default"
add_function_parentheses = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# Configure theme
html_theme = "sphinx_rtd_theme"
html_theme_options = {"version_selector": True}
repository = "GenericMappingTools/pygmt"
repository_url = "https://github.com/GenericMappingTools/pygmt"
if __commit__:
    commit_link = (
        f'<a href="{repository_url}/commit/{ __commit__ }">{ __commit__[:8] }</a>'
    )
else:
    commit_link = (
        f'<a href="{repository_url}/releases/tag/{ __version__ }">{ __version__ }</a>'
    )
html_context = {
    "menu_links": [
        (
            '<i class="fa fa-gavel fa-fw"></i> Code of Conduct',
            "https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> License',
            f"{repository_url}/blob/main/LICENSE.txt",
        ),
        (
            '<i class="fa fa-comment fa-fw"></i> Contact',
            "https://forum.generic-mapping-tools.org",
        ),
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            repository_url,
        ),
    ],
    # Custom variables to enable "Improve this page"" and "Download notebook" links
    "doc_path": "doc",
    "galleries": sphinx_gallery_conf["gallery_dirs"],
    "gallery_dir": dict(
        zip(
            sphinx_gallery_conf["gallery_dirs"],
            sphinx_gallery_conf["examples_dirs"],
            strict=True,
        )
    ),
    "github_repo": repository,
    "github_version": "main",
    "commit": commit_link,
}
