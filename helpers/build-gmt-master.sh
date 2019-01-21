#!/bin/bash
# Download and build the GMT master branch. Used by TravisCI.

set -e

mkdir -p "$INSTALLDIR"
mkdir -p "$COASTLINEDIR"
git clone --depth=1 --branch=travis-build https://github.com/GenericMappingTools/gmt.git tmp
mkdir -p gmt-master
cp -r tmp/* gmt-master
rm -rf tmp
cd gmt-master
bash ci/download-coastlines.sh
bash ci/build-gmt.sh

set +e
