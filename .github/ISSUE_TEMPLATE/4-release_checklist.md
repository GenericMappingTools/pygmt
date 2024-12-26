---
name: PyGMT release checklist
about: Checklist for a new PyGMT release. [For project maintainers only!]
title: Release PyGMT vX.Y.Z
labels: maintenance
assignees: ''

---

**Release**: [v0.x.x](https://github.com/GenericMappingTools/pygmt/milestones/?)
**Scheduled Date**: 20YY/MM/DD
**Pull request due date**: 20YY/MM/DD
**DOI**: `10.5281/zenodo.XXXXXXX`

**Priority PRs/issues to complete prior to release**

- [ ] Wrap X ()
- [ ] Wrap Y ()

**Before release**:

- [ ] Check [SPEC 0](https://scientific-python.org/specs/spec-0000/) to see if we need to bump the minimum supported versions of GMT, Python and
      core package dependencies (NumPy, pandas, Xarray)
- [ ] Review the ["PyGMT Team" page](https://www.pygmt.org/dev/team.html)
- [ ] Check to ensure that:
  - [ ] Deprecated workarounds/codes/tests are removed. Run `grep "# TODO" **/*.py` to find all potential TODOs.
  - [ ] All tests pass in the ["GMT Legacy Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_legacy.yaml)
  - [ ] All tests pass in the ["GMT Dev Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml)
  - [ ] All tests pass in the ["Doctests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_doctests.yaml)
- [ ] Update warnings in `pygmt/_show_versions.py` as well as notes in
      [Not working transparency](https://www.pygmt.org/dev/install.html#not-working-transparency)
      regarding GMT-Ghostscript incompatibility
- [ ] Reserve a DOI on [Zenodo](https://zenodo.org) by clicking on "New Version"
- [ ] Finish up the "Changelog entry for v0.x.x" Pull Request (Use the previous changelog PR as a reference)
- [ ] Run `make codespell` to check common misspellings. If there are any, either fix them or add them to `ignore-words-list` in `pyproject.toml`
- [ ] Draft the announcement on https://hackmd.io/@pygmt

**Release**:

- [ ] At the [PyGMT release page on GitHub](https://github.com/GenericMappingTools/pygmt/releases):
  - [ ] Edit the draft release notes with the finalized changelog
  - [ ] Set the tag version and release title to vX.Y.Z
  - [ ] Make a release by clicking the 'Publish Release' button, this will automatically create a tag too
- [ ] Download pygmt-X.Y.Z.zip (rename to pygmt-vX.Y.Z.zip) and baseline-images.zip from
      the release page, and upload the two zip files to https://zenodo.org/deposit,
      ensure that they are filed under the correct reserved DOI

**After release**:

- [ ] Update conda-forge [pygmt-feedstock](https://github.com/conda-forge/pygmt-feedstock)
      [Done automatically by conda-forge's bot. Remember to pin Python and SPEC0 versions]
- [ ] Bump PyGMT version on https://github.com/GenericMappingTools/try-gmt (after conda-forge update)
- [ ] Announce the release on:
  - [ ] GMT [forum](https://forum.generic-mapping-tools.org/c/news/) (do this announcement first! Requires moderator status)
  - [ ] [ResearchGate](https://www.researchgate.net) (after forum announcement, add new version as research item via the **code** category, be sure to include the corresponding new Zenodo DOI)

---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
