# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    = -j auto
SPHINXBUILD   = sphinx-build
SPHINXAUTOGEN = sphinx-autogen
BUILDDIR      = _build

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees  $(SPHINXOPTS) .

.PHONY: help all api html server clean

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all          build the HTML files from the existing rst sources"
	@echo "  api          generate rst source files of API documentation"
	@echo "  html         build the HTML files from the existing rst sources"
	@echo "  html-noplot  build the HTML files without running any examples"
	@echo "  server       make a local HTTP server for previewing the built documentation"
	@echo "  clean        clean up built and generated files"

all: html

api:
	@echo
	@echo "Generating rst source files of API documentation."
	@echo
	$(SPHINXAUTOGEN) -i -t _templates -o api/generated api/*.rst

html: api
	@echo
	@echo "Building HTML files."
	@echo
	# Set PYGMT_USE_EXTERNAL_DISPLAY to "false" to disable external display
	PYGMT_USE_EXTERNAL_DISPLAY="false" $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

html-noplot: api
	@echo
	@echo "Building HTML files without example plots."
	@echo
	$(SPHINXBUILD) -D plot_gallery=0 -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

server:
	@echo
	@echo "Running a server on port 8009."
	@echo "Open http://localhost:8009 in a web browser to preview the documentation."
	@echo
	cd $(BUILDDIR)/html && python -m http.server 8009

clean:
	rm -rf $(BUILDDIR)
	rm -rf api/generated
	rm -rf gallery
	rm -rf tutorials
	rm -rf get_started
	rm -rf projections
