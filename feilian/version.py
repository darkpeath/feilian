# -*- coding: utf-8 -*-

from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("feilian")
except PackageNotFoundError:
    # package is not installed
    __version__ = "UNKNOWN"
