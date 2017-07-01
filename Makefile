# Build, package, test, and clean

TESTDIR=tmp-test-dir-with-unique-name
PYTEST_ARGS=--doctest-modules -v --pyargs
PYTEST_COV_ARGS=--cov-config=../.coveragerc --cov-report=term-missing

help:
	@echo "Commands:"
	@echo ""
	@echo "    develop       install in editable mode"
	@echo "    test          run the test suite (including doctests)"
	@echo "    check         run all code quality checks (pep8, linter)"
	@echo "    pep8          check for PEP8 style compliance"
	@echo "    lint          run static analysis using pylint"
	@echo "    coverage      calculate test coverage"
	@echo "    clean         clean up build and generated files"
	@echo ""

develop:
	pip install --no-deps -e .

test:
	# Run a tmp folder to make sure the tests are run on the installed version
	# of Fatiando
	mkdir -p $(TESTDIR)
	cd $(TESTDIR); python -c "import gmt; gmt.test()"
	rm -r $(TESTDIR)

coverage:
	# Run a tmp folder to make sure the tests are run on the installed version
	# of Fatiando
	mkdir -p $(TESTDIR)
	cd $(TESTDIR); pytest $(PYTEST_COV_ARGS) --cov=gmt $(PYTEST_ARGS) gmt
	cp $(TESTDIR)/.coverage* .
	rm -r $(TESTDIR)

pep8:
	flake8 gmt setup.py

lint:
	pylint gmt setup.py

check: pep8 lint

clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache
	rm -rvf $(TESTDIR)
