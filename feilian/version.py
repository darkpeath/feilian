# -*- coding: utf-8 -*-

try:
    from ._dist_ver import VERSION, __version__
except ImportError:
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root='..', relative_to=__file__)
    except (ImportError, LookupError):
        from importlib.metadata import version, PackageNotFoundError
        try:
            __version__ = version('feilian')
        except PackageNotFoundError:
            # package is not installed
            __version__ = "UNKNOWN"
    VERSION = __version__.split('.')
