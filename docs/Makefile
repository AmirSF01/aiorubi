# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXINTL    ?= sphinx-intl
SOURCEDIR     = .
BUILDDIR      = _build
LANGUAGES     ?= fa

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

gettext:
	@$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext" $(SPHINXOPTS) $(O)

update-intl: gettext
	$(SPHINXINTL) update -p $(BUILDDIR)/gettext $(addprefix -l , $(LANGUAGES))

mo:
	$(SPHINXINTL) -c conf.py build $(addprefix -l , $(LANGUAGES))

html-en:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html/en" $(SPHINXOPTS)

html-fa: mo
	$(SPHINXBUILD) -b html -D language=fa "$(SOURCEDIR)" "$(BUILDDIR)/html/fa" $(SPHINXOPTS)

bilingual: html-en html-fa
	@echo "Built $(BUILDDIR)/html/en and $(BUILDDIR)/html/fa"

.PHONY: help gettext update-intl mo html-en html-fa bilingual Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
