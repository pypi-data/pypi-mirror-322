# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS     ?=
SPHINXBUILD    ?= sphinx-build
SOURCEDIR      = .
BUILDDIR       = _build
LANGUAGE       ?= en
BUILDDIRSUFFIX =

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

.PHONY: help Makefile gettext clean

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)/$(LANGUAGE)$(BUILDDIRSUFFIX)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*
	rm -f autotodo

# depends on autotodo.py but that does not work well with the catch-all below
autotodo:
	@./autotodo.py ../ .py TODO,FIXME,XXX

gettext: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)$(BUILDDIRSUFFIX)" $(SPHINXOPTS) $(O)

# Use to update *.po files
update_locale: Makefile gettext
	@sphinx-intl update -p "$(BUILDDIR)$(BUILDDIRSUFFIX)/gettext" -l $(LANGUAGE)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile autotodo
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)/$@/$(LANGUAGE)$(BUILDDIRSUFFIX)" -d "$(BUILDDIR)$(BUILDDIRSUFFIX)/doctrees/$(LANGUAGE)" $(SPHINXOPTS) -D language=$(LANGUAGE) $(O)
