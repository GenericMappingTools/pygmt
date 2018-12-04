#!/bin/bash
# Build latest GMT master branch

# To return a failure if any commands inside fail
set -e

export INSTALLDIR="$HOME/gmt-install-dir";
export COASTLINEDIR="$HOME/gmt-install-dir/coast";

git clone --depth=1 https://github.com/GenericMappingTools/gmt ${HOME}/gmt-master
cd ${HOME}/gmt-master
bash ci/travis-setup.sh
bash ci/travis-build.sh
cd ${TRAVIS_BUILD_DIR}

export PATH=$INSTALLDIR/bin:$PATH
export LD_LIBRARY_PATH=$INSTALLDIR/lib:$LD_LIBRARY_PATH

# Turn off exit on failure.
set +e
