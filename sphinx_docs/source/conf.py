# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'iGrafx P360 Live Mining SDK'
copyright = '2024, iGrafx'
author = 'iGrafx'
release = '2.35.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
for x in os.walk('../mining-python-sdk/igrafx_mining_sdk'):
    sys.path.insert(0, x[0])
sys.path.insert(0, os.path.abspath("../.."))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
