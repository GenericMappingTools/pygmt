# Build, package, test, and clean
PROJECT=pygmt
TESTDIR=tmp-test-dir-with-unique-name
PYTEST_COV_ARGS=--cov=$(PROJECT) --cov-config=../pyproject.toml \
			--cov-report=term-missing --cov-report=xml --cov-report=html \
			--pyargs ${PYTEST_EXTRA}
FORMAT_FILES=$(PROJECT) doc/conf.py examples
LINT_FILES=$(PROJECT) doc/conf.py

help:
	@echo "Commands:"
	@echo ""
	@echo "  install        install in editable mode"
	@echo "  package        build source and wheel distributions"
	@echo "  test           run the test suite (including some doctests) and report coverage"
	@echo "  fulltest       run the test suite (including all doctests) and report coverage"
	@echo "  test_no_images run the test suite (including all doctests) but skip image comparisons"
	@echo "  format         run black, blackdoc, docformatter and isort to automatically format the code"
	@echo "  check          run code style and quality checks (black, blackdoc, docformatter, flakeheaven and isort)"
	@echo "  lint           run pylint for a deeper (and slower) quality check"
	@echo "  clean          clean up build and generated files"
	@echo "  distclean      clean up build and generated files, including project metadata files"
	@echo ""

install:
	pip install --no-deps -e .

package:
	python -m build --sdist --wheel

test:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	cd $(TESTDIR); PYGMT_USE_EXTERNAL_DISPLAY="false" pytest $(PYTEST_COV_ARGS) --doctest-plus $(PROJECT)
	cp $(TESTDIR)/coverage.xml .
	cp -r $(TESTDIR)/htmlcov .
	rm -r $(TESTDIR)

fulltest:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	cd $(TESTDIR); PYGMT_USE_EXTERNAL_DISPLAY="false" pytest $(PYTEST_COV_ARGS) $(PROJECT)
	cp $(TESTDIR)/coverage.xml .
	cp -r $(TESTDIR)/htmlcov .
	rm -r $(TESTDIR)

test_no_images:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	# run pytest without the --mpl option to disable image comparisons
	# use -o to override the addopts in pyproject.toml file
	cd $(TESTDIR); \
		PYGMT_USE_EXTERNAL_DISPLAY="false" \
		pytest -o addopts="--verbose --durations=0 --durations-min=0.2 --doctest-modules" \
		$(PYTEST_COV_ARGS) $(PROJECT)
	rm -r $(TESTDIR)

format:
	isort .
	docformatter --in-place $(FORMAT_FILES)
	black $(FORMAT_FILES)
	blackdoc $(FORMAT_FILES)

check:
	isort . --check
	docformatter --check $(FORMAT_FILES)
	black --check $(FORMAT_FILES)
	blackdoc --check $(FORMAT_FILES)
	FLAKEHEAVEN_CACHE_TIMEOUT=0 flakeheaven lint $(FORMAT_FILES)

lint:
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} +
	find . -name "*~" -exec rm -v {} +
	find . -type d -name  "__pycache__" -exec rm -rv {} +
	rm -rvf build dist .eggs MANIFEST .coverage .cache .pytest_cache htmlcov coverage.xml
	rm -rvf $(TESTDIR)
	rm -rvf baseline
	rm -rvf result_images
	rm -rvf results

distclean: clean
	rm -rvf *.egg-info
