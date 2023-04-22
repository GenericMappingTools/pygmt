# Build, package, test, and clean
PROJECT=pygmt
TESTDIR=tmp-test-dir-with-unique-name
PYTEST_COV_ARGS=--cov=$(PROJECT) --cov-config=../pyproject.toml \
			--cov-report=term-missing --cov-report=xml --cov-report=html
FORMAT_FILES=$(PROJECT) doc/conf.py examples
LINT_FILES=$(PROJECT) doc/conf.py

help:
	@echo "Commands:"
	@echo ""
	@echo "  install        install in editable mode"
	@echo "  package        build source and wheel distributions"
	@echo "  test           run the test suite (including some doctests) and report coverage"
	@echo "  fulltest       run the test suite (including all doctests)"
	@echo "  doctest        run the doctests only"
	@echo "  test_no_images run the test suite (including all doctests) but skip image comparisons"
	@echo "  format         run black, blackdoc, docformatter and isort to automatically format the code"
	@echo "  check          run code style and quality checks (black, blackdoc, docformatter, flakeheaven and isort)"
	@echo "  lint           run pylint for a deeper (and slower) quality check"
	@echo "  clean          clean up build and generated files"
	@echo "  distclean      clean up build and generated files, including project metadata files"
	@echo ""

install:
	python -m pip install --no-deps -e .

package:
	python -m build

_runtest:
	# Run in a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	cd $(TESTDIR); PYGMT_USE_EXTERNAL_DISPLAY="false" pytest $(PYTEST_ARGS) --pyargs $(PROJECT)
	@echo ""
	if [ -e $(TESTDIR)/coverage.xml ]; then cp $(TESTDIR)/coverage.xml .; fi
	if [ -e $(TESTDIR)/htmlcov ]; then cp -r $(TESTDIR)/htmlcov .; fi
	rm -r $(TESTDIR)

# run regular tests (unit tests + some doctests)
test: PYTEST_ARGS=--doctest-plus $(PYTEST_COV_ARGS) ${PYTEST_EXTRA}
test: _runtest

# run full tests (unit tests + all doctests)
fulltest: PYTEST_ARGS=${PYTEST_EXTRA}
fulltest: _runtest

# run doctests only
doctest: PYTEST_ARGS=--ignore=../pygmt/tests ${PYTEST_EXTRA}
doctest: _runtest

# run tests without image comparisons
# run pytest without the --mpl option to disable image comparisons
# use '-o addopts' to override 'addopts' settings in pyproject.toml file
test_no_images: PYTEST_ARGS=-o addopts="--verbose --durations=0 --durations-min=0.2 --doctest-modules"
test_no_images: _runtest

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
