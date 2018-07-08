# Build, package, test, and clean

TESTDIR=tmp-test-dir-with-unique-name
PYTEST_ARGS=--doctest-modules -v --pyargs
PYTEST_COV_ARGS=--cov-config=../.coveragerc --cov-report=term-missing
FORMAT_FILES=gmt setup.py doc/conf.py
LINT_FILES=gmt setup.py

help:
	@echo "Commands:"
	@echo ""
	@echo "    develop       install in editable mode"
	@echo "    test          run the test suite (including doctests)"
	@echo "    check         run code quality checks (black and pylint)"
	@echo "    format        run black to automatically format the code"
	@echo "    coverage      calculate test coverage"
	@echo "    clean         clean up build and generated files"
	@echo ""

develop:
	pip install --no-deps -e .

test:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	cd $(TESTDIR); python -c "import gmt; gmt.test()"
	rm -r $(TESTDIR)

coverage:
	# Run a tmp folder to make sure the tests are run on the installed version
	mkdir -p $(TESTDIR)
	@echo ""
	@cd $(TESTDIR); python -c "import gmt; gmt.print_clib_info()"
	@echo ""
	cd $(TESTDIR); pytest $(PYTEST_COV_ARGS) --cov=gmt $(PYTEST_ARGS) gmt
	cp $(TESTDIR)/.coverage* .
	rm -r $(TESTDIR)

format:
	black $(FORMAT_FILES)

check:
	black --check $(FORMAT_FILES)
	pylint $(LINT_FILES)

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache
	rm -rvf $(TESTDIR)
	rm -rvf baseline
