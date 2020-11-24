# Build, package, test, and clean
PROJECT=pygmt
TESTDIR=tmp-test-dir-with-unique-name
PYTEST_ARGS=--cov=$(PROJECT) --cov-config=../pyproject.toml \
			--cov-report=term-missing --cov-report=xml --cov-report=html \
			--doctest-modules -v --mpl --mpl-results-path=results \
			--pyargs ${PYTEST_EXTRA}
BLACK_FILES=$(PROJECT) setup.py doc/conf.py examples
BLACKDOC_OPTIONS=--line-length 79
FLAKE8_FILES=$(PROJECT) setup.py doc/conf.py
LINT_FILES=$(PROJECT) setup.py doc/conf.py

help:
	@echo "Commands:"
	@echo ""
	@echo "  install   install in editable mode"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  format    run black and blackdoc to automatically format the code"
	@echo "  check     run code style and quality checks (black, blackdoc and flake8)"
	@echo "  lint      run pylint for a deeper (and slower) quality check"
	@echo "  clean     clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

test:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	cd $(TESTDIR); pytest $(PYTEST_ARGS) $(PROJECT)
	cp $(TESTDIR)/coverage.xml .
	cp -r $(TESTDIR)/htmlcov .
	rm -r $(TESTDIR)

format:
	black $(BLACK_FILES)
	blackdoc $(BLACKDOC_OPTIONS) $(BLACK_FILES)

check:
	black --check $(BLACK_FILES)
	blackdoc --check $(BLACKDOC_OPTIONS) $(BLACK_FILES)
	flake8 $(FLAKE8_FILES)

lint:
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	find . -name "*~" -exec rm -v {} \;
	find . -type d -name  "__pycache__" -exec rm -rv {} +
	rm -rvf build dist MANIFEST *.egg-info .coverage .cache htmlcov coverage.xml
	rm -rvf $(TESTDIR)
	rm -rvf baseline
	rm -rvf result_images
