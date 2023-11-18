#!/usr/bin/env bash
#
# Create a conda environment.yml file based on environment variables and arguments.
#
# Evnironment variables:
#
# - PYTHON_VERSION
# - GMT_VERSION
# - GS_VERSION
# - NUMPY_VERSION
# - PANDAS_VERSION
# - OPTIONAL_PACKAGES
#
if [ "$#" -ne 1 ]; then
  echo "Usage: bash make_environment.sh tests|tests_legacy|tests_dev|docs|doctests"
  exit 1
fi

# pinned packages
PYTHON_VERSION=${PYTHON_VERSION:-3.12}
GMT_VERSION=${GMT_VERSION:-6.4.0}
GS_VERSION=${GS_VERSION:-9.54.0}

gmt="gmt"
required="numpy pandas xarray netCDF4 packaging"
optional="contextily geopandas ipython rioxarray"
build="build make pip"
docs="myst-parser panel sphinx sphinx-copybutton sphinx-design sphinx-gallery sphinx_rtd_theme"
pytest="pytest pytest-doctestplus pytest-mpl"
cov="pytest-cov"
dvc="dvc"
gmtdev="cmake make ninja curl fftw glib hdf5 libblas libcblas libgdal liblapack libnetcdf pcre zlib"

# function to add a package and optionally pin its version
add_package() {
    package=$1
    version=$2
    if [ -z "$version" ]; then
        echo "  - $package"
    else
        echo "  - $package=$version"
    fi
}

# decide the packages to install
case $1 in
    tests)
        if [[ $OPTIONAL_PACKAGES == "yes" ]]; then
            packages="$gmt $required $optional $build $dvc $pytest $cov"
        else
            packages="$gmt $required $build $dvc $pytest $cov"
        fi
        ;;
    tests_legacy)
        packages="$gmt $required $optional $build $dvc $pytest sphinx-gallery"
        ;;
    tests_dev)
        packages="$gmtdev"
        ;;
    docs)
        packages="$gmt $required $optional $build $docs"
        ;;
    doctest)
        packages="$gmt $required $optional $build $pytest"
        ;;
    *)
        exit 1
        ;;
esac

# Environment name and channels
cat << EOF
name: pygmt
channels:
  - conda-forge
  - nodefaults
EOF

# Dependencies
echo "dependencies:"
add_package "python" ${PYTHON_VERSION}
add_package "ghostscript" ${GS_VERSION}

for package in $packages; do
    if [[ $package == "numpy" ]]; then
        add_package "numpy" $NUMPY_VERSION
    elif [[ $package == "pandas" ]]; then
        add_package "pandas" $PANDAS_VERSION
    else
        add_package "$package"
    fi
done
