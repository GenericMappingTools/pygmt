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
- [ ] Run `grep --include="*.py" -r 'remove_version="vX.Y.Z"' pygmt` from the base of the repository to check if any deprecations and related tests should be removed in this version
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
  - [ ] [ResearchGate](https://www.researchgate.net/project/PyGMT-A-Python-interface-for-the-Generic-Mapping-Tools) (after forum announcement)
  - [ ] [Twitter](https://twitter.com/gmt_dev) (after forum announcement)
---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
