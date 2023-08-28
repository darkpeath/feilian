# -*- coding: utf-8 -*-

try:
    from ._dist_ver import VERSION, __version__
except ImportError:
    try:
        from importlib_metadata import version, PackageNotFoundError
        __version__ = version("feilian")
    except PackageNotFoundError:
        # package is not installed
        __version__ = "UNKNOWN"
    VERSION = __version__.split('.')
