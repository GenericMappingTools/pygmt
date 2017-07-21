#!/bin/bash

# To return a failure if any commands inside fail
set -e

MINICONDA_URL="http://repo.continuum.io/miniconda"

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    MINICONDA_FILE=Miniconda3-latest-MacOSX-x86_64.sh
    CONDA_PREFIX=/Users/travis/miniconda3
else
    MINICONDA_FILE=Miniconda3-latest-Linux-x86_64.sh
    CONDA_PREFIX=/home/travis/miniconda3
fi
wget $MINICONDA_URL/$MINICONDA_FILE -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b

export PATH=$CONDA_PREFIX/bin:$PATH

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
