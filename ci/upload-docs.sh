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

REPO=gmt-python
USER=GenericMappingTools
BRANCH=gh-pages
CLONE_ARGS="--quiet --branch=$BRANCH --single-branch"
REPO_URL=https://${GH_TOKEN}@github.com/${USER}/${REPO}.git

echo "Preparing to push HTML to branch ${BRANCH} of ${USER}/${REPO}"

if [ "$TRAVIS_PULL_REQUEST" == "false" ] &&
   [ "$TRAVIS_BRANCH" == "master" ];
then
    echo -e "Copying generated files."
    cp -R doc/_build/html/ $HOME/keep
    # Go to home and setup git
    cd $HOME
    git config --global user.email "leouieda@gmail.com"
    git config --global user.name "Leonardo Uieda"
    git config --global github.user "leouieda"
    echo -e "Cloning ${USER}/${REPO}"
    # Clone the project, using the secret token.
    # Uses /dev/null to avoid leaking decrypted key.
    git clone ${CLONE_ARGS} ${REPO_URL} deploy > /dev/null
    cd deploy
    # Move the old branch out of the way and create a new one:
    echo -e "Create an empty ${BRANCH} branch"
    git checkout ${BRANCH}
    git branch -m ${BRANCH}-old
    git checkout --orphan ${BRANCH}
    # Delete all the files and replace with our good set
    echo -e "Remove old files from previous builds"
    git rm -rf .
    cp -Rf $HOME/keep/. $HOME/deploy
    # Remove the CNAME file because this is not the main website
    rm -f CNAME
    # add, commit, and push files
    echo -e "Add and commit changes"
    git add -f .
    git commit -m "Push from Travis build $TRAVIS_BUILD_NUMBER"
    echo -e "Pushing..."
    git push -fq origin ${BRANCH} > /dev/null
    echo -e "Finished uploading generated files."
else
    echo -e "Not updating website. This is either a PR or not master."
fi
echo -e "Done"

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e

