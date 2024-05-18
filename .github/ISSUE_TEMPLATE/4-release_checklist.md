---
name: PyGMT release checklist
about: Checklist for a new PyGMT release.
title: Release PyGMT vX.Y.Z
labels: maintenance
assignees: ''

---

**Release**: [v0.x.x](https://github.com/GenericMappingTools/pygmt/milestones/?)
**Scheduled Date**: YYYY/MM/DD
**Pull request due date**: YYYY/MM/DD

**Priority PRs/issues to complete prior to release**
- [ ] Wrap X ()
- [ ] Wrap Y ()

**Before release**:
- [ ] Check [SPEC 0](https://scientific-python.org/specs/spec-0000/) to see if we need to bump the minimum supported versions of GMT, Python and core package dependencies (NumPy/Pandas/Xarray)
- [ ] Run `make codespell` to check common misspellings. If there are any, either fix them or add them to `ignore-words-list` in `pyproject.toml`
- [ ] Check to ensure that:
  - [ ] All tests pass in the ["GMT Legacy Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_legacy.yaml)
  - [ ] All tests pass in the ["GMT Dev Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml)
  - [ ] All tests pass in the ["Doctests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_doctests.yaml)
  - [ ] Deprecations and related tests are removed for this version by running `grep --include="*.py" -r 'remove_version="vX.Y.Z"' pygmt` from the base of the repository
- [ ] Update warnings in `pygmt.show_versions()` as well as notes in [Common installation issues](https://www.pygmt.org/dev/install.html#not-working-transparency)
      and [Testing your install]((https://www.pygmt.org/dev/install.html#testing-your-install) regarding GMT-Ghostscript incompatibility
- [ ] Reserve a DOI on [Zenodo](https://zenodo.org) by clicking on "New Version"
- [ ] Review the ["PyGMT Team" page](https://www.pygmt.org/dev/team.html)
- [ ] Finish up 'Changelog entry for v0.x.x' Pull Request:
  - [ ] Add a new entry in `doc/_static/version_switch.js` for documentation switcher
  - [ ] Update `CITATION.cff` and BibTeX at https://github.com/GenericMappingTools/pygmt#citing-pygmt
    - [ ] Update authorship list
    - [ ] Update DOI (and url for BibTeX)
    - [ ] Update version
    - [ ] Update date released
  - [ ] Add the documentation link `doc/minversions.md`
  - [ ] Add minimum required version information `doc/minversions.md`
  - [ ] Copy draft changelog from Release Drafter and edit it to look nice ([see maintainers guide for details](https://www.pygmt.org/dev/maintenance.html#updating-the-changelog))

**Release**:
- [ ] At the [PyGMT release page on GitHub](https://github.com/GenericMappingTools/pygmt/releases):
  - [ ] Edit the draft release notes with the finalized changelog
  - [ ] Set the tag version and release title to vX.Y.Z
  - [ ] Make a release by clicking the 'Publish Release' button, this will automatically create a tag too
- [ ] Manually upload the pygmt-vX.Y.Z.zip and baseline-images.zip files to https://zenodo.org/deposit, ensure that it is filed under the correct reserved DOI

**After release**:
- [ ] Update conda-forge [pygmt-feedstock](https://github.com/conda-forge/pygmt-feedstock) [Done automatically by conda-forge's bot, but remember to pin SPEC0 versions]
- [ ] Bump PyGMT version on https://github.com/GenericMappingTools/try-gmt (after conda-forge update)
- [ ] Announce the release on:
  - [ ] GMT [forum](https://forum.generic-mapping-tools.org/c/news/) (do this announcement first! draft on https://hackmd.io/@pygmt. requires moderator status)
  - [ ] [ResearchGate](https://www.researchgate.net) (after forum announcement, add new version as research item via the **code** category, be sure to include the corresponding new Zenodo DOI)
---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
