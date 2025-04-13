import os
import sys
from pathlib import Path

# Path setup
project_root = str(Path(__file__).parents[2].absolute())
sys.path.insert(0, project_root)

# Django setup - must happen before any model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matching_algo.docs_settings')

import django
from django.conf import settings

if not settings.configured:
    from matching_algo import docs_settings
django.setup()

# Project information
project = 'Matching Algo Documentation'
copyright = '2025, sherl'
author = 'sherl'

# Extensions configuration
extensions = [ 
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
templates_path = ['_templates']
exclude_patterns = []

# -- Autodoc settings -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'special-members': '__init__',
}

# -- HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']