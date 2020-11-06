---
name: PyGMT release checklist
about: Checklist for a new PyGMT release.
title: 'Release PyGMT x.x.x'
labels: 'maintenance'
assignees: ''

---

**Release**: [v0.x.x](https://github.com/GenericMappingTools/pygmt/milestones/0.x.x)
**Scheduled Date**: YYYY/MM/DD

**Before release**:
- [ ] Reserve a DOI on [Zenodo](https://zenodo.org) by clicking on "New Version"
- [ ] Update Changelog
- [ ] Add a new entry in `doc/_static/version_switch.js` for documentation switcher
- [ ] Update citation information https://github.com/GenericMappingTools/pygmt#citing-pygmt

**Release**:
- [ ] Go to [GitHub Release](https://github.com/GenericMappingTools/pygmt/releases) and make a release, this will automatically create a tag too
- [ ] Manually upload the pygmt-vX.Y.Z.zip file to https://zenodo.org/deposit, make sure you file it under the correct reserved DOI

**After release**:
- [ ] Update conda-forge [pygmt-feedstock](https://github.com/conda-forge/pygmt-feedstock) [Usually done automatically by conda-forge's bot]
- [ ] Bump PyGMT version on https://github.com/GenericMappingTools/try-gmt
- [ ] Announce the release on:
  - [ ] GMT [forum](https://forum.generic-mapping-tools.org/c/news/)
  - [ ] [Major/Minor releases only] GMT [website](https://github.com/GenericMappingTools/website) (News)
  - [ ] [ResearchGate](https://www.researchgate.net/project/PyGMT-A-Python-interface-for-the-Generic-Mapping-Tools)

---

- [ ] Party :tada: (don't tick before all other checkboxes are ticked!)
