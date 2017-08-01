# -*- coding: utf-8 -*-
import sys
import os
import datetime
import sphinx_bootstrap_theme

# Sphinx needs to be able to import the package to use autodoc and get the
# version number
sys.path.append(os.path.pardir)

from gmt import __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'numpydoc',
    'nbsphinx',
]

# Produce pages for each class and function
autosummary_generate = True
autodoc_default_flags = ['members', 'inherited-members']

numpydoc_class_members_toctree = False

# Sphinx project configuration
templates_path = ['_templates']
exclude_patterns = ['_build', '.ipynb_checkpoints']
source_suffix = '.rst'
# The encoding of source files.
source_encoding = 'utf-8-sig'
master_doc = 'index'

# General information about the project
year = datetime.date.today().year
project = u'GMT/Python'
copyright = u'2017, Leonardo Uieda'
version = ''

# These enable substitutions using |variable| in the rst files
rst_epilog = """
.. |year| replace:: {year}
""".format(year=year)

html_last_updated_fmt = '%b %d, %Y'
html_title = 'GMT/Python'
html_short_title = 'GMT/Python'
html_logo = ''
html_favicon = '_static/favicon.png'
html_static_path = ['_static']
html_extra_path = ['.nojekyll']
pygments_style = 'default'
add_function_parentheses = False
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
htmlhelp_basename = 'gmt-python'

html_sidebars = {
    'install': ['localtoc.html'],
    'api': ['localtoc.html'],
    'first-steps': ['localtoc.html'],
    'design': ['localtoc.html'],
}

# Theme config
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_theme_options = {
    'navbar_title': project,
    'navbar_links': [
        ('Install', 'install'),
        ('API', 'api'),
        ('Tutorial', 'first-steps'),
        ('Design', 'design'),
        ('Code', 'https://github.com/GenericMappingTools/gmt-python', True),
        ('Contact', 'https://gitter.im/GenericMappingTools/gmt-python', True),
    ],
    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,
    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,
    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "Page",
    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "Site",
    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 2,
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    'globaltoc_includehidden': "false",
    'navbar_class': "navbar",
    'navbar_fixed_top': "false",
    'source_link_position': "footer",
    'bootswatch_theme': "paper",
    'bootstrap_version': "3",
}

# Load the custom CSS files (needs sphinx >= 1.6 for this to work)
def setup(app):
    app.add_stylesheet("style.css")
