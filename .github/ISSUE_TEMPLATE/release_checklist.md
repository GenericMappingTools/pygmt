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
- [ ] Reserve a DOI on [Zenodo](https://zenodo.org) by clicking on "New Version"
- [ ] Finish up 'Changelog entry for v0.x.x' Pull Request:
  - [ ] Add a new entry in `doc/_static/version_switch.js` for documentation switcher
  - [ ] Update citation information https://github.com/GenericMappingTools/pygmt#citing-pygmt
  - [ ] Add the documentation link https://github.com/GenericMappingTools/pygmt#documentation-for-other-versions
  - [ ] Add compatibility information https://github.com/GenericMappingTools/pygmt#compatibility-with-python-and-gmt-versions
  - [ ] Copy draft changelog from Release Drafter and edit it to look nice

**Release**:
- [ ] At the [PyGMT release page on GitHub](https://github.com/GenericMappingTools/pygmt/releases):
  - [ ] Edit the draft release notes with the finalized changelog
  - [ ] Set the tag version and release title to vX.Y.Z
  - [ ] Make a release by clicking the 'Publish Release' button, this will automatically create a tag too
- [ ] Manually upload the pygmt-vX.Y.Z.zip file to https://zenodo.org/deposit, ensure that it is filed under the correct reserved DOI

**After release**:
- [ ] Update conda-forge [pygmt-feedstock](https://github.com/conda-forge/pygmt-feedstock) [Usually done automatically by conda-forge's bot]
- [ ] Bump PyGMT version on https://github.com/GenericMappingTools/try-gmt
- [ ] Announce the release on:
  - [ ] GMT [forum](https://forum.generic-mapping-tools.org/c/news/)
  - [ ] [Major/Minor releases only] GMT [website](https://github.com/GenericMappingTools/website) (News)
  - [ ] [ResearchGate](https://www.researchgate.net/project/PyGMT-A-Python-interface-for-the-Generic-Mapping-Tools)

---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
