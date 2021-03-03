# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAUTOGEN = sphinx-autogen
BUILDDIR      = _build

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees  $(SPHINXOPTS) .

.PHONY: help clean html linkcheck doctest api

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  all        generate the complete webpage"
	@echo "  html       build the HTML files from the existing rst sources"
	@echo "  api        generate API documentation rst sources"
	@echo "  serve      make a HTTP server"
	@echo "  clean      clean up build and generated files"

all: html

html: api
	@echo
	@echo "Building HTML files."
	@echo
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

api:
	@echo
	@echo "Building API docs."
	@echo
	$(SPHINXAUTOGEN) -i -t _templates -o api/generated api/*.rst

serve:
	cd $(BUILDDIR)/html && python -m http.server 8009

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished; look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

clean:
	rm -rf $(BUILDDIR)/doctrees
	rm -rf $(BUILDDIR)/html
	rm -rf $(BUILDDIR)/linkcheck
	rm -rf $(BUILDDIR)/doctest
	rm -rf api/generated
	rm -rf modules
	rm -rf gallery
	rm -rf tutorials
	rm -rf projections
	rm -rf .ipynb_checkpoints
