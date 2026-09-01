# -*- coding: utf-8 -*-

try:
    from ._dist_ver import VERSION, __version__
except ImportError:
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:
        # fallback for python < 3.8
        from importlib_metadata import version, PackageNotFoundError
    try:
        __version__ = version('feilian')
    except PackageNotFoundError:
        # package is not installed
        __version__ = "UNKNOWN"
    VERSION = __version__.split('.')
