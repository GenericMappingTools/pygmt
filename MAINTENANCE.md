# Maintainers Guide

This page contains instructions for project maintainers about how our setup works,
making releases, creating packages, etc.

If you want to make a contribution to the project, see the
[Contributing Guide](CONTRIBUTING.md) instead.


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
They rely on the `requirements.txt` file to install required dependencies using
conda and the `Makefile` to run the tests and checks.

### GitHub Actions

There are 4 configuration files located in `.github/workflows`:

1. `ci_tests.yaml` (Style Checks, Tests on Linux/macOS/Windows)

This is ran on every commit on the *master* and Pull Request branches.
It is also scheduled to run daily on the *master* branch.

On the *master* branch, the workflow also handles the documentation deployment:

* Updating the development documentation by pushing the built HTML pages from the
  *master* branch onto the `dev` folder of the *gh-pages* branch.
* Updated the `latest` documentation link to the new release.

2. `ci_tests_dev.yaml` (GMT Latest Tests on Linux/macOS/Windows).

This is only triggered when a review is requested or re-requested on a PR.
It is also scheduled to run daily on the *master* branch.

3. `cache_data.yaml` (Caches GMT remote data files needed for GitHub Actions CI)

This is scheduled to run every Sunday at 12 noon.
If new remote files are needed urgently, maintainers can manually uncomment
the 'pull_request:' line in that `cache_data.yaml` file to refresh the cache.

4. `publish-to-pypi.yml` (Publish wheels to PyPI and TestPyPI)

This workflow is ran to publish wheels to PyPI and TestPyPI (for testing only).
Archives will be pushed to TestPyPI on every commit to the *master* branch and
tagged releases, and to PyPI for tagged releases only.


## Continuous Documentation

We use the [Vercel for GitHub](https://github.com/apps/vercel) App to preview changes
made to our documentation website every time we make a commit in a pull request.
The service has a configuration file `vercel.json`, with a list of options to
change the default behaviour at https://vercel.com/docs/configuration.
The actual script `package.json` is used by Vercel to install the necessary packages,
build the documentation, copy the files to a 'public' folder and deploy that to the web,
see https://vercel.com/docs/build-step.

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

1. Generate a list of commits between the last release tag and now:

    ```bash
    git log HEAD...v0.1.2 --pretty="* %s" > changes.txt
    ```

2. Edit the changes list to remove any trivial changes (updates to the README, typo
   fixes, CI configuration, etc).
3. Replace the PR number in the commit titles with a link to the GitHub PR page.
   Use ``sed -i.bak -E 's$\(#([0-9]*)\)$(`#\1 <https://github.com/GenericMappingTools/pygmt/pull/\1>`__)$g' changes.rst``
   to make the change automatically.
4. Copy the remaining changes to `doc/changes.rst` under a new section for the
   intended release.
5. Add a list of people who contributed to the release (use
   `` git shortlog HEAD...v0.1.2 -sne ``).
6. Include the DOI badge in the changelog. Remember to replace your DOI inside the badge url.

    ```
    .. image:: https://zenodo.org/badge/DOI/<INSERT-DOI-HERE>.svg
        :alt: Digital Object Identifier for the Zenodo archive
        :target: https://doi.org/<INSERT-DOI-HERE>
    ```

7. Add a link to the new release version documentation in `README.rst`.
8. Open a new PR with the updated changelog.

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
