#!/bin/bash
#
# Push the built HTML pages to the gh-pages branch.

# To return a failure if any commands inside fail
set -e

REPO=gmt-python
USER=GenericMappingTools
BRANCH=gh-pages
CLONE_ARGS="--quiet --branch=$BRANCH --single-branch"
REPO_URL=https://${GH_TOKEN}@github.com/${USER}/${REPO}.git
CLONE_DIR=$CLONE_DIR

echo -e "Preparing to push HTML to branch ${BRANCH} of ${USER}/${REPO}"

echo -e "Copying generated files."
cp -R doc/_build/html/ $HOME/keep

# Go to home and setup git
cd $HOME

git config --global user.email "travis@nothing.com"
git config --global user.name "TravisCI"

# Clone the project, using the secret token.
# Uses /dev/null to avoid leaking decrypted key.
echo -e "Cloning ${USER}/${REPO}"
git clone ${CLONE_ARGS} ${REPO_URL} $CLONE_DIR 2>&1 >/dev/null

cd $CLONE_DIR

# Move the old branch out of the way and create a new one:
echo -e "Create an empty ${BRANCH} branch"
git checkout ${BRANCH}
git branch -m ${BRANCH}-old
git checkout --orphan ${BRANCH}

# Delete all the files and replace with our good set
echo -e "Remove old files from previous builds"
git rm -rf .
cp -Rf $HOME/keep/. $HOME/$CLONE_DIR

# Remove the CNAME file because this is not the main website
rm -f CNAME

# add, commit, and push files
echo -e "Add and commit changes"
git add -f .
git commit -m "Push from Travis build $TRAVIS_BUILD_NUMBER"
echo -e "Pushing..."
git push -fq origin ${BRANCH} 2>&1 >/dev/null

echo -e "Finished uploading generated files."

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
