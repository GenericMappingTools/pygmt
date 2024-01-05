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
	@echo "  format         run ruff to automatically format the code"
	@echo "  check          run ruff to check code style and quality"
	@echo "  codespell      run codespell to check common misspellings"
	@echo "  typecheck      run mypy for static type check"
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
	ruff check --fix $(FORMAT_FILES)
	ruff format $(FORMAT_FILES)

check:
	ruff check $(FORMAT_FILES)
	ruff format --check $(FORMAT_FILES)

codespell:
	@codespell

typecheck:
	mypy ${PROJECT}

clean:
	find . -name "*.pyc" -exec rm -v {} +
	find . -name "*~" -exec rm -v {} +
	find . -type d -name  "__pycache__" -exec rm -rv {} +
	rm -rvf build dist .eggs MANIFEST .coverage htmlcov coverage.xml
	rm -rvf .cache .mypy_cache .pytest_cache .ruff_cache
	rm -rvf $(TESTDIR)
	rm -rvf baseline
	rm -rvf result_images
	rm -rvf results

distclean: clean
	rm -rvf *.egg-info
