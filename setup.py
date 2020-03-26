"""
Build and install the project.

Uses versioneer to manage version numbers using git tags.
"""
from setuptools import setup, find_packages

import versioneer


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

VERSION = versioneer.get_version()
CMDCLASS = versioneer.get_cmdclass()

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
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: {}".format(LICENSE),
]
PLATFORMS = "Any"
INSTALL_REQUIRES = ["numpy", "pandas", "xarray", "netCDF4", "packaging"]

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
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
        install_requires=INSTALL_REQUIRES,
        cmdclass=CMDCLASS,
    )
