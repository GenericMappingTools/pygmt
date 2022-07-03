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
with open("README.rst", "r", encoding="utf8") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

PACKAGES = find_packages(exclude=["doc"])
SCRIPTS = []
PACKAGE_DATA = {"pygmt.tests": ["data/*", "baseline/*"]}

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    f"License :: OSI Approved :: {LICENSE}",
]
PLATFORMS = "Any"
PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = ["numpy>=1.20", "pandas", "xarray", "netCDF4", "packaging"]

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
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
    )
