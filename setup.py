"""
Build and install the project.
"""
from setuptools import find_packages, setup

NAME = "pygmt"
FULLNAME = "PyGMT"
AUTHOR = "The PyGMT Developers"
AUTHOR_EMAIL = "leouieda@gmail.com"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "BSD License"
URL = "https://github.com/GenericMappingTools/pygmt"
DESCRIPTION = "A Python interface for the Generic Mapping Tools"
KEYWORDS = ""
with open("README.rst") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

PACKAGES = find_packages(exclude=["doc"])
SCRIPTS = []
PACKAGE_DATA = {"pygmt.tests": ["data/*", "baseline/*"]}

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    f"License :: OSI Approved :: {LICENSE}",
]
PLATFORMS = "Any"
PYTHON_REQUIRES = ">=3.7"
INSTALL_REQUIRES = ["numpy>=1.17", "pandas", "xarray", "netCDF4", "packaging"]
# Configuration for setuptools-scm
SETUP_REQUIRES = ["setuptools_scm"]
USE_SCM_VERSION = {"local_scheme": "node-and-date", "fallback_version": "unknown"}

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        use_scm_version=USE_SCM_VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        scripts=SCRIPTS,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
    )
