# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import shutil
from sphinx_gallery.scrapers import figure_rst
project = 'pykz'
copyright = '2025, Mathijs Schuurmans'
author = 'Mathijs Schuurmans'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_gallery.gen_gallery',
    "sphinx_codeautolink",
]

templates_path = ['_templates']
exclude_patterns = []


# Define custom PDF scraper
sys.path.insert(0, os.path.abspath('..'))


def pdf_scraper(block, block_vars, gallery_conf):
    """Scrape PDFs and move them to the right directory."""
    import pdf2image
    from glob import glob

    image_path_iterator = block_vars['image_path_iterator']
    path_current_example = os.path.dirname(block_vars['src_file'])
    pdfs = sorted(glob(os.path.join(path_current_example, '*.pdf')))

    # Iterate through PNGs, copy them to the Sphinx-Gallery output directory
    image_names = list()
    image_path_iterator = block_vars['image_path_iterator']
    seen = set()
    for pdf in pdfs:
        if pdf not in seen:
            seen |= set(pdf)
            this_image_path = image_path_iterator.next()
            image_names.append(this_image_path)
            print(f"Converting {pdf} to {this_image_path}")
            pdf2image.convert_from_path(pdf, single_file=True,
                                        paths_only=True,
                                        transparent=False,
                                        output_file=os.path.splitext(this_image_path)[0],
                                        output_folder=os.path.dirname(this_image_path),
                                        dpi=500,
                                        fmt="png")
            assert os.path.isfile(this_image_path)
            shutil.move(pdf, this_image_path.replace("png", "pdf"))
    # Use the `figure_rst` helper function to generate reST for image files
    return figure_rst(image_names, gallery_conf['src_dir'])


sphinx_gallery_conf = {
    'examples_dirs': '../../examples',   # Path from conf.py to examples folder
    'recommender': {"enable": True, "n_examples": 5, "min_df": 3, "max_df": 0.9},
    'gallery_dirs': 'gallery',     # This will be created relative to doc build
    'filename_pattern': '/',
    'image_scrapers': (pdf_scraper),  # Add PDF scraper
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
