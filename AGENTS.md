# Agent Guide for PyGMT

This file gives coding agents the project-specific context needed to work safely in
this repository. It summarizes the contributor and maintainer guidance; when in doubt,
prefer the authoritative sources in `CONTRIBUTING.md`, `doc/contributing.md`, and
`doc/maintenance.md`.

## Project Overview

PyGMT is a Python interface to the Generic Mapping Tools (GMT). The codebase wraps GMT
modules in Pythonic functions and methods, handles scientific Python data structures,
and provides documentation, gallery examples, tutorials, and image-based regression
tests.

The project values small, focused pull requests. Avoid unrelated cleanup, generated
metadata churn, or broad refactors unless they are required for the requested change.
The `main` branch is expected to stay tested and releasable; do not push directly to it.

## Repository Layout

- `pygmt/`: Python package source.
- `pygmt/src/`: GMT wrapper implementations and most `Figure` plotting methods.
- `pygmt/figure.py`: `Figure` class; attaches plotting functions from `pygmt/src`.
- `pygmt/clib/`: GMT C API session and virtual file handling.
- `pygmt/helpers/`: decorators, common docstrings, testing helpers, temporary files,
  encoding helpers, and utility functions.
- `pygmt/params/`: structured parameter helper classes.
- `pygmt/datasets/`: sample and remote dataset loaders.
- `pygmt/tests/`: pytest suite, test data, and image baseline metadata.
- `pygmt/tests/baseline/`: DVC-tracked image baselines; commit `.png.dvc` files, not
  raw baseline PNG blobs.
- `examples/gallery/`: concise sphinx-gallery examples.
- `examples/tutorials/`: longer tutorial-style examples.
- `doc/`: documentation sources, API index, contributor and maintainer guides.
- `.github/workflows/`: CI, docs, release, formatting, type checking, and DVC workflows.

## Development Environment

The recommended development environment is the conda environment in `environment.yml`.
It includes GMT, Ghostscript, DVC, pytest, pytest-mpl, Ruff, prek, Sphinx, mypy, and
documentation dependencies.

Common setup:

```bash
mamba env create --file environment.yml
mamba activate pygmt
make install
```

`make install` installs PyGMT in editable mode with `python -m pip install --no-deps -e .`.

## Core Commands

Use the narrowest command that validates the change.

```bash
make test              # unit tests, selected doctests, image comparisons, coverage
make fulltest          # unit tests and all doctests
make doctest           # doctests only
make test_no_images    # tests/doctests without pytest-mpl image comparisons
make check             # Ruff lint and format check
make format            # Ruff auto-fix/format and prek hooks
make codespell         # spelling checks
make typecheck         # mypy
make package           # source and wheel distributions
```

For focused testing, run:

```bash
pytest pygmt/tests/test_<name>.py
pytest -k KEYWORD pygmt/tests
```

PyGMT tests should avoid opening external viewers. The Makefile sets
`PYGMT_USE_EXTERNAL_DISPLAY=false` where needed; set it manually for ad hoc test or doc
runs that may render figures.

## Style and Conventions

- Python requires 3.12 or newer.
- Formatting and linting are managed by Ruff; do not hand-format large areas.
- Ruff uses an 88-character line length. Docstrings should also be manually wrapped to
  88 characters for readable IPython/Jupyter display.
- Docstrings follow NumPy style.
- Python file and directory names use underscores, not hyphens.
- New parameter names should separate words with underscores, except established short
  forms such as `surftype`, `outgrid`, or `timefmt`.
- Use readable, direct code over clever compression.
- Add comments only when they explain non-obvious reasoning.
- The repository uses prek hooks for line endings, trailing whitespace, YAML checks,
  executable permissions, file mode 644, and workflow linting.

## Wrapping GMT Modules or Adding APIs

When adding a standalone wrapper:

1. Add a module in `pygmt/src/<module_name>.py`.
2. Add the function and a complete NumPy-style docstring.
3. Use existing wrappers with similar input/output behavior as templates.
4. Export standalone functions from `pygmt/src/__init__.py` and `pygmt/__init__.py`.
5. Add API documentation in `doc/api/index.rst`.
6. Add focused tests in `pygmt/tests/test_<module_name>.py`.

When adding a `Figure` method:

1. Implement the function in `pygmt/src/<method_name>.py`.
2. Import and attach it in `pygmt/figure.py`.
3. Add it to the appropriate section of `doc/api/index.rst`.
4. Add tests, including image tests when rendering behavior matters.

