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
	@echo "  api        generate rst source files of API documentation"
	@echo "  server     make a local HTTP server for previewing the built documentation"
	@echo "  clean      clean up built and generated files"

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

server:
	cd $(BUILDDIR)/html && python -m http.server 8009

clean:
	rm -rf $(BUILDDIR)/doctrees
	rm -rf $(BUILDDIR)/html
	rm -rf $(BUILDDIR)/linkcheck
	rm -rf $(BUILDDIR)/doctest
	rm -rf api/generated
	rm -rf gallery
	rm -rf tutorials
	rm -rf projections
