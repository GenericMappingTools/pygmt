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
- [ ] Check [NEP29](https://numpy.org/neps/nep-0029-deprecation_policy.html) to see if we need to bump the minimum Python and NumPy versions
- [ ] Check to ensure that:
  - [ ] All tests pass in the ["GMT Legacy Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_legacy.yaml)
  - [ ] All tests pass in the ["GMT Dev Tests" workflow](https://github.com/GenericMappingTools/pygmt/actions/workflows/ci_tests_dev.yaml)
  - [ ] Deprecations and related tests are removed for this version by running `grep --include="*.py" -r 'remove_version="vX.Y.Z"' pygmt` from the base of the repository
- [ ] Reserve a DOI on [Zenodo](https://zenodo.org) by clicking on "New Version"
- [ ] Finish up 'Changelog entry for v0.x.x' Pull Request:
  - [ ] Add a new entry in `doc/_static/version_switch.js` for documentation switcher
  - [ ] Update `CITATION.cff` and BibTeX at https://github.com/GenericMappingTools/pygmt#citing-pygmt
    - [ ] Update authorship list
    - [ ] Update DOI (and url for BibTeX)
    - [ ] Update version
    - [ ] Update date released
  - [ ] Add the documentation link https://github.com/GenericMappingTools/pygmt#compatibility-with-gmtpythonnumpy-versions
  - [ ] Add compatibility information https://github.com/GenericMappingTools/pygmt#compatibility-with-gmtpythonnumpy-versions
  - [ ] Copy draft changelog from Release Drafter and edit it to look nice ([see maintainers guide for details](https://www.pygmt.org/dev/maintenance.html#updating-the-changelog))

**Release**:
- [ ] At the [PyGMT release page on GitHub](https://github.com/GenericMappingTools/pygmt/releases):
  - [ ] Edit the draft release notes with the finalized changelog
  - [ ] Set the tag version and release title to vX.Y.Z
  - [ ] Make a release by clicking the 'Publish Release' button, this will automatically create a tag too
- [ ] Manually upload the pygmt-vX.Y.Z.zip and baseline-images.zip files to https://zenodo.org/deposit, ensure that it is filed under the correct reserved DOI

**After release**:
- [ ] Update conda-forge [pygmt-feedstock](https://github.com/conda-forge/pygmt-feedstock) [Done automatically by conda-forge's bot, but remember to pin NEP29 versions]
- [ ] Bump PyGMT version on https://github.com/GenericMappingTools/try-gmt (after conda-forge update)
- [ ] Announce the release on:
  - [ ] GMT [forum](https://forum.generic-mapping-tools.org/c/news/) (do this announcement first! draft on https://hackmd.io/@pygmt. requires moderator status)
  - [ ] [Twitter](https://twitter.com/gmt_dev) (after forum announcement)
---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
