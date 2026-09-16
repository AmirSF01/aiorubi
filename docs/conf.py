import datetime
import os

import aiorubi

project = "aiorubi"
author = "Amir S. Farahani"
copyright = f"{datetime.date.today().year}, {author}"
release = aiorubi.__version__
version = release
api_version = aiorubi.__api_version__

# Read the Docs builds one language per (linked translation) project and exposes
# it via READTHEDOCS_LANGUAGE; without it Sphinx defaults to English. Locally the
# Makefile / build script pass `-D language=fa`, which overrides this value.
language = os.environ.get("READTHEDOCS_LANGUAGE") or "en"

templates_path = ["_templates"]
html_theme = "furo"
html_logo = "_static/logo.png"
html_static_path = ["_static"]
todo_include_todos = True
pygments_style = "sphinx"
htmlhelp_basename = project
html_theme_options = {}
highlight_language = "python3"

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx_substitution_extensions",
    "sphinx_copybutton",
    "sphinx_design",
]

rst_prolog = f"""
.. |api_version| replace:: {aiorubi.__api_version__}

.. role:: pycode(code)
   :language: python3
"""

locale_dirs = ["locales/"]
gettext_compact = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "description"

exclude_patterns = ["_build", "locales", "Thumbs.db", ".DS_Store"]
source_suffix = ".rst"
master_doc = "index"

html_title = f"{project} {release} documentation"
html_css_files = ["bilingual.css"]
html_js_files = ["language_switcher.js"]
html_context = {
    "display_github": True,
    "github_user": "AmirSF01",
    "github_repo": "aiorubi",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

latex_documents = [
    (master_doc, f"{project}.tex", f"{project} Documentation", author, "manual"),
]
man_pages = [(master_doc, project, f"{project} Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        "Modern and fully asynchronous framework for the Rubika Bot API",
        "Miscellaneous",
    ),
]


def skip_model_prefixed_members(app, what, name, obj, skip, options):
    if name.startswith("model_"):
        return True
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_model_prefixed_members)
