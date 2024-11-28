# Maintainers Guide

This page contains instructions for project maintainers about how our setup works,
making releases, creating packages, etc.

If you want to make a contribution to the project, see the [](contributing.md) instead.

## Onboarding/Offboarding Access Checklist

Note that anyone can contribute to PyGMT, even without being added to the
[GenericMappingTools team](https://github.com/orgs/GenericMappingTools/teams).
The onboarding items below are for people who would like to make regular
contributions, and could benefit from extra permissions to the developer and
communication tools we use.

### As a Contributor

- Add to the [pygmt-contributors team](https://github.com/orgs/GenericMappingTools/teams/pygmt-contributors) (gives 'write' permission to the repository)
- Add as a collaborator on [DAGsHub](https://dagshub.com/GenericMappingTools/pygmt) (gives 'write' permission to dvc remote storage)
- Add as a member on [HackMD](https://hackmd.io/@pygmt) (for draft announcements) [optional]

### As a Maintainer

- Add to the [pygmt-maintainers team](https://github.com/orgs/GenericMappingTools/teams/pygmt-maintainers) (gives 'maintain' permission to the repository)
- Add to "Active Maintainers" on the [Team Gallery page](team.md)
- Add as a moderator on the [GMT forum](https://forum.generic-mapping-tools.org) (to see mod-only discussions) [optional]
- Add as a maintainer on [ReadtheDocs](https://readthedocs.org/projects/pygmt-dev) [optional]
- Add as a curator to the [GMT community](https://zenodo.org/communities/generic-mapping-tools/) on Zenodo (for making releases) [optional]

### As an Administrator

- Add to the [pygmt-admin team](https://github.com/orgs/GenericMappingTools/teams/pygmt-admin) (gives 'admin' permission to the repository)
- Add as an admin on [DAGsHub](https://www.dagshub.com/GenericMappingTools/pygmt)
- Add as a maintainer on [PyPI](https://pypi.org/project/pygmt/) and [Test PyPI](https://test.pypi.org/project/pygmt) [optional]

**Note**: When a maintainer is no longer active (no activity in one year), we will mirror
the onboarding access checklist:

- Move from the [pygmt-maintainers team](https://github.com/orgs/GenericMappingTools/teams/pygmt-maintainers)
  to the [pygmt-contributors team](https://github.com/orgs/GenericMappingTools/teams/pygmt-contributors)
- Move from "Active Maintainers" to "Distinguished Contributors" on the [Team Gallery page](team.md)
- Remove 'maintain' permission from GMT forum, ReadTheDocs, Zenodo

## Branches

* *main*: Always tested and ready to become a new version. Don't push directly to this
  branch. Make a new branch and submit a pull request instead.
* *gh-pages*: Holds the HTML documentation and is served by GitHub. Pages for the main
  branch are in the `dev` folder. Pages for each release are in their own folders.
  **Automatically updated by GitHub Actions** so you shouldn't have to make commits here.

## Managing GitHub Issues

A few guidelines for managing GitHub issues:

* Assign [labels](https://github.com/GenericMappingTools/pygmt/labels) and the expected
  [milestone](https://github.com/GenericMappingTools/pygmt/milestones) to issues as
  appropriate.
* When people request to work on an open issue, either assign the issue to that person
  and post a comment about the assignment or explain why you are not assigning the
  issue to them and, if possible, recommend other issues for them to work on.
* People with write access should self-assign issues and/or comment on the issues that
  they will address.
* For upstream bugs, close the issue after an upstream release fixes the bug. If
  possible, post a comment when an upstream PR is merged that fixes the problem, and
  consider adding a regression test for serious bugs.

## Reviewing and Merging Pull Requests

A few guidelines for reviewing:

* Always **be polite** and give constructive feedback.
* Welcome new users and thank them for their time, even if we don't plan on merging the
  PR.
* Don't be harsh with code style or performance. If the code is bad, either (1) merge
  the pull request and open a new one fixing the code and pinging the original submitter
  or (2) comment on the PR detailing how the code could be improved. Both ways are
  focused on showing the contributor **how to write good code**, not shaming them.

Pull requests should be **squash merged**.
This means that all commits will be collapsed into one.
The main advantages of this are:

* Eliminates experimental commits or commits to undo previous changes.
* Makes sure every commit on the main branch passes the tests and has a defined purpose.
* The maintainer writes the final commit message, so we can make sure it's good and
  descriptive.


## Continuous Integration

We use GitHub Actions continuous integration (CI) services to build, test and
manage the project on Linux, macOS and Windows. The GitHub Actions CI are
controlled by workflow files located in `.github/workflows`. Here we briefly
summarize the functions of the workflows. Please refer to the comments in the
workflow files for more details.

- `benchmarks.yml`: Benchmarks the execution speed of tests to track performance of PyGMT functions
- `cache_data.yaml`: Cache GMT remote data files and uplodas as artifacts
- `check-links.yml`: Check links in the repository and documentation
- `ci_docs.yml`: Build documentation on Linux/macOS/Windows and deploy to GitHub
- `ci_doctest.yaml`: Run all doctests on Linux/macOS/Windows
- `ci_tests.yaml`: Run regular PyGMT tests on Linux/macOS/Windows
- `ci_tests_dev.yaml`: Run regular PyGMT tests with GMT dev version on Linux/macOS/Windows
- `ci_tests_legacy.yaml`: Run regular PyGMT tests with GMT legacy versions on Linux/macOS/Windows
- `dvc-diff.yml`: Report changes in test images
- `format-command.yml`: Format the codes using slash command
- `publish-to-pypi.yml`: Publish archives to PyPI and TestPyPI
- `release-baseline-images.yml`: Upload the ZIP archive of baseline images as a release asset
- `release-drafter.yml`: Draft the next release notes
- `slash-command-dispatch.yml`: Support slash commands in pull requests
- `style_checks.yaml`: Code lint and style checks
- `type_checks.yml`: Static type checks


## Continuous Documentation

We use the [ReadtheDocs](https://readthedocs.org/) service to preview changes
made to our documentation website every time we make a commit in a pull request.
The service has a configuration file `.readthedocs.yaml`, with a list of options
to change the default behaviour at <https://docs.readthedocs.io/en/stable/config-file/index.html>.

## Continuous Benchmarking

We use the [CodSpeed](https://codspeed.io) service to continuously track PyGMT's
performance. The `pytest-codspeed` plugin collects benchmark data and uploads it to the
CodSpeed server, where results are available at <https://codspeed.io/GenericMappingTools/pygmt>.

Benchmarking is handled through the `benchmarks.yml` GitHub Actions workflow. It's
automatically executed when a pull request is merged into the main branch. To trigger
benchmarking in a pull request, add the `run/benchmark` label to the pull request.

To include a new test in the benchmark suite, apply the `@pytest.mark.benchmark`
decorator to a test function.

## Dependencies Policy

PyGMT has adopted [SPEC 0](https://scientific-python.org/specs/spec-0000/) alongside the
rest of the scientific Python ecosystem, and made a few extensions based on the needs of
the project. Please see [Minimum Supported Versions](minversions.md) for the detailed
policy and the minimum supported versions of GMT, Python and core package dependencies.

In `pyproject.toml`, the `requires-python` key should be set to the minimum supported
version of Python. Minimum supported versions of GMT, Python and core package
dependencies should be adjusted upward on every major and minor release, but never on a
patch release.


## Backwards Compatibility and Deprecation Policy

PyGMT is still undergoing rapid development. All of the API is subject to change
until the v1.0.0 release. Versioning in PyGMT is based on the
[semantic versioning specification](https://semver.org/spec/v2.0.0.html)
(i.e., v*MAJOR*.*MINOR*.*PATCH*).
Basic policy for backwards compatibility:

- Any incompatible changes should go through the deprecation process below.
- Incompatible changes are only allowed in major and minor releases, not in
  patch releases.
- Incompatible changes should be documented in the release notes.

When making incompatible changes, we should follow the process:

- Discuss whether the incompatible changes are necessary on GitHub.
- Make the changes in a backwards compatible way, and raise a `FutureWarning`
  warning for the old usage. At least one test using the old usage should be added.
- The warning message should clearly explain the changes and include the versions
  in which the old usage is deprecated and is expected to be removed.
- The `FutureWarning` warning should appear for 2-4 minor versions, depending on
  the impact of the changes. It means the deprecation period usually lasts
  3-12 months.
- Remove the old usage and warning when reaching the declared version.

To rename a function parameter, add the `@deprecate_parameter` decorator near
the top after the `@fmt_docstring` decorator but before the `@use_alias`
decorator (if those two exist). Here is an example:

```
@fmt_docstring
@deprecate_parameter("columns", "incols", "v0.4.0", remove_version="v0.6.0")
@use_alias(J="projection", R="region", V="verbose", i="incols")
@kwargs_to_strings(R="sequence", i="sequence_comma")
def plot(self, x=None, y=None, data=None, size=None, direction=None, **kwargs):
    pass
```

In this case, the old parameter name `columns` is deprecated since v0.4.0, and
will be fully removed in v0.6.0. The new parameter name is `incols`.


## Making a Release

We try to automate the release process as much as possible.
GitHub Actions workflow handles publishing new releases to PyPI and updating the documentation.
The version number is set automatically using [setuptools_scm](https://pypi.org/project/setuptools-scm/)
based information obtained from git.
There are a few steps that still must be done manually, though.

### Updating the Changelog

The [Release Drafter](https://github.com/release-drafter/release-drafter) GitHub Action
will automatically keep a draft changelog at
<https://github.com/GenericMappingTools/pygmt/releases>, adding a new entry
every time a pull request (with a proper label) is merged into the main branch.
This release drafter tool has two configuration files, one for the GitHub Action
at `.github/workflows/release-drafter.yml`, and one for the changelog template
at `.github/release-drafter.yml`. Configuration settings can be found at
<https://github.com/release-drafter/release-drafter>.

The drafted release notes are not perfect, so we will need to tidy it prior to
publishing the actual release notes at [](changes.md).

1. Go to <https://github.com/GenericMappingTools/pygmt/releases> and click on the
   'Edit' button next to the current draft release note. Copy the text of the
   automatically drafted release notes under the 'Write' tab to
   `doc/changes.md`. Add a section separator `---` between the new and old
   changelog sections.
2. Update the DOI badge in the changelog. Remember to replace the DOI number
   inside the badge url.

    ```
    [![Digital Object Identifier for PyGMT vX.Y.Z](https://zenodo.org/badge/DOI/10.5281/zenodo.<INSERT-DOI-HERE>.svg)](https://doi.org/10.5281/zenodo.<INSERT-DOI-HERE>)
    ```
3. Open a new pull request using the title 'Changelog entry for vX.Y.Z' with
   the updated release notes, so that other people can help to review and
   collaborate on the changelog curation process described next.
4. Edit the change list to remove any trivial changes (updates to the README,
   typo fixes, CI configuration, test updates due to GMT releases, etc).
5. Sort the items within each section (i.e., New Features, Enhancements, etc.)
   such that similar items are located near each other (e.g., new wrapped
   modules and methods, gallery examples, API docs changes) and entries within each group
   are alphabetical.
6. Move a few important items from the main sections to the Highlights section.
7. Edit the list of people who contributed to the release, linking to their
   GitHub accounts. Sort their names by the number of commits made since the
   last release (e.g., use `git shortlog HEAD...v0.4.0 -sne`).
8. Update `doc/minversions.md` with new information on the new release version,
   including a vX.Y.Z documentation link, and minimum required versions of GMT, Python
   and core package dependencies (NumPy, pandas, Xarray). Follow
   [SPEC 0](https://scientific-python.org/specs/spec-0000/) for updates.
9. Refresh citation information. Specifically, the BibTeX in `README.md` and
   `CITATION.cff` needs to be updated with any metadata changes, including the
   DOI, release date, and version information. Please also follow
   guidelines in `AUTHORSHIP.md` for updating the author list in the BibTeX.
   More information about the `CITATION.cff` specification can be found at
   <https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md>.

### Pushing to PyPI and Updating the Documentation

After the changelog is updated, making a release can be done by going to
<https://github.com/GenericMappingTools/pygmt/releases>, editing the draft release,
and clicking on publish. A git tag will also be created, make sure that this
tag is a proper version number (following [Semantic Versioning](https://semver.org/))
with a leading `v` (e.g., `v0.2.1`).

Once the release/tag is created, this should trigger GitHub Actions to do all the work for us.
A new source distribution will be uploaded to PyPI, a new folder with the documentation
HTML will be pushed to *gh-pages*, and the `latest` link will be updated to point to
this new folder.

### Archiving on Zenodo

Grab both the source code and baseline images ZIP files from the GitHub release page
and upload them to Zenodo using the previously reserved DOI.

### Updating the Conda Package

When a new version is released on PyPI, conda-forge's bot automatically creates version
updates for the feedstock. In most cases, the maintainers can simply merge that PR.

If changes need to be done manually, you can:

1. Fork the [pygmt feedstock repository](https://github.com/conda-forge/pygmt-feedstock) if
   you haven't already. If you have a fork, update it.
2. Update the version number and sha256 hash on `recipe/meta.yaml`. You can get the hash
   from the [PyPI "Download files" section](https://pypi.org/project/pygmt/#files).
3. Add or remove any new dependencies (most are probably only `run` dependencies).
4. Make sure the minimum support versions of all dependencies are correctly pinned.
5. Make a new branch, commit, and push the changes **to your personal fork**.
6. Create a PR against the original feedstock main.
7. Once the CI tests pass, merge the PR or ask a maintainer to do so.