For GMT options and aliases:

- Prefer `AliasSystem`, `Alias`, `build_arg_list`, and common helper patterns already
  used in nearby modules.
- Check `COMMON_DOCSTRINGS` in `pygmt/helpers/decorators.py` before writing duplicate
  parameter documentation.
- Use `@fmt_docstring` when docstrings include shared placeholders.
- Use `@use_alias` where a module follows the decorator-based alias style.
- Use `Session.virtualfile_in` and related virtual file helpers for in-memory data.
- Validate PyGMT-specific Python behavior; do not duplicate exhaustive GMT option tests.

## Backwards Compatibility

PyGMT is pre-1.0 but still follows a formal compatibility and deprecation process.
Incompatible changes should be discussed, documented in release notes, and generally
introduced with a `FutureWarning`.

For parameter renames, use `@deprecate_parameter` after `@fmt_docstring` and before
`@use_alias`. Include a TODO with the expected removal version, following:

```python
# TODO(PyGMT>=X.Y.Z): Remove the deprecated "old_name" parameter.
```

Temporary TODOs should use the maintainer guide format:

```python
# TODO(package>=X.Y.Z): A brief description of the TODO item.
```

Do not use TODOs as a substitute for opening issues for unimplemented features.

## Testing Guidance

Prioritize tests for PyGMT-specific behavior:

- Python data structure handling: NumPy, pandas, xarray, dict-like inputs.
- Virtual file behavior and input validation.
- Alias conversion and argument construction.
- Backwards-compatible deprecation paths.
- Regression tests for serious bugs.

For plot rendering, prefer `@pytest.mark.mpl_image_compare` when a single generated
figure should match a baseline. Test functions must return one `pygmt.Figure`.

Use `check_figures_equal` from `pygmt.helpers.testing` when comparing two ways of
producing the same figure.

For image baselines:

```bash
dvc pull
pytest --mpl-generate-path=baseline pygmt/tests/test_<name>.py
```

Inspect generated images before accepting them. Move accepted PNGs into
`pygmt/tests/baseline/`, run `dvc add`, and commit only the resulting `.png.dvc` files.
Pushing actual image data requires `dvc push` and DAGsHub access; do not fake or bypass
that workflow.

## Documentation Guidance

Documentation has four main sources:

- API docs: docstrings in `pygmt/src/` and `pygmt/datasets/`.
- API index: `doc/api/index.rst`.
- Gallery examples: `examples/gallery/`.
- Tutorials: `examples/tutorials/`.

Build docs locally with:

```bash
cd doc
make all
```

For faster docs without running example plots:

```bash
cd doc
make html-noplot
```

Generated HTML is in `doc/_build/html`.

Documentation examples should be simple, explicit, and focused. Gallery examples should
highlight one feature. Tutorials can be more explanatory. Use SI units in examples.
Example scripts should include at least one `# %%` code block separator.

Docstring examples use doctest-style prompts. If example code should not be executed
during doctests, add `__doctest_skip__ = ["function_name"]` near the top of the module.

Use Sphinx roles consistently:

- `:func:`, `:class:`, `:meth:`, `:mod:` for Python API references.
- `:doc:` for documentation pages.
- `:gmt-docs:` for GMT documentation pages.
- `:gmt-term:` for GMT configuration parameters.

## Maintainer and Release Context

Most agents should not perform maintainer-only operations unless explicitly asked.
Important maintainer policies from `doc/maintenance.md`:

- PRs should be squash merged.
- Reviews should be polite, constructive, and welcoming.
- CI runs across Linux, macOS, and Windows.
- Dependencies follow SPEC 0 with project-specific extensions.
- Minimum supported versions are updated on major/minor releases, not patch releases.
- Releases are mostly automated through GitHub Actions, but changelog curation,
  Zenodo archiving, and conda-forge follow-up have manual steps.

Avoid editing release metadata (`doc/changes.md`, `doc/minversions.md`,
`CITATION.cff`, release badges, feedstock instructions) unless the task is explicitly
about releases or version support.

## Git and Workspace Safety

- Check `git status --short` before editing.
- Keep user changes. Do not revert unrelated modifications.
- Ignore unrelated untracked scratch files unless the task asks about them.
- Never use destructive commands such as `git reset --hard` or `git checkout --` unless
  explicitly requested and approved.
- Keep changes focused and explain any tests that could not be run because dependencies
  or external tools are unavailable.

