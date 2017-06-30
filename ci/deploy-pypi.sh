#!/bin/bash
#
# Push the built HTML pages to the gh-pages branch.
# Only runs if this is not a pull request and is on the master branch.
#
# Based on
# http://sleepycoders.blogspot.com.au/2013/03/sharing-travis-ci-generated-files.html
# and https://github.com/richfitz/wood

# To return a failure if any commands inside fail
set -e

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]] &&
   [[ "$TRAVIS_BRANCH" == "master" ]] &&
   [[ -z "$TRAVIS_TAG" ]];

    # Build source distributions and wheels
    echo "Building packages"
    python setup.py sdist bdist_wheel

    # Upload to PyPI. Credentials are set using env variables.
    twine upload --skip-existing dist/*

then

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
