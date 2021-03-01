# Build, package, test, and clean
PROJECT=pygmt
TESTDIR=tmp-test-dir-with-unique-name
PYTEST_COV_ARGS=--cov=$(PROJECT) --cov-config=../pyproject.toml \
			--cov-report=term-missing --cov-report=xml --cov-report=html \
			--pyargs ${PYTEST_EXTRA}
BLACK_FILES=$(PROJECT) setup.py doc/conf.py examples
BLACKDOC_OPTIONS=--line-length 79
DOCFORMATTER_FILES=$(PROJECT) setup.py doc/conf.py examples
DOCFORMATTER_OPTIONS=--recursive --pre-summary-newline --make-summary-multi-line --wrap-summaries 79 --wrap-descriptions 79
FLAKE8_FILES=$(PROJECT) setup.py doc/conf.py
LINT_FILES=$(PROJECT) setup.py doc/conf.py

help:
	@echo "Commands:"
	@echo ""
	@echo "  install   install in editable mode"
	@echo "  package   build source and wheel distributions"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  format    run black, blackdoc, docformatter and isort to automatically format the code"
	@echo "  check     run code style and quality checks (black, blackdoc, docformatter, flake8 and isort)"
	@echo "  lint      run pylint for a deeper (and slower) quality check"
	@echo "  clean     clean up build and generated files"
	@echo "  distclean clean up build and generated files, including project metadata files"
	@echo ""

install:
	pip install --no-deps -e .

package:
	python setup.py sdist bdist_wheel

test:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import $(PROJECT); $(PROJECT).show_versions()"
	@echo ""
	cd $(TESTDIR); pytest $(PYTEST_COV_ARGS) $(PROJECT)
	cp $(TESTDIR)/coverage.xml .
	cp -r $(TESTDIR)/htmlcov .
	rm -r $(TESTDIR)

format:
	isort .
	docformatter --in-place $(DOCFORMATTER_OPTIONS) $(DOCFORMATTER_FILES)
	black $(BLACK_FILES)
	blackdoc $(BLACKDOC_OPTIONS) $(BLACK_FILES)

check:
	isort . --check
	docformatter --check $(DOCFORMATTER_OPTIONS) $(DOCFORMATTER_FILES)
	black --check $(BLACK_FILES)
	blackdoc --check $(BLACKDOC_OPTIONS) $(BLACK_FILES)
	flake8 $(FLAKE8_FILES)

lint:
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} +
	find . -name "*~" -exec rm -v {} +
	find . -type d -name  "__pycache__" -exec rm -rv {} +
	rm -rvf build dist MANIFEST .coverage .cache .pytest_cache htmlcov coverage.xml
	rm -rvf $(TESTDIR)
	rm -rvf baseline
	rm -rvf result_images

distclean: clean
	rm -rvf *.egg-info
