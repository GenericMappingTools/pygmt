# Maintainers Guide

This page contains instructions for project maintainers about how our setup works,
making releases, creating packages, etc.

If you want to make a contribution to the project, see the
[Contributing Guide](https://github.com/GenericMappingTools/pygmt/blob/master/CONTRIBUTING.md)
instead.

## Onboarding Access Checklist

- Added to [python-maintainers](https://github.com/orgs/GenericMappingTools/teams/python-maintainers) team in the [GenericMappingTools](https://github.com/orgs/GenericMappingTools/teams/) organization on GitHub (gives 'maintain' permissions)
- Added as collaborator on [DAGsHub](https://dagshub.com/GenericMappingTools/pygmt/settings/collaboration) (gives 'write' permission to dvc remote storage)
- Added as moderator on [GMT forum](https://forum.generic-mapping-tools.org) (to see mod-only discussions)
- Added as member on the [PyGMT devs Slack channel](https://pygmtdevs.slack.com) (for casual conversations)
- Added as maintainer on [PyPI](https://pypi.org/project/pygmt/) and [Test PyPI](https://test.pypi.org/project/pygmt) [optional]
- Added as member on [HackMD](https://hackmd.io/@pygmt) [optional]

## Branches

* *master*: Always tested and ready to become a new version. Don't push directly to this
  branch. Make a new branch and submit a pull request instead.
* *gh-pages*: Holds the HTML documentation and is served by GitHub. Pages for the master
  branch are in the `dev` folder. Pages for each release are in their own folders.
  **Automatically updated by GitHub Actions** so you shouldn't have to make commits here.


## Reviewing and merging pull requests

A few guidelines for reviewing:

* Always **be polite** and give constructive feedback.
* Welcome new users and thank them for their time, even if we don't plan on merging the
  PR.
* Don't be harsh with code style or performance. If the code is bad, either (1) merge
  the pull request and open a new one fixing the code and pinging the original submitter
  (2) comment on the PR detailing how the code could be improved. Both ways are focused
  on showing the contributor **how to write good code**, not shaming them.

Pull requests should be **squash merged**.
This means that all commits will be collapsed into one.
The main advantages of this are:

* Eliminates experimental commits or commits to undo previous changes.
* Makes sure every commit on master passes the tests and has a defined purpose.
* The maintainer writes the final commit message, so we can make sure it's good and
  descriptive.


## Continuous Integration

We use GitHub Actions continuous integration (CI) services to
build and test the project on Linux, macOS and Windows.
They rely on the `environment.yml` file to install required dependencies using
conda and the `Makefile` to run the tests and checks.

There are 9 configuration files located in `.github/workflows`:

1. `style_checks.yaml` (Code lint and style checks)

   This is run on every commit to the *master* and Pull Request branches.
   It is also scheduled to run daily on the *master* branch.

2. `ci_tests.yaml` (Tests on Linux/macOS/Windows)

   This is run on every commit to the *master* and Pull Request branches.
   It is also scheduled to run daily on the *master* branch.
   In draft Pull Requests, only two jobs on Linux (minimum NEP29 Python/NumPy versions
   and latest Python/NumPy versions) are triggered to save on Continuous Integration
   resources.

3. `ci_docs.yml` (Build documentation on Linux/macOS/Windows)

   This is run on every commit to the *master* and Pull Request branches.
   In draft Pull Requests, only the job on Linux is triggered to save on
   Continuous Integration resources.

   On the *master* branch, the workflow also handles the documentation
   deployment:

   * Updating the development documentation by pushing the built HTML pages
     from the *master* branch onto the `dev` folder of the *gh-pages* branch.
   * Updating the `latest` documentation link to the new release.

4. `ci_tests_dev.yaml` (GMT Dev Tests on Linux/macOS/Windows).

   This is triggered when a PR is marked as "ready for review", or using the
   slash command `/test-gmt-dev`. It is also scheduled to run daily on the
   *master* branch.

5. `cache_data.yaml` (Caches GMT remote data files needed for GitHub Actions CI)

   This is scheduled to run every Sunday at 12:00 (UTC).
   If new remote files are needed urgently, maintainers can manually uncomment
   the 'pull_request:' line in that `cache_data.yaml` file to refresh the cache.

6. `publish-to-pypi.yml` (Publish wheels to PyPI and TestPyPI)

   This workflow is run to publish wheels to PyPI and TestPyPI (for testing only).
   Archives will be pushed to TestPyPI on every commit to the *master* branch
   and tagged releases, and to PyPI for tagged releases only.

7. `release-drafter.yml` (Drafts the next release notes)

    This workflow is run to update the next releases notes as pull requests are
    merged into master.

8. `check-links.yml` (Check links in the repository and website)

   This workflow is run weekly to check all external links in plaintext and
   HTML files. It will create an issue if broken links are found.

9. `format-command.yml` (Format the codes using slash command)

   This workflow is triggered in a PR if the slash command `/format` is used.

10. `dvc-diff.yml` (Report changes to test images on dvc remote)

    This workflow is triggered in a PR when any *.png.dvc files have been added,
    modified, or deleted. A GitHub comment will be published that contains a summary
    table of the images that have changed along with a visual report.

## Continuous Documentation

We use the [Vercel for GitHub](https://github.com/apps/vercel) App to preview changes
made to our documentation website every time we make a commit in a pull request.
The service has a configuration file `vercel.json`, with a list of options to
change the default behaviour at https://vercel.com/docs/configuration.
The actual script `package.json` is used by Vercel to install the necessary packages,
build the documentation, copy the files to a 'public' folder and deploy that to the web,
see https://vercel.com/docs/build-step.


## Dependencies Policy

PyGMT has adopted [NEP29](https://numpy.org/neps/nep-0029-deprecation_policy)
alongside the rest of the Scientific Python ecosystem, and therefore supports:

* All minor versions of Python released 42 months prior to the project,
  and at minimum the two latest minor versions.
* All minor versions of NumPy released in the 24 months prior to the project,
  and at minimum the last three minor versions.

In `setup.py`, the `python_requires` variable should be set to the minimum
supported version of Python. Minimum Python and NumPy version support should be
adjusted upward on every major and minor release, but never on a patch release.


## Backwards compatibility and deprecation policy

PyGMT is still undergoing rapid developement. All of the API is subject to change
until the v1.0.0 release.

Basic policy for backwards compatibility:

- Any incompatible changes should go through the deprecation process below.
- Incompatible changes are only allowed in major and minor releases, not in
  patch releases.
- Incompatible changes should be documented in the release notes.

When making incompatible changes, we should follow the process:

- Discuss whether the incompatible changes are necessary on GitHub.
- Make the changes in a backwards compatible way, and raise a `FutureWarning`
  warning for old usage. At least one test using the old usage should be added.
- The warning message should clearly explain the changes and include the versions
  in which the old usage is deprecated and is expected to be removed.
- The `FutureWarning` warning should appear for 2-4 minor versions, depending on
  the impact of the changes. It means the deprecation period usually lasts
  3-12 months.
- Remove the old usage and warning when reaching the declared version.

To rename a function parameter, add the `@deprecated_parameter` decorator
before the function definition (but after the `@use_alias` decorator if it exists).
Here is an example:

```
@fmt_docstring
@use_alias(J="projection", R="region", V="verbose")
@kwargs_to_strings(R="sequence")
@deprecate_parameter("sizes", "size", "v0.4.0", remove_version="v0.6.0")
def plot(self, x=None, y=None, data=None, size=None, direction=None, **kwargs):
    pass
```

In this case, the old parameter name `sizes` is deprecated since v0.4.0, and will be
fully removed in v0.6.0. The new parameter name is `size`.


## Making a Release

We try to automate the release process as much as possible.
GitHub Actions workflow handles publishing new releases to PyPI and updating the documentation.
The version number is set automatically using setuptools_scm based information
obtained from git.
There are a few steps that still must be done manually, though.

### Updating the changelog

The Release Drafter GitHub Action will automatically keep a draft changelog at
https://github.com/GenericMappingTools/pygmt/releases, adding a new entry
every time a Pull Request (with a proper label) is merged into the master branch.
This release drafter tool has two configuration files, one for the GitHub Action
at .github/workflows/release-drafter.yml, and one for the changelog template
at .github/release-drafter.yml. Configuration settings can be found at
https://github.com/release-drafter/release-drafter.

The drafted release notes are not perfect, so we will need to tidy it prior to
publishing the actual release notes at https://www.pygmt.org/latest/changes.html.

1. Go to https://github.com/GenericMappingTools/pygmt/releases and click on the
   'Edit' button next to the current draft release note. Copy the text of the
   automatically drafted release notes under the 'Write' tab to
   `doc/changes.md`. Add a section separator `---` between the new and old
   changelog sections.
2. Update the DOI badge in the changelog. Remember to replace the DOI number
   inside the badge url.

    ```
    [![Digital Object Identifier for PyGMT vX.Y.Z](https://zenodo.org/badge/DOI/10.5281/zenodo.<INSERT-DOI-HERE>.svg)](https://doi.org/10.5281/zenodo.<INSERT-DOI-HERE>)
    ```
3. Open a new Pull Request using the title 'Changelog entry for vX.Y.Z' with
   the updated release notes, so that other people can help to review and
   collaborate on the changelog curation process described next.
4. Edit the change list to remove any trivial changes (updates to the README,
   typo fixes, CI configuration, etc).
5. Edit the list of people who contributed to the release, linking to their
   GitHub account. Sort their names by the number of commits made since the
   last release (e.g., use `git shortlog HEAD...v0.1.2 -sne`).
6. Update `README.rst` with new information on the new release version, namely
   the BibTeX citation, a vX.Y.Z documentation link, and compatibility with
   Python and GMT versions.

### Check the README syntax

GitHub is a bit forgiving when it comes to the RST syntax in the README but PyPI is not.
So slightly broken RST can cause the PyPI page to not render the correct content. Check
using the `rst2html.py` script that comes with docutils:

```
python setup.py --long-description | rst2html.py --no-raw > index.html
```

Open `index.html` and check for any flaws or error messages.

### Pushing to PyPI and updating the documentation

After the changelog is updated, making a release can be done by going to
https://github.com/GenericMappingTools/pygmt/releases, editing the draft release,
and clicking on publish. A git tag will also be created, make sure that this
tag is a proper version number (following [Semantic Versioning](https://semver.org/))
with a leading `v`. E.g. `v0.2.1`.

Once the release/tag is created, this should trigger GitHub Actions to do all the work for us.
A new source distribution will be uploaded to PyPI, a new folder with the documentation
HTML will be pushed to *gh-pages*, and the `latest` link will be updated to point to
this new folder.

### Archiving on Zenodo

Grab a zip file from the GitHub release and upload to Zenodo using the previously
reserved DOI.

### Updating the conda package

When a new version is released on PyPI, conda-forge's bot automatically creates version
updates for the feedstock. In most cases, the maintainers can simply merge that PR.

If changes need to be done manually, you can:

1. Fork the [pygmt feedstock repository](https://github.com/conda-forge/pygmt-feedstock) if
   you haven't already. If you have a fork, update it.
2. Update the version number and sha256 hash on `recipe/meta.yaml`. You can get the hash
   from the PyPI "Download files" section.
3. Add or remove any new dependencies (most are probably only `run` dependencies).
4. Make a new branch, commit, and push the changes **to your personal fork**.
5. Create a PR against the original feedstock master.
6. Once the CI tests pass, merge the PR or ask a maintainer to do so.
