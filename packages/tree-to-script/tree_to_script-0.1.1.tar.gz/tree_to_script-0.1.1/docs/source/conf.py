# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../tree_to_script'))

project = 'tree-to-script'
copyright = '2024, vanuan'
author = 'vanuan'

extensions = ['myst_parser', 'sphinx.ext.autodoc']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
