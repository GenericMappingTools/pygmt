#!/bin/bash
# Download and build the GMT master branch. Used by TravisCI.

set -e

# Paths for GMT installation
INSTALLDIR="${GMTINSTALLDIR:-$HOME/gmt-install-dir}"
COASTLINEDIR="$INSTALLDIR/coast"
PATH="$INSTALLDIR/bin:$PATH"
LD_LIBRARY_PATH="$INSTALLDIR/lib:$LD_LIBRARY_PATH"

mkdir -p "$INSTALLDIR"
mkdir -p "$COASTLINEDIR"
git clone --depth=1 --branch=master https://github.com/GenericMappingTools/gmt.git tmp
mkdir -p gmt-master
cp -r tmp/* gmt-master
rm -rf tmp
cd gmt-master
bash ci/download-coastlines.sh
bash TEST=false ci/build-gmt.sh

set +e
