import os
from setuptools import setup, find_packages
# import versioneer

# VERSIONEER SETUP
# #############################################################################
# versioneer.VCS = 'git'
# versioneer.versionfile_source = 'gmt/_version.py'
# versioneer.versionfile_build = 'gmt/_version.py'
# versioneer.tag_prefix = 'v'
# versioneer.parentdir_prefix = '.'

# PACKAGE METADATA
# #############################################################################
NAME = 'gmt-python'
FULLNAME = 'GMT Python Interface'
DESCRIPTION = ""
AUTHOR = "Leonardo Uieda"
AUTHOR_EMAIL = 'leouieda@gmail.com'
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
# VERSION = versioneer.get_version()
VERSION = '0.1a0'
with open("README.rst") as f:
    LONG_DESCRIPTION = ''.join(f.readlines())
PACKAGES = find_packages(exclude=['doc', 'ci'])
LICENSE = ""
URL = "https://github.com/GenericMappingTools/gmt-python"
PLATFORMS = "Any"
SCRIPTS = []
# PACKAGE_DATA = {'': [os.path.join('data', '*')]}
PACKAGE_DATA = {}
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: {}".format(LICENSE),
]
KEYWORDS = ''

# DEPENDENCIES
# #############################################################################
INSTALL_REQUIRES = [
    'numpy',
]

if __name__ == '__main__':
    setup(name=NAME,
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
          classifiers=CLASSIFIERS,
          keywords=KEYWORDS,
          install_requires=INSTALL_REQUIRES)
