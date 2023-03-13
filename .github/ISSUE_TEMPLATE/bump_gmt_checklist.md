---
name: Bump GMT version checklist
about: Checklist for bumping the minimum required GMT version.
title: Bump to GMT X.Y.Z
labels: maintenance
assignees: ''

---

:tada: [GMT X.Y.Z](https://github.com/GenericMappingTools/gmt/releases/tag/X.Y.Z) has been released! It is installable from the
[conda-forge channel](https://anaconda.org/conda-forge/gmt/files) using the following command:

`mamba install -c conda-forge gmt=X.Y.Z`

<!-- Please add specific checklist items for the tests, xfail pytest markers, and deprecated syntax that need to be updated. -->

**To-Do for bumping the GMT version in CI**:

- [ ] Bump the GMT version in CI (1 PR)
  - [ ] Update `.github/workflows/cache_data.yaml`
  - [ ] Update `.github/workflows/ci_docs.yml`
  - [ ] Update `.github/workflows/ci_tests.yaml`
  - [ ] Update `ci/requirements/docs.yml`
  - [ ] Update `environment.yml`
- [ ] Fix failing tests (1 or more PRs)
- [ ] Fix [xfail](https://docs.pytest.org/en/stable/skipping.html#xfail-mark-test-functions-as-expected-to-fail) pytest markers on tests that are now xpass

**To-Do for bumping the minimum required GMT version**:

- [ ] Bump the minimum required GMT version (1 PR)
  - [ ] Update `doc/install.rst`
  - [ ] Update `required_version` in `pygmt/clib/session.py`
  - [ ] Update `test_get_default` in `pygmt/tests/test_clib.py`
  - [ ] Update compatibility table in `README.rst`
- [ ] Remove [xfail](https://docs.pytest.org/en/stable/skipping.html#xfail-mark-test-functions-as-expected-to-fail) pytest markers on tests that are now xpass
- [ ] Update deprecated syntax in source code and examples based on the [GMT Changelog](https://docs.generic-mapping-tools.org/latest/changes.html)
