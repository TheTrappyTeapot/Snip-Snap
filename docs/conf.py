# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'Snip-Snap'
copyright = '2026, TheTrappyTeapot'
author = 'TheTrappyTeapot'
release = '1.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# Source directory configuration
source_suffix = '.rst'

# Templates path
templates_path = ['_templates']

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'source/_build']

# HTML theme
html_theme = 'sphinx_rtd_theme'

# HTML theme options
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': 'edit',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'github_url': 'https://github.com/TheTrappyTeapot/Snip-Snap',
}

# HTML static files
html_static_path = ['_static']

# Root document (formerly master_doc)
root_doc = 'source/index'
