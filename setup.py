# -*- coding: utf-8 -*-

import os
import io
from setuptools import setup, find_packages

NAME = "feilian"
DESCRIPTION = "General data processing tool."
REQUIRES = [
    "pandas",
]
EXTRA_REQUIRES = [
    "tqdm",
]

PACKAGES = find_packages(exclude=['tests'])

HERE = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='darkpeath',
    author_email='darkpeath@gmail.com',
    url="https://github.com/darkpeath/feilian",
    packages=PACKAGES,
    include_package_data=True,
    platforms="any",
    install_requires=REQUIRES,
    extras_require={"extra": EXTRA_REQUIRES},
    tests_require=["pytest"],
    scripts=[],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
