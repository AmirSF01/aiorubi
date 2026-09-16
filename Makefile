# =================================================================================================
# Docs
# =================================================================================================

locales := fa
locale_targets := $(addprefix docs-serve-, $(locales))
locales_pot := _build/gettext
docs_dir := docs

docs-gettext:
	uv run --extra docs bash -c 'cd $(docs_dir) && make gettext'
	uv run --extra docs bash -c 'cd $(docs_dir) && sphinx-intl update -p $(locales_pot) $(addprefix -l , $(locales))'
.PHONY: docs-gettext

docs-serve:
	uv run --extra docs sphinx-autobuild --watch aiorubi/ docs/ docs/_build/ $(OPTS)
.PHONY: docs-serve

$(locale_targets): docs-serve-%:
	$(MAKE) docs-serve OPTS="-D language=$(subst docs-serve-,,$@)"
.PHONY: $(locale_targets)

# =================================================================================================
# Release
# =================================================================================================

.PHONY: bump
bump:
	uv run python scripts/bump_version.py $(args)
