# pylint: disable=E0611
# pylint: disable=W0403

"""
This module provides a way to cache key network and system information
This improves reporting performance.
"""

try:
    # this seems to work for Python3
    import netshowlib.netshowlib as nnlib
except ImportError:
    # this seems to work for Python2
    import netshowlib as nnlib


def cache():
    """
    Performs OS discovery and returns the OS appropriate Cache() module
    """
    os_type = nnlib.os_check()
    if os_type:
        cache_path = "netshowlib.%s.cache" % os_type
        cache_module = nnlib.import_module(cache_path)
        return cache_module.Cache()
    return None
